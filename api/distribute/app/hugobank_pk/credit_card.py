import pprint

from behave import *
from retry import retry

use_step_matcher("re")

import tests.api.distribute.app_helper as ah
from tests.util.common_util import check_status_distribute


@Step("I fetch credit card constants for ([^']*)")
def fetch_credit_card_constants(context, customer):

    request = context.request

    if "users" not in context.data or not context.data["users"]:
        raise Exception("Stopping test: No users found in context! CHECK 'Background' step fail?")

    uid = list(context.data["users"].keys())[0]

    response = request.hugosave_get_request(
        path=ah.credit_card_urls["get_product_config"],
        headers=ah.get_user_header(context,uid),
    )

    if check_status_distribute(response, 200):

        assert "data" in response, (
            f"Expected 'data' in response, got: {response}"
        )

        data = response["data"]

        for field in ["minCreditLimit", "maxCreditLimit", "lienFactor"]:
            assert field in data, f"Missing '{field}' in credit card constants"

        context.data["credit_card_constants"] = {
            "min_credit_limit": float(data["minCreditLimit"]),
            "max_credit_limit": float(data["maxCreditLimit"]),
            "lien_factor": float(data["lienFactor"]),
        }

    optional_fields = [
                 "annualFee",
                 "annualPercentageRate",
                 "latePaymentFee",
                 "cashAdvanceFee",
                 "atmWithdrawalFee",
                 "fedOnFeesPercent",
             ]

    for field in optional_fields:
        if field in data:
            context.data["credit_card_constants"][field] = data[field]

@step("I validate credit card eligibility using balance of the wallet with product code ([^']*) for user ([^']*)")
def validate_eligibility(context,product_code, uid):
    # uid = list(context.data["users"].keys())[0]

    requested_credit_limit = float(context.table[0]["credit_limit"])

    if "credit_card_constants" not in context.data:
        raise Exception("Error: Credit Card constants missing. Check if you run the 'fetch constants' step")

    cc_constants = context.data["credit_card_constants"]
    min_limit = float(cc_constants["min_credit_limit"])
    max_limit = float(cc_constants["max_credit_limit"])
    lien_factor = float(cc_constants["lien_factor"])

    print(f"\n--- VALIDATION CHECKS ---")
    print(f"Requested Limit: {requested_credit_limit}")

    if not (min_limit <= requested_credit_limit <= max_limit):
        assert False, (
            f"FAIL: Credit limit {requested_credit_limit} is out of bounds! "
            f"Must be between {min_limit} and {max_limit}."
        )


    required_lien_amount = requested_credit_limit * lien_factor
    print(f"Lien Factor: {lien_factor}")
    print(f"Required Lien Amount: {required_lien_amount}")

    # ---------------------------------------------------------
    print("Fetching fresh wallet balance from API...")

    request = context.request
    current_balance = 0.0

    @retry(AssertionError, tries=40, delay=20, logger=None)
    def retry_for_acc_balance():
        response = request.hugosave_get_request(
            path=ah.balance_urls["balances"],
            headers=ah.get_user_header(context, uid),
        )

        b1 = ah.get_balance(response, product_code)
        return b1

    current_balance= retry_for_acc_balance()
    print(f"Fresh Account Balance: {current_balance}")

    if current_balance < required_lien_amount:
        assert False, (
            f"FAIL: Insufficient Funds! "
            f"Balance ({current_balance}) is less than required Lien ({required_lien_amount})"
        )

    print("SUCCESS: User is eligible for this credit limit.")

@Step("I order a credit card for user ([^']*)")
def order_credit_card(context, uid):

    request = context.request

    credit_limit = int(context.table.rows[0]["credit_limit"])
    expected_card_status = context.table.rows[0]["expected_card_status"]

    order_card_req = {
        "product_code": "CARD_PRODUCT_PHYSICAL_SECURED_CREDIT_CARD_VISA",
        "funding_details": {
            "approved_limit": credit_limit,
            "earn_interest_on_lien": True,
        }
    }

    # Fetch card name

    response = request.hugosave_get_request(
        path=ah.user_profile_urls["card_name"],
        headers=ah.get_user_header(context, uid),
    )
    if check_status_distribute(response, 200):
        assert "names" in response["data"], (
            f"Expected names in response, but received: {response}"
        )
        order_card_req["name_on_card"] = response["data"]["names"][0]


    #Prepare headers

    headers = ah.get_user_header(context, uid)

    assert "user_authorisation_token" in context.data["users"][uid], (
        "Final user authorisation token missing for credit card order"
    )

    headers["x-final-user-authorisation-token"] = (
        context.data["users"][uid]["user_authorisation_token"]
    )

    response = request.hugosave_post_request(
        path=ah.card_urls["issue_card"],
        headers=headers,
        data=order_card_req,
    )

    if check_status_distribute(response, 200):

        assert "data" in response, (
            f"Expected data in response, but received: {response}"
        )

        assert response["data"]["cardStatus"] == expected_card_status, (
            f"Expected card status {expected_card_status}, "
            f"but received {response['data']['cardStatus']}"
        )

        context.data["cardOrderStatus"] = response["data"]
        context.data["users"][uid]["card_id"] = response["data"]["cardId"]

