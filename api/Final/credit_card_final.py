import pprint

from behave import *
from retry import retry

use_step_matcher("re")

from hugoutils.utilities.dataclass_util import DataClassParser
from api.distribute.steps.app_dataclass import *
import tests.api.distribute.app_helper as ah
from tests.util.common_util import check_status_distribute


@Step("User fetch credit card constants for ([^']*)")
def fetch_credit_card_constants(context, customer):

    request = context.request

    if "users" not in context.data or not context.data["users"]:
        raise Exception("Stopping the test: No users found in context! CHECK 'Background' step fail?")

    # uid = list(context.data["users"].keys())[0]
    uid = None

    for user_key in context.data["users"]:
        if user_key == "UID1":
            uid = user_key
            break

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


@step("Validate credit card eligibility using balance of the wallet with product code ([^']*) for user ([^']*)")
def validate_eligibility(context,product_code, uid):

    # requested_credit_limit = float(context.table[0]["credit_limit"])
    # for row in context.table:
    #     requested_credit_limit = float(row["credit_limit"])
    order_card_dto_list = DataClassParser.parse_rows(
        context.table, OrderCreditCardDTO
    )

    for order_card_dto in order_card_dto_list:
        requested_credit_limit = order_card_dto.get_credit_limit()


    # if "credit_card_constants" not in context.data:
    #     raise Exception("Error: Credit Card constants missing. Check if you run the 'fetch constants' step")

    cc_constants = context.data["credit_card_constants"]
    min_limit = float(cc_constants["min_credit_limit"])
    max_limit = float(cc_constants["max_credit_limit"])
    lien_factor = float(cc_constants["lien_factor"])



    if not (min_limit <= requested_credit_limit <= max_limit):
        assert False, (
            f"FAIL: Credit limit {requested_credit_limit} is out of bounds! "
            f"Must be between {min_limit} and {max_limit}."
        )


    required_lien_amount = requested_credit_limit * lien_factor

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

    if current_balance < required_lien_amount:
        assert False, (
            f"FAIL: Insufficient Funds! "
            f"Balance ({current_balance}) is less than required Lien ({required_lien_amount})"
        )



@Step("User order a ([^']*) as ([^']*) for ([^']*) with card name as ([^']*) and expect a status code of ([^']*) and expect a card status of ([^']*)")
def order_credit_card(context,card_type: str,card_tag: str,uid: str,card_name: str,expected_status_code: str,expected_status):
    request = context.request
    order_card_req = {}
    # if context.table:
    #     if "credit_limit" in context.table.headings:
    #         credit_limit = int(context.table.rows[0]["credit_limit"])

    order_card_dto_list = DataClassParser.parse_rows(
        context.table, OrderCreditCardDTO
    )

    for order_card_dto in order_card_dto_list:
        credit_limit = order_card_dto.get_credit_limit()

    product_code = "CARD_PRODUCT_PHYSICAL_SECURED_CREDIT_CARD_VISA"

    order_card_req.update({
        "product_code": product_code,
        "funding_details":
            {
                "approved_limit": credit_limit,
                "earn_interest_on_lien": True
            }
    })

    path = ah.card_urls["order_card"]

    if card_name == "random_valid_choice":
        response = request.hugosave_get_request(
            path=ah.user_profile_urls["card_name"],
            headers=ah.get_user_header(context, uid),
        )
        if check_status_distribute(response, "200"):
            assert "names" in response["data"], f"Expected names in response, but received response: {response}"
            order_card_req["name_on_card"] = response["data"]["names"][0]
    elif card_name != "empty":
        order_card_req["name_on_card"] = card_name

    headers = ah.get_user_header(context, uid)
    if "user_authorisation_token" in context.data["users"][uid]:
        headers["x-final-user-authorisation-token"] = context.data["users"][
            uid
        ]["user_authorisation_token"]
    response = request.hugosave_post_request(
        path=path,
        headers=headers,
        data=order_card_req,
    )

    if check_status_distribute(response, expected_status_code):
        if "data" in response:
            assert expected_status == response["data"]["cardStatus"], f"Expected status: {expected_status}, but received response: {response}"
            context.data["cardOrderStatus"] = response["data"]
            context.data["users"][uid]["credit_card"]=response["data"]
            context.data["users"][uid][card_tag] = {}
            context.data["users"][uid][card_tag]["card_id"] = response["data"]["cardId"]
            context.data["users"][uid][card_tag]["cardAccountId"] = response["data"]["cardAccountId"]

        else:
            assert expected_status == response["headers"]["message"], f"Expected status: {expected_status}, but received response: {response}"


@Step("User ([^']*) view the credit card PIN and expect the PIN to be returned successfully")
def view_credit_card_pin(context, uid: str):
    request = context.request

    card_id = context.data["users"][uid]["credit_card"]["cardId"]

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


@Step("Check the available credits for user ([^']*) and available credit should be ([^']*)")
def check_available_credit(context, uid, checks):
    request = context.request

    # credit_account_id = context.data["users"][uid]["credit_accounts"][0]["creditAccountId"]
    credit_account_id = ah.get_credit_account_id(context, uid)

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


@Step("User ([^']*) get card transaction channel limits and expect status code ([^']*)")
def get_card_txn_channel_limits(context, uid: str, expected_status_code: str):
    request = context.request
    card_id = context.data["users"][uid]["credit_card"]["cardId"]

    response = request.hugosave_get_request(
        path=ah.card_urls["get_limits"].replace("{card-id}", card_id),
        headers=ah.get_user_header(context, uid),
    )

    assert check_status_distribute(response, expected_status_code), (
        f"Expected {expected_status_code}, received: {response}"
    )

    assert "data" in response, f"Missing data in response: {response}"

    # credit_accounts = context.data["users"][uid].get("credit_accounts", [])
    #
    # if not isinstance(credit_accounts, list) or not credit_accounts:
    #     raise Exception("Credit accounts missing or invalid in context")
    #
    # credit_accounts[0]["channelDetails"] = response["data"]["channelDetails"]

    credit_accounts = context.data["users"][uid].get("credit_accounts", [])

    if not isinstance(credit_accounts, list) or not credit_accounts:
        raise Exception("Credit accounts missing or invalid in context")

    # target_credit_account_id = response["data"]["creditAccountId"]
    #
    # matched_account = next(
    #     (acc for acc in credit_accounts if acc["creditAccountId"] == target_credit_account_id),
    #     None
    # )
    #
    # if not matched_account:
    #     raise Exception(f"Credit account {target_credit_account_id} not found in context")
    # matched_account["channelDetails"] = response["data"]["channelDetails"]
    for account in credit_accounts:
        account["channelDetails"] = response["data"]["channelDetails"]

@Step(
    "User ([^']*) verified approved limit and it should be ([^']*)"
)
def verify_approved_limit(context, uid: str, checks: str):

    request = context.request

    amount = 0.0
    precision = ""

    parts = checks.split(" ")
    for item in parts:
        try:
            amount = float(item)
        except ValueError:
            if item in ["approx", "exact"]:
                precision = item

    @retry(AssertionError, tries=20, delay=20, logger=None)
    def retry_for_approved_limit():

        response = request.hugosave_get_request(
            path=ah.user_profile_urls["credit-account-list"],
            headers=ah.get_user_header(context, uid),
        )

        assert check_status_distribute(response, 200), (
            f"Failed to fetch credit accounts. Response: {response}"
        )

        assert "data" in response and "creditAccounts" in response["data"], (
            f"Missing creditAccounts in response: {response}"
        )

        credit_accounts = response["data"]["creditAccounts"]
        assert credit_accounts, "No credit accounts found for user"

        # approved_limit = float(credit_accounts[0]["approvedLimit"])
        credit_account_id = ah.get_credit_account_id(context, uid)
        approved_limit = None
        for account in credit_accounts:
            if account.get("creditAccountId") == credit_account_id:
                approved_limit = float(account.get("approvedLimit"))
                break
        assert approved_limit is not None, "Matching credit account not found"

        if precision == "approx":
            assert amount - 1 <= approved_limit <= amount + 1, (
                f"Approx check failed! Expected ~{amount}, got {approved_limit}"
            )
        elif precision == "exact":
            assert approved_limit == amount, (
                f"Exact check failed! Expected {amount}, got {approved_limit}"
            )
        else:
            assert approved_limit == amount, (
                f"Comparison failed! Expected {amount}, got {approved_limit}"
            )

    retry_for_approved_limit()