@Step("I view the credit card PIN for user ([^']*) and expect the PIN to be returned successfully")
def view_credit_card_pin(context, uid: str):
    request = context.request

    card_id = context.data["users"][uid]["card_id"]

    headers = ah.get_user_header(context, uid)

    headers["x-final-user-authorisation-token"] = context.data["users"][uid][
        "user_authorisation_token"
    ]

    response = request.hugosave_get_request(
        path=ah.credit_card_urls["show_card_pin"].replace("{card-id}", card_id),
        headers=headers,
    )

    assert check_status_distribute(response, 200), (
        f"Expected 200 for SHOW_CARD_PIN, received: {response}"
    )

    assert "data" in response, f"Missing data in response: {response}"

    data = response["data"]

    assert "encryptedPin" in data, (
        f"Expected encryptedPin in response, received: {data}"
    )
    assert "key" in data, (
        f"Expected key in response, received: {data}"
    )


    # We Can Store PIN if needed for further steps
    # context.data["users"][uid]["card_pin"] = response["data"]["pin"]

@Step("I check the available credits for user ([^']*) and available credit should be ([^']*)")
def check_available_credit(context, uid, checks):
    request = context.request

    credit_account_id = context.data["users"][uid]["credit_accounts"][0]["creditAccountId"]

    amount = 0.0
    precision = ""
    amount_checks_list = checks.split(" ")

    for item in amount_checks_list:
        try:
            amount = float(item)
        except ValueError:
            if item == "approx" or item == "exact":
                precision = item

    @retry(AssertionError, tries=40, delay=20, logger=None)
    def retry_for_available_credit():
        response = request.hugosave_get_request(
            path=ah.cms_urls["balance"].replace("{account-id}", credit_account_id),
            headers=ah.get_user_header(context, uid),
        )

        if check_status_distribute(response, 200):
            available_credit_balance = response["data"]["availableCredit"]

            if precision == "approx":
                assert amount - 1 <= available_credit_balance <= amount + 1, \
                    f"Approx check failed! Expected ~{amount}, but got {available_credit_balance}"
            elif precision == "exact":
                assert available_credit_balance == amount, \
                    f"Exact check failed! Expected {amount}, but got {available_credit_balance}"
            else:
                assert available_credit_balance == amount, \
                    f"Comparison failed! Got {available_credit_balance}"

    retry_for_available_credit()

@Step("I get card transaction channel limits for user ([^']*) and expect status code ([^']*)")
def get_card_txn_channel_limits(context, uid: str, expected_status_code: str):
    request = context.request
    card_id = context.data["users"][uid]["card_id"]

    response = request.hugosave_get_request(
        path=ah.card_urls["get_limits"].replace("{card-id}", card_id),
        headers=ah.get_user_header(context, uid),
    )

    assert check_status_distribute(response, expected_status_code), (
        f"Expected {expected_status_code}, received: {response}"
    )

    assert "data" in response, f"Missing data in response: {response}"

    context.data["users"][uid]["credit_accounts"] = (
        context.data["users"][uid]["credit_accounts"]
        if isinstance(context.data["users"][uid].get("credit_accounts"), dict)
        else {}
    )
    context.data["users"][uid]["credit_accounts"]["channelDetails"] = response["data"]["channelDetails"]