@Step("User ([^']*) update card channel limit and expect status code ([^']*)")
def update_card_channel_limit(context, uid: str, expected_status_code: str):
    request = context.request
    card_id = context.data["users"][uid]["credit_card"]["cardId"]

    # row = context.table.rows[0]
    # requested_limit_name = row["limit_id"]
    # new_value = int(row["value"])

    limit_dto_list = DataClassParser.parse_rows(
        context.table, UpdateCardLimitDTO
    )

    for limit_dto in limit_dto_list:
        requested_limit_name = limit_dto.get_limit_id()
        new_value = limit_dto.get_value()

    # channel_details = context.data["users"][uid]["credit_accounts"][0]["channelDetails"]
    credit_account_id = ah.get_credit_account_id(context, uid)
    channel_details = None
    for account in context.data["users"][uid]["credit_accounts"]:
        if account.get("creditAccountId") == credit_account_id:
            channel_details = account.get("channelDetails")
            break
    assert channel_details, f"Channel details not found for credit account {credit_account_id}"


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


@Step("User ([^']*) verified the updated ([^']*) limit and limit should be ([^']*)")
def verify_updated_channel_limit(context,uid: str,limit_name: str,  expected_limit: str):
    request = context.request
    expected_limit = float(expected_limit)

    card_id = context.data["users"][uid]["credit_card"]["cardId"]

    @retry(AssertionError, tries=40, delay=20, logger=None)
    def retry_verify_updated_limit():
        response = request.hugosave_get_request(
            path=ah.card_urls["get_limits"].replace("{card-id}", card_id),
            headers=ah.get_user_header(context, uid),
        )

        assert check_status_distribute(response, 200), (
            f"Failed to fetch limits. Response: {response}"
        )

        assert "data" in response and "channelDetails" in response["data"], (
            f"Missing channelDetails in response: {response}"
        )

        channel_details = response["data"]["channelDetails"]

        expected_channel = "_".join(limit_name.split("_")[:-2])

        matched = False

        for channel in channel_details:
            if channel["channel"] == expected_channel:
                limit_details = channel.get("cardLimitDetails", {})
                user_set_value = limit_details.get("userSetValue")

                assert user_set_value == expected_limit, (
                    f"{expected_channel} limit mismatch. "
                    f"Expected {expected_limit}, got {user_set_value}"
                )
                matched = True
                break

        assert matched, (
            f"No channel found for {expected_channel}. "
            f"Available channels: {[c['channel'] for c in channel_details]}"
        )
    retry_verify_updated_limit()


@Step("User ([^']*) get channel limit history for credit card and expect status code ([^']*)")
def get_channel_limit_history(context, uid: str, expected_status_code: str):
    request = context.request
    card_id = context.data["users"][uid]["credit_card"]["cardId"]

    limit_dto_list = DataClassParser.parse_rows(
        context.table, GetChannelLimitHistoryDTO
    )
    for limit_dto in limit_dto_list:
        requested_limit_name = limit_dto.get_credit_limit_history()

    # row = context.table.rows[0]
    # requested_limit_name = row["limit_id"]

    # channel_details = context.data["users"][uid]["credit_accounts"][0]["channelDetails"]
    credit_account_id = ah.get_credit_account_id(context, uid)
    channel_details = None
    for account in context.data["users"][uid]["credit_accounts"]:
        if account.get("creditAccountId") == credit_account_id:
            channel_details = account.get("channelDetails")
            break
    assert channel_details, f"Channel details not found for credit account {credit_account_id}"

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

    context.data["users"][uid]["credit_accounts"][0]["limitHistory"] = response["data"]["limitHistory"]


@Step("User ([^']*) check status of ([^']*) for channel ([^']*) and it should be ([^']*)")
def check_channel_status(context , uid : str, card_type:str, channel_type:str,  status : str) :
    request = context.request

    card_id = context.data["users"][uid]["credit_card"]["cardId"]


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


@Step("User ([^']*) update credit limit and expect a status code of ([^']*)")
def update_credit_limit(context, uid, expected_status_code):
    request = context.request

    # row = context.table.rows[0]
    # final_requested_limit = float(row["credit_limit"])

    limit_dto_list = DataClassParser.parse_rows(
        context.table, UpdateCreditLimitDTO
    )
    for limit_dto in limit_dto_list:
        final_requested_limit = limit_dto.get_updated_credit_limit()


    account_id = ah.get_credit_account_id(context, uid)
    # credit_accounts = context.data["users"][uid]["credit_accounts"]
    # credit_account = credit_accounts[0]
    #
    # account_id = credit_account["creditAccountId"]

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


@Step("User ([^']*) get cash advance limit for credit account expect a status code of ([^']*)")
def get_cash_advance_limit(context, uid, expected_status_code):
    request = context.request

    account_id = ah.get_credit_account_id(context, uid)

    # credit_accounts = context.data["users"][uid]["credit_accounts"]
    # credit_account = credit_accounts[0]
    # account_id = credit_account["creditAccountId"]


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


@Step("User ([^']*) validate cash advance eligibility")
def validate_cash_advance_eligibility(context, uid):
    # row = context.table.rows[0]
    # requested_amount = float(row["cash_advance_amount"])

    limit_dto_list = DataClassParser.parse_rows(
        context.table, CashAdvanceRequestDTO
    )
    for limit_dto in limit_dto_list:
        requested_amount = limit_dto.get_cash_advance_amount()


    limit_data = context.data["users"][uid]["cash_advance_limit"]

    available_limit = float(
        limit_data.get("availableLimit", limit_data.get("maxLimit"))
    )

    assert requested_amount <= available_limit, (
        f"Requested cash advance {requested_amount} exceeds available limit {available_limit}"
    )


@Step("User ([^']*) request cash advance for credit account and expect a status code of ([^']*)")
def request_cash_advance(context, uid, expected_status_code):
    request = context.request

    # row = context.table.rows[0]
    # requested_amount = float(row["cash_advance_amount"])
    requested_amount=None
    limit_dto_list = DataClassParser.parse_rows(
        context.table, CashAdvanceRequestDTO
    )
    for limit_dto in limit_dto_list:
        requested_amount = limit_dto.get_cash_advance_amount()


    account_id = ah.get_credit_account_id(context, uid)

    # credit_accounts = context.data["users"][uid]["credit_accounts"]
    # credit_account = credit_accounts[0]
    # account_id = credit_account["creditAccountId"]

    # default_cash_wallet_id = context.data["users"][uid]["user_cash_wallets"]["userCashWallets"][0]["cashWalletId"]
    default_cash_wallet_id = None
    wallets = context.data["users"][uid]["user_cash_wallets"]["userCashWallets"]
    for wallet in wallets:
        if wallet.get("productCode") == "CASH_WALLET_CURRENT":
            default_cash_wallet_id = wallet.get("cashWalletId")
            break
    assert default_cash_wallet_id, "CASH_WALLET_CURRENT wallet not found"

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


@Step("User ([^']*) generate credit account bill and expect status code ([^']*)")
def generate_credit_account_bill(context, uid, expected_status_code):
    request = context.request

    account_id = ah.get_credit_account_id(context, uid)

    # credit_account = context.data["users"][uid]["credit_accounts"][0]
    # account_id = credit_account["creditAccountId"]

    response = request.hugosave_post_request(
        path=ah.dev_urls["generate_credit_bills"],
        data={
            "creditAccountId": account_id
        },
        headers=ah.get_user_header(context, uid),
    )

    assert check_status_distribute(response, expected_status_code), (
        f"Expected {expected_status_code}, received: {response}"
    )

    context.data["users"][uid]["generated_credit_bill_response"] = response