@Step("I update card limit for user ([^']*) and expect status code ([^']*)")
def update_card_limit(context, uid: str, expected_status_code: str):
    request = context.request
    card_id = context.data["users"][uid]["card_id"]

    row = context.table.rows[0]
    requested_limit_name = row["limit_id"]
    new_value = int(row["value"])

    channel_details = context.data["users"][uid]["credit_accounts"]["channelDetails"]

    resolved_limit_id = None
    for channel in channel_details:
        if requested_limit_name.startswith(channel["channel"]):
            resolved_limit_id = channel["cardLimitDetails"]["limitId"]
            break

    assert resolved_limit_id, f"Unable to resolve limitId for {requested_limit_name}"


    payload = {
        "limitId": resolved_limit_id,
        "value": new_value,
    }

    headers = ah.get_user_header(context, uid)
    headers["x-final-user-authorisation-token"] = context.data["users"][uid][
        "user_authorisation_token"
    ]

    response = request.hugosave_put_request(
        path=ah.card_urls["update_limits"].replace("{card-id}", card_id),
        data=payload,
        headers=headers,
    )

    assert check_status_distribute(response, expected_status_code), (
        f"Expected {expected_status_code}, received: {response}"
    )

@Step("I get limit history for card for user ([^']*) and expect status code ([^']*)")
def get_limit_history(context, uid: str, expected_status_code: str):
    request = context.request
    card_id = context.data["users"][uid]["card_id"]

    row = context.table.rows[0]
    requested_limit_name = row["limit_id"]

    channel_details = context.data["users"][uid]["credit_accounts"]["channelDetails"]

    resolved_limit_id = None
    for channel in channel_details:
        if requested_limit_name.startswith(channel["channel"]):
            resolved_limit_id = channel["cardLimitDetails"]["limitId"]
            break

    assert resolved_limit_id, f"Unable to resolve limitId for {requested_limit_name}"


    response = request.hugosave_get_request(
        path=ah.card_urls["get_limit_history"].replace("{card-id}", card_id),
        params={"limit-id": resolved_limit_id},
        headers=ah.get_user_header(context, uid),
    )

    assert check_status_distribute(response, expected_status_code), (
        f"Expected {expected_status_code}, received: {response}"
    )

    assert "data" in response, f"Missing data in response: {response}"

    context.data["users"][uid]["credit_accounts"] = (
        context.data["users"][uid]["credit_accounts"]
        if isinstance(context.data["users"][uid].get("credit_accounts"), dict)
        else {}
    )
    context.data["users"][uid]["credit_accounts"]["limitHistory"] = response["data"]["limitHistory"]

@Step("I check status of ([^']*) channel ([^']*) for ([^']*) and it should be ([^']*)")
def check_channel_status(context , card_type:str, channel_type:str, uid : str, status : str) :
    request = context.request
    user_cards = context.data["users"][uid]["cards"][0]
    card_id = ""
    if (user_cards["cardLabel"] == card_type):
        card_id = user_cards["cardId"]

    if status.strip() == "DISABLED":
        expected_status = False
    elif status.strip() == "ENABLED":
        expected_status = True

    if channel_type == "E_COMMERCE":
        to_check = "ecomStatus"
    elif channel_type == "POS":
        to_check = "posStatus"
    else:
        to_check = "atmStatus"

    @retry(AssertionError, tries=10, delay=15, logger=None)
    def retry_check_limit():
        response = request.hugosave_get_request(
            headers = ah.get_user_header(context,uid),
            path = ah.card_urls["get_limits"].replace("{card-id}",card_id)
        )

        if check_status_distribute(response,200):
            saved_status=None
            channels = response.get("data", {}).get("channelDetails", [])

            for channel in channels:
                if channel.get("channel") == channel_type:
                    saved_status = channel.get("channelStatus", {}).get(to_check, {}).get("enabled")
                    break

            saved_status = saved_status if isinstance(saved_status, bool) else str(saved_status).lower() == "true"

            if saved_status is None:
                raise AssertionError(f"Channel '{channel_type}' not found or 'enabled' missing. available: {[c.get('channel') for c in channels]}")

            assert saved_status == expected_status, f"Channel Status Not Updated\n, received response: {response}"

    retry_check_limit()

@Step("I update credit limit for user ([^']*) and expect a status code of ([^']*)")
def update_credit_limit(context, uid, expected_status_code):
    request = context.request

    row = context.table.rows[0]
    final_requested_limit = float(row["credit_limit"])

    credit_accounts = context.data["users"][uid]["credit_accounts"]
    credit_account = credit_accounts[0]

    account_id = credit_account["creditAccountId"]
    # current_limit = float(credit_account["approvedLimit"])

    # limit_to_increase = final_requested_limit - current_limit
    # assert limit_to_increase > 0, "Final credit limit must be greater than current limit"

    # # fetch lien factor from constants
    # lien_factor = context.data["credit_card_constants"]["lien_factor"]
    #
    # # calculate required lien amount
    # required_lien_amount = limit_to_increase * lien_factor

    payload = {
        "approvedLimit": final_requested_limit
    }

    headers = ah.get_user_header(context, uid)
    headers["x-final-user-authorisation-token"] = context.data["users"][uid][
        "user_authorisation_token"
    ]

    response = request.hugosave_put_request(
        path=ah.credit_card_urls["update_credit_limit"].replace(
            "{account-id}", account_id
        ),
        data=payload,
        headers=headers,
    )

    assert check_status_distribute(response, expected_status_code), (
        f"Expected {expected_status_code}, received: {response}"
    )

    # We can store for later use
    # context.data["users"][uid]["credit_limit_update_attempt"] = {
    #     "current_limit": current_limit,
    #     "final_requested_limit": final_requested_limit,
    #     "limit_to_increase": limit_to_increase,
    #     "required_lien_amount": required_lien_amount,
    # }