@Step("User ([^']*) get the credit account bills and expect status code ([^']*)")
def get_credit_account_bills(context, uid, expected_status_code):
    request = context.request

    account_id = ah.get_credit_account_id(context, uid)

    # credit_accounts = context.data["users"][uid]["credit_accounts"]
    # credit_account = credit_accounts[0]
    # account_id = credit_account["creditAccountId"]

    response = request.hugosave_get_request(
        path=ah.credit_card_urls["get_credit_account_bills"].replace(
            "{account-id}", account_id
        ),
        headers=ah.get_user_header(context, uid),
    )

    assert check_status_distribute(response, expected_status_code), (
        f"Expected {expected_status_code}, received: {response}"
    )

    assert "data" in response, f"Missing data in response: {response}"

    context.data["users"][uid]["credit_account_bills"] = response["data"]


@Step("User ([^']*) get the latest credit account bill and expect status code ([^']*) and bill present as ([^']*)")
def get_latest_credit_account_bill(context, uid, expected_status_code, expected_bill_present):
    request = context.request

    account_id = ah.get_credit_account_id(context, uid)

    # credit_account = context.data["users"][uid]["credit_accounts"][0]
    # account_id = credit_account["creditAccountId"]

    response = request.hugosave_get_request(
        path=ah.credit_card_urls["get_credit_account_latest_bill"].replace(
            "{account-id}", account_id
        ),
        headers=ah.get_user_header(context, uid),
    )

    assert check_status_distribute(response, expected_status_code), (
        f"Expected {expected_status_code}, received: {response}"
    )

    bill_data = response.get("data")
    assert bill_data is not None, f"Missing data in response: {response}"

    expected_bill_present = expected_bill_present.lower() == "true"

    assert bill_data.get("billPresent") is expected_bill_present, (
        f"Expected billPresent {expected_bill_present}, received: {bill_data}"
    )

    context.data["users"][uid]["latest_credit_account_bill"] = bill_data


@Step("User ([^']*) pay credit account bill with amount ([^']*) and expect status code ([^']*) and intent status as ([^']*)")
def pay_credit_account_bill_with_amount(context, uid, amount, expected_status_code, expected_intent_status):
    request = context.request

    user_data = context.data["users"][uid]

    credit_account_id = ah.get_credit_account_id(context, uid)

    # credit_account = user_data["credit_accounts"][0]
    # credit_account_id = credit_account["creditAccountId"]

    # cash_wallet = user_data["user_cash_wallets"]["userCashWallets"][0]
    # cash_wallet_id = cash_wallet["cashWalletId"]
    cash_wallet_id = None
    wallets = context.data["users"][uid]["user_cash_wallets"]["userCashWallets"]
    for wallet in wallets:
        if wallet.get("productCode") == "CASH_WALLET_CURRENT":
            cash_wallet_id = wallet.get("cashWalletId")
            break
    assert cash_wallet_id, "CASH_WALLET_CURRENT wallet not found"


    payload = {
        "amount": float(amount),
        "cashWalletId": cash_wallet_id
    }

    response = request.hugosave_post_request(
        path=ah.credit_card_urls["pay_credit_account_bill"].replace(
            "{account-id}", credit_account_id
        ),
        headers=ah.get_user_header(context, uid),
        data=payload,
    )

    assert check_status_distribute(response, expected_status_code), (
        f"Expected {expected_status_code}, received: {response}"
    )

    response_data = response.get("data")
    assert response_data is not None, f"Missing data in response: {response}"

    assert response_data.get("status") == expected_intent_status, (
        f"Expected intent status {expected_intent_status}, received: {response_data}"
    )

    assert response_data.get("intentId"), (
        f"Missing intentId in response: {response_data}"
    )


@Step("User ([^']*) close credit account using settlement source ([^']*) and expect status code ([^']*)")
def close_credit_account(context, uid, settlement_source, expected_status_code):
    request = context.request

    credit_account_id = ah.get_credit_account_id(context, uid)

    # user_data = context.data["users"][uid]
    # credit_account = user_data["credit_accounts"][0]
    # credit_account_id = credit_account["creditAccountId"]


    headers = ah.get_user_header(context, uid)
    if "user_authorisation_token" in context.data["users"][uid]:
        headers["x-final-user-authorisation-token"] = context.data["users"][
            uid
        ]["user_authorisation_token"]

    response = request.hugosave_delete_request(
        path=ah.credit_card_urls["close_credit_account"].replace(
            "{account-id}", credit_account_id
        ),
        params={
            "settlement-source": settlement_source
        },
        headers=headers,
    )

    assert check_status_distribute(response, expected_status_code), (
        f"Expected {expected_status_code}, received: {response}"
    )


@Step("User ([^']*) verify credit account is closed")
def verify_credit_account_closed(context, uid: str):

    request = context.request

    # previous_accounts = context.data["users"][uid].get("credit_accounts", [])
    # assert previous_accounts, "No previous credit account stored in context"
    # credit_account_id = previous_accounts[0]["creditAccountId"]

    previous_accounts = context.data["users"][uid].get("credit_accounts", [])
    assert previous_accounts, "No previous credit account stored in context"

    credit_account_id = None
    for account in previous_accounts:
        credit_account_id = account.get("creditAccountId")
        if credit_account_id:
            break
    assert credit_account_id, "Unable to resolve creditAccountId from stored credit accounts"

    @retry(AssertionError, tries=20, delay=20, logger=None)
    def retry_verify_closure():

        response = request.hugosave_get_request(
            path=ah.user_profile_urls["credit-account-list"],
            headers=ah.get_user_header(context, uid),
        )

        assert check_status_distribute(response, 200), (
            f"Failed to fetch credit accounts. Response: {response}"
        )

        accounts = response["data"].get("creditAccounts", [])

        if not accounts:
            return

        for account in accounts:
            if account["creditAccountId"] == credit_account_id:
                status = account.get("accountStatus")
                assert status in [
                    "ACCOUNT_CLOSED",
                    "CREDIT_ACCOUNT_STATUS_CLOSED"
                ], (
                    f"Credit account not closed yet. Current status: {status}"
                )
                return
        return

    retry_verify_closure()


@Step("User ([^']*) fetch credit account list")
def fetch_credit_account_list(context, uid):
    request = context.request

    response = request.hugosave_get_request(
        path=ah.user_profile_urls["credit-account-list"],
        headers=ah.get_user_header(context, uid),
    )

    if check_status_distribute(response, 200):
        context.data["users"][uid]["credit_accounts"] = response["data"]["creditAccounts"]


@Step("Wait for credit card status as ([^']*) to activate ([^']*) card for user ([^']*)")
def get_card_status(context, card_status: str, card_type, uid: str,):
    request = context.request
    card_account_id = context.data["users"][uid]["credit_card"]["cardAccountId"]

    @retry(AssertionError, delay=30, tries=40, logger=None)
    def wait_for_card_status():
        response = request.hugosave_get_request(
            path=ah.card_urls["cards"].replace("{card-account-id}", card_account_id),
            headers=ah.get_user_header(context, uid),
        )
        if check_status_distribute(response, 200):
            if response["data"]["cards"]:
                for card in response["data"]["cards"]:
                    if card["cardType"] == card_type:
                        if card["cardId"] == context.data["users"][uid]["credit_card"]["cardId"]:
                            assert card["cardStatus"] == card_status, f"Expected card status: {card_status}, but received: {card}"
                            context.data["users"][uid]["cards"] = response["data"][
                                "cards"
                            ]
            else:
                assert False,f"Expected cards in response but received response: {response}"
    wait_for_card_status()


@Step("Store credit card replacement details for user ([^']*)")
def store_credit_card_replacement_snapshot(context, uid: str):

    user_data = context.data["users"][uid]

    credit_account_id = ah.get_credit_account_id(context, uid)

    # credit_account = user_data["credit_accounts"][0]
    # # credit_account_id = credit_account["creditAccountId"]
    # approved_limit = float(credit_account["approvedLimit"])

    credit_accounts = user_data.get("credit_accounts", [])
    assert credit_accounts, "No credit accounts found in user data"

    approved_limit = None
    for account in credit_accounts:
        if account.get("creditAccountId") == credit_account_id:
            approved_limit = float(account.get("approvedLimit"))
            break
    assert approved_limit is not None, f"Approved limit not found for credit account {credit_account_id}"

    balance_data = user_data.get("credit_account_balance")
    assert balance_data, "Credit account balance not fetched before snapshot"

    snapshot = {
        "old_card_id": user_data["credit_card"]["cardId"],
        "old_card_account_id": user_data["credit_card"]["cardAccountId"],
        "creditAccountId": credit_account_id,
        "approvedLimit": approved_limit,
        "availableCredit": float(balance_data["availableCredit"]),
        "settledAmount": float(balance_data["settledAmount"]),
        "unsettledAmount": float(balance_data["unsettledAmount"]),
    }

    context.data["users"][uid]["replace_snapshot"] = snapshot