@Step("I get cash advance limit for credit account of user ([^']*) and expect a status code of ([^']*)")
def get_cash_advance_limit(context, uid, expected_status_code):
    request = context.request

    credit_accounts = context.data["users"][uid]["credit_accounts"]
    credit_account = credit_accounts[0]
    account_id = credit_account["creditAccountId"]

    response = request.hugosave_get_request(
        path=ah.credit_card_urls["get_cash_advance_limit"].replace(
            "{account-id}", account_id
        ),
        headers=ah.get_user_header(context, uid),
    )

    assert check_status_distribute(response, expected_status_code), (
        f"Expected {expected_status_code}, received: {response}"
    )

    assert "data" in response, f"Missing data in response: {response}"

    context.data["users"][uid]["cash_advance_limit"] = response["data"]


@Step("I validate cash advance eligibility for user ([^']*)")
def validate_cash_advance_eligibility(context, uid):
    row = context.table.rows[0]
    requested_amount = float(row["cash_advance_amount"])

    limit_data = context.data["users"][uid]["cash_advance_limit"]

    available_limit = float(
        limit_data.get("availableLimit", limit_data.get("maxLimit"))
    )

    assert requested_amount <= available_limit, (
        f"Requested cash advance {requested_amount} exceeds available limit {available_limit}"
    )

    # print("--------context structure-------------", context.data)


@Step("I request cash advance for credit account of user ([^']*) and expect a status code of ([^']*)")
def request_cash_advance(context, uid, expected_status_code):
    request = context.request

    row = context.table.rows[0]
    requested_amount = float(row["cash_advance_amount"])

    credit_accounts = context.data["users"][uid]["credit_accounts"]
    credit_account = credit_accounts[0]
    account_id = credit_account["creditAccountId"]

    default_cash_wallet_id = context.data["users"][uid]["cashBalances"][0]["cashWalletId"]

    payload = {
        "amount": requested_amount,
        "cashWalletId": default_cash_wallet_id,
    }

    headers = ah.get_user_header(context, uid)
    headers["x-final-user-authorisation-token"] = context.data["users"][uid][
        "user_authorisation_token"
    ]

    response = request.hugosave_post_request(
        path=ah.credit_card_urls["request_cash_advance"].replace(
            "{account-id}", account_id
        ),
        data=payload,
        headers=headers,
    )

    assert check_status_distribute(response, expected_status_code), (
        f"Expected {expected_status_code}, received: {response}"
    )


################################## Temporary files just for testing ################################################

@Step("I print the current test context")
def print_context(context):
    import pprint

    print("\n========== CONTEXT DEBUG ==========")
    pprint.pprint(context.data)
    print("==================================\n")


@step("I load the previous test context")
def load_context(context):
    print(context.data)

@Step("I get the user credit accounts for the user ([^']*) and expect the account status of ([^']*)")
def get_user_credit_accounts(context, uid, expected_status):
    request = context.request

    response = request.hugosave_get_request(
        path=ah.user_profile_urls["credit-account-list"],
        headers=ah.get_user_header(context, uid),
    )

    if check_status_distribute(response, 200):

        assert "data" in response, f"Expected data in response, got: {response}"

        assert "creditAccounts" in response["data"], (
            f"Expected creditAccounts in response, got: {response['data']}"
        )

        credit_accounts = response["data"]["creditAccounts"]

        context.data["users"][uid]["credit_accounts"] = credit_accounts

        active_credit_account = None

        for account in credit_accounts:
            if account.get("accountStatus") == expected_status:
                active_credit_account = account
                break

        assert active_credit_account is not None, (
            f"No credit account found with status {expected_status}"
        )

        context.data["users"][uid]["credit_account_id"] = active_credit_account["accountId"]

########################################################################################