@Step("I replace ([^']*) credit card for user ([^']*) and expect a card status of ([^']*)")
def replace_card(context, card_type: str, uid: str, expected_status: str):

    request = context.request

    old_card_id = context.data["users"][uid]["credit_card"]["cardId"]

    context.data["users"][uid]["old_card_id"] = old_card_id

    headers = ah.get_user_header(context, uid)
    headers["x-final-user-authorisation-token"] = context.data["users"][uid]["user_authorisation_token"]

    response = request.hugosave_post_request(
        path=ah.card_urls["replace_card"].replace("{card-id}", old_card_id),
        headers=headers,
        data={}
    )

    assert check_status_distribute(response, 200), f"Replace failed: {response}"

    assert response["data"]["cardStatus"] == expected_status, (
        f"Expected {expected_status}, got {response['data']['cardStatus']}"
    )

    context.data["users"][uid]["credit_card"] = {
        "cardId": response["data"]["cardId"],
        "cardAccountId": response["data"]["cardAccountId"],
        "cardStatus": response["data"]["cardStatus"],
        "cardType": response["data"]["cardType"],
        "category": response["data"]["category"],
        "nameOnCard": response["data"].get("nameOnCard"),
    }


@Step("User ([^']*) verify credit account integrity after replacement")
def verify_credit_account_integrity(context, uid: str):

    request=context.request
    user_data = context.data["users"][uid]
    snapshot = user_data["replace_snapshot"]

    # credit_account = user_data["credit_accounts"][0]
    credit_accounts = user_data.get("credit_accounts", [])
    for account in credit_accounts:
        credit_account = account
        break

    balance = user_data["credit_account_balance"]
    new_card = user_data["credit_card"]

    # 700 is charge and 15% is tax(Fixed amount)
    tax_on_replacement = 700 + (0.15 * 700)

    assert new_card["cardId"] != snapshot["old_card_id"], \
        "Card ID did not change after replacement"

    assert credit_account["creditAccountId"] == snapshot["creditAccountId"], \
        "Credit Account ID changed after replacement"

    assert float(credit_account["approvedLimit"]) == snapshot["approvedLimit"], \
        "Approved limit changed after replacement"

    @retry(AssertionError, tries=20, delay=15, logger=None)
    def retry_balance_verification():

        credit_account_id = ah.get_credit_account_id(context, uid)

        response = request.hugosave_get_request(
            path=ah.cms_urls["balance"].replace("{account-id}", credit_account_id),
            headers=ah.get_user_header(context, uid),
        )

        assert check_status_distribute(response, 200), \
            f"Failed to fetch balance: {response}"

        balance = response["data"]
        available_credit_after_rep = float(snapshot["availableCredit"]) - float(tax_on_replacement)
        assert float(balance["availableCredit"]) == float(available_credit_after_rep), \
            "Available credit changed after replacement"

        settled_amount_after_rep=float(snapshot["settledAmount"])+ float(tax_on_replacement)
        assert float(balance["settledAmount"]) == float(settled_amount_after_rep), \
            "Settled amount changed after replacement"

        assert float(balance["unsettledAmount"]) == snapshot["unsettledAmount"], \
            "Unsettled amount changed after replacement"

    retry_balance_verification()


@Step("I check old card status is ([^']*) for user ([^']*)")
def check_old_card_status(context, old_card_status, uid):
    request = context.request
    card_id = context.data["users"][uid]["old_card_id"]

    response = request.hugosave_get_request(
        path=ah.card_urls["card_details"].replace("{card-id}", card_id),
        headers=ah.get_user_header(context, uid),
    )
    if check_status_distribute(response, 200):
        assert (
                response["data"]["cardStatus"] == old_card_status
        ), f"Expected Card status: {old_card_status}\nActual Card status: {response['data']['cardStatus']}"


@Step("User ([^']*) fetch credit account balance")
def fetch_credit_account_list(context, uid):
    request = context.request
    credit_account_id = ah.get_credit_account_id(context, uid)

    # credit_account_id = context.data["users"][uid]["credit_accounts"][0]["creditAccountId"]

    response = request.hugosave_get_request(
        path=ah.cms_urls["balance"].replace("{account-id}", credit_account_id),
        headers=ah.get_user_header(context, uid),
    )

    if check_status_distribute(response, 200):
        context.data["users"][uid]["credit_account_balance"] = response["data"]



#######################Scenario outline#################################################################


@Step("User ([^']*) update ([^']*) to ([^']*) and expect status code ([^']*)")
def update_card_limit(context, uid: str, limit_id: str, limit_value: str,  expected_status_code: str):
    request = context.request
    # card_id = context.data["users"][uid]["card_id"]
    card_id = context.data["users"][uid]["credit_card"]["cardId"]
    requested_limit_name = limit_id
    new_value = int(limit_value)

    # channel_details = context.data["users"][uid]["credit_accounts"][0]["channelDetails"]

    credit_account_id = ah.get_credit_account_id(context, uid)
    channel_details = None
    for account in context.data["users"][uid]["credit_accounts"]:
        if account.get("creditAccountId") == credit_account_id:
            channel_details = account.get("channelDetails")
            break
    assert channel_details, f"Channel details not found for credit account {credit_account_id}"


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


@Step("User ([^']*) verify ([^']*) limit and it should be ([^']*)")
def verify_updated_channel_limit(context,uid: str, limit_name: str,  expected_limit: str):
    request = context.request
    expected_limit = float(expected_limit)

    card_id = context.data["users"][uid]["credit_card"]["cardId"]
    # card_id = context.data["users"][uid]["card_id"]
    response = request.hugosave_get_request(
        path=ah.card_urls["get_limits"].replace("{card-id}", card_id),
        headers=ah.get_user_header(context, uid),
    )

    assert check_status_distribute(response, 200), (
        f"Failed to fetch limits. Response: {response}"
    )

    assert "data" in response and "channelDetails" in response["data"], (
        f"Missing channelDetails in response: {response}"
    )

    channel_details = response["data"]["channelDetails"]

    expected_channel = "_".join(limit_name.split("_")[:-2])

    matched = False

    for channel in channel_details:
        if channel["channel"] == expected_channel:
            limit_details = channel.get("cardLimitDetails", {})
            user_set_value = limit_details.get("userSetValue")

            assert user_set_value == expected_limit, (
                f"{expected_channel} limit mismatch. "
                f"Expected {expected_limit}, got {user_set_value}"
            )
            matched = True
            break

    assert matched, (
        f"No channel found for {expected_channel}. "
        f"Available channels: {[c['channel'] for c in channel_details]}"
    )


@Step("User ([^']*) check available credit and it should be ([^']*)")
def check_available_credit(context, uid, expected_amount):
    request = context.request

    # credit_account_id = context.data["users"][uid]["credit_accounts"][0]["creditAccountId"]
    credit_account_id = ah.get_credit_account_id(context, uid)

    expected_amount = float(expected_amount)

    @retry(AssertionError, tries=40, delay=20, logger=None)
    def retry_for_available_credit():

        response = request.hugosave_get_request(
            path=ah.cms_urls["balance"].replace("{account-id}", credit_account_id),
            headers=ah.get_user_header(context, uid),
        )

        assert check_status_distribute(response, 200)

        available_credit_balance = float(response["data"]["availableCredit"])

        assert available_credit_balance == expected_amount, \
            f"Expected {expected_amount}, got {available_credit_balance}"

    retry_for_available_credit()


##################################################################################################
