import random

from behave import *
from hugoutils.utilities.dataclass_util import DataClassParser
from retry import retry

import tests.api.distribute.app_helper as ah
from tests.api.distribute.app.hugosave_sg.app_dataclass import CreatePayPaymentsScheduleDTO, WeekDay, \
    SubmitOTPDTO
from tests.api.distribute.app.hugosave_sg.map_schedule_steps import get_schedule_payee_payments_data
from tests.util.common_util import check_status_distribute

use_step_matcher("re")


@Step(
    "I add the wallet with product code ([^']*) of user ([^']*) to user ([^']*) as payee ([^']*) with ([^']*) and expect a status code of ([^']*) and a status of ([^']*)"
)
def add_payee(
    context,
    product_type: str,
    payee_profile_identifier,
    uid: str,
    payee_identifier: str,
    case: str,
    expected_status_code,
    expected_status
):
    request = context.request
    payee_details = context.data["users"][payee_profile_identifier][
        "user_details_response"
    ]

    cash_wallet_id = ah.get_cash_wallet_id(context, payee_profile_identifier)

    response = request.hugosave_get_request(
        path=ah.cash_urls["cash-wallet-details"].replace(
            "{cash-wallet-id}", cash_wallet_id
        ),
        headers=ah.get_user_header(context, payee_profile_identifier),
    )
    user_prof_id = ah.get_user_profile_id(uid, context)
    context.data["users"][payee_profile_identifier]["account_number"] = response[
        "data"
    ]["accountNumber"]
    if response["data"]["iban"]:
        context.data["users"][payee_profile_identifier]["iban"] = response["data"][
            "iban"
        ]

    payee_name = payee_details["name"]
    payee_email = payee_details["email"]
    payee_acc_no = response["data"]["accountNumber"]
    payee_phone_no = payee_details["phoneNumber"]

    payee_data = ah.get_add_payee_data(
        context,
        payee_name,
        payee_profile_identifier,
        payee_acc_no,
        payee_email,
        payee_phone_no,
        case,
    )
    user_authorisation_token = context.data["users"][uid][
        "user_authorisation_token"
    ]

    headers = ah.get_user_header(context, uid)

    headers["x-final-user-authorisation-token"] = user_authorisation_token

    response = request.hugosave_post_request(
        path=ah.payee_urls["root"], data=payee_data, headers=headers
    )
    if check_status_distribute(response, expected_status_code):
        assert response["data"]["status"] == expected_status, f"Error adding payee to user : {user_prof_id}, with payee user : {payee_profile_identifier}"
        context.data["users"][uid][payee_identifier] = response["data"]


@Step("I submit otp of user ([^']*) for payee ([^']*)")
def submit_otp_success(context, uid: str, payee_identifier: str):
    request = context.request
    otp_dto_list = DataClassParser.parse_rows(
        context.table.rows, data_class=SubmitOTPDTO
    )
    payee_id = context.data["users"][uid][payee_identifier][
        "payeeId"
    ]
    for otp_dto in otp_dto_list:
        response = request.hugosave_post_request(
            ah.payee_urls["submit-otp"].replace("{payee-id}", payee_id),
            otp_dto.get_dict(),
            headers=ah.get_user_header(context, uid),
        )
        assert check_status_distribute(
            response, "200"
        ), f"Payee submit otp not success.\nReceived : {response}"


@Step(
    "I check if the wallet with product code ([^']*) of user ([^']*) is ([^']*) as payee to user ([^']*) and expect a status of ([^']*)"
)
def check_add_payee(
    context, product_type: str, payee: str, case: str, uid: str, expected_status
):
    request = context.request
    payee_identifier = payee
    payee = context.data["users"][payee_identifier]["user_details_response"]

    response = request.hugosave_get_request(
        ah.user_profile_urls["payees-list"],
        headers=ah.get_user_header(context, uid),
    )

    found = False
    payee_id = None
    payee_acc_no = context.data["users"][payee_identifier]["account_number"]
    bank_details = ""
    if context.data["customer"] == "HUGOSAVE":
        bank_details = "sgBankDetails"
    elif context.data["customer"] == "HUGOBANK":
        bank_details = "pkBankDetails"
    for payee in response["data"]["payees"]:
        if (
            payee["transferOutAccountDetails"]["codeDetails"][bank_details][
                "accountNumber"
            ]
            == payee_acc_no
        ):
            found = True
            payee_id = payee["payeeId"]
            break

    if not found:
        if case != "not_added":
            assert False, f"Payee with account number {payee_acc_no} not added"
        else:
            assert True

    elif found:
        if case == "not_added":
            for payee in response["data"]["payees"]:
                if payee["payeeId"] == payee_id:
                    assert payee["deleted"] == True, f"Payee with id {payee_acc_no} deleted successfully"

        response = request.hugosave_get_request(
            ah.payee_urls["payee"].replace("{payee-id}", payee_id),
            headers=ah.get_user_header(context, uid),
        )

        if check_status_distribute(response,200):
            assert response["data"]["transferOutAccountDetails"]["codeDetails"][bank_details]["accountNumber"]== payee_acc_no, f"Failed getting payee details for payee with account number: {payee_id}.\nReceived response: {response}"
            assert response["data"]["status"] == expected_status, f"Expected status: {expected_status}, but received response: {response}"

            context.data["users"][uid]["payees"] = (
                {}
                if context.data["users"][uid].get("payees", None)
                is None
                else context.data["users"][uid]["payees"]
            )
            context.data["users"][uid]["payees"][payee_identifier] = {
                "id": payee_id,
                "updated_data": {},
            }


@Step("I deposit ([^']*) into wallet with product code ([^']*) for user ([^ ]+) and expect a status code of ([^']*)")
def deposit_test_money(context, amount, product_type, uid, expected_status_code):
    global acc_id, response
    request = context.request
    amount_list = amount.split(" ")
    for item in amount_list:
        try:
            float(item)
            amount = item
        except ValueError:
            pass

    if product_type == "CASH_WALLET_SAVE" or product_type == "CASH_WALLET_CURRENT" or product_type == "CASH_WALLET_DIGITAL":
        acc_id = ah.get_cash_wallet_id(context, uid)
        response = request.hugosave_put_request(
            path=ah.dev_urls["deposit"],
            data={"amount": amount},
            headers=ah.get_user_header(context, uid),
        )
    elif product_type == "CASH_WALLET_SPEND":
        acc_id = ah.get_spend_account_id(context, uid)
        funding_acc_id = ah.get_cash_wallet_id(context, uid)
        url = ah.cash_urls["transfer"].replace("{cash-wallet-id}", acc_id)
        headers = ah.get_user_header(context, uid)
        response = request.hugosave_put_request(
            path=url,
            data={
                "amount": amount,
                "transfer_type": "TRANSFER_IN",
                "funding_cash_wallet_id": funding_acc_id,
            },
            headers=headers,
        )

    assert check_status_distribute(response, expected_status_code), f"The expected status code for deposit is: {expected_status_code}, but received response: {response}"


@Step(
    "I transfer ([^']*) ([^']*) from user ([^']*) to user ([^']*) with ([^']*) reference and ([^']*) payee id and expect a status code of ([^']*)"
)
def transfer_hugo_payee(context, amount, currency, from_user, to_user, reference, case, expected_status_code):
    request = context.request

    user_payees = context.data["users"][from_user]["payees"]
    payee_info = user_payees[to_user]
    payee_id = payee_info["id"]
    from_cash_wallet_id = ah.get_cash_wallet_id(context, from_user)
    amount = float(amount)

    headers = ah.get_user_header(context, from_user)

    if case == "invalid":
        payee_id = payee_id + "11"
    data = {"from_cash_wallet_id": from_cash_wallet_id, "description": "test txn"}
    if reference == "description":
        data["special_character_description"] = "@#$"

    detailed_payee_response = request.hugosave_get_request(
        path=ah.payee_urls["payee"].replace("{payee-id}", payee_id),
        headers=headers,
    )
    payee_currency = detailed_payee_response["data"]["transferOutAccountDetails"]["currency"]
    config_inquiry_data = {"payment_config": {"from_cash_wallet_id": from_cash_wallet_id, "payee_id": payee_id}, "amount": amount, "amount_qualifier": "SENDER_AMOUNT"}
    config_inquiry_response = request.hugosave_post_request(
        path = ah.user_profile_urls["config_inquiry"],
        data=config_inquiry_data,
        headers=headers,
        params={"action": "PAY_PAYEE"},
    )

    if payee_currency == currency:
        data["transaction_amount"] = amount + config_inquiry_response["data"]["fee"]["feeAmount"] + config_inquiry_response["data"]["tax"]["taxAmount"]
        data["receiver_amount"] = amount
        data["charges"] = config_inquiry_response["data"]["fee"]["feeAmount"] + config_inquiry_response["data"]["tax"]["taxAmount"]
        context.data["users"][from_user]["charges"] = data["charges"]

    elif payee_currency != currency:
        rate_exchange_response = request.hugosave_get_request(
            path=ah.cash_urls["exchange-rate"].replace("{cash-wallet-id}", from_cash_wallet_id),
            params={"to-currency": payee_currency},
            headers=headers,
        )
        token = rate_exchange_response["data"]["token"]
        data["rate"] = rate_exchange_response["data"]["rate"]
        data["token"] = token
        data["charges"] = config_inquiry_response["data"]["conversionFee"]["feeAmount"] + ((config_inquiry_response["data"]["conversionFee"]["feePercentage"] / 100) * amount) + config_inquiry_response["data"]["fee"]["feeAmount"] + config_inquiry_response["data"]["tax"]["taxAmount"]
        context.data["users"][from_user]["charges"] = data["charges"]
        if context.data["customer"] == "CDV":
            data["transaction_amount"] = amount
            data["receiver_amount"] = amount - config_inquiry_response["data"]["conversionFee"]["feeAmount"] - ((config_inquiry_response["data"]["conversionFee"]["feePercentage"] / 100) * amount) - config_inquiry_response["data"]["fee"]["feeAmount"] - config_inquiry_response["data"]["tax"]["taxAmount"]
        elif context.data["customer"] == "HUGOBANK":
            data["transaction_amount"] = amount + config_inquiry_response["data"]["conversionFee"]["feeAmount"] + ((config_inquiry_response["data"]["conversionFee"]["feePercentage"] / 100) * amount) + config_inquiry_response["data"]["fee"]["feeAmount"] + config_inquiry_response["data"]["tax"]["taxAmount"]
            data["receiver_amount"] = amount

    user_authorisation_token = context.data["users"][from_user][
        "user_authorisation_token"
    ]
    headers = ah.get_user_header(context, from_user)
    headers["x-final-user-authorisation-token"] = user_authorisation_token

    response = request.hugosave_post_request(
        path=ah.payee_urls["pay_payee"].replace("{payee-id}", payee_id),
        data=data,
        headers=headers,
    )

    if check_status_distribute(response, expected_status_code):
        if case != "invalid":
            assert "intentId" in response["data"], f"Missing intent id in response, received response: {response}"


@Step("I delete the payee ([^']*) added to user ([^']*)")
def delete_payee(context, payee, uid):
    request = context.request

    payee_id = context.data["users"][uid]["payees"][payee]

    response = request.hugosave_delete_request(
        ah.payee_urls["payee"].replace("{payee-id}", payee_id["id"]),
        headers=ah.get_user_header(context, uid),
    )

    assert check_status_distribute(response, "200"), f"Failed to delete payee.\nReceived : {response}"


@Step(
    "I check the balance of the wallet with product code ([^']*) for user ([^']*) and the balance should be ([^']*)"
)
def step_impl(context, product_code, uid, checks):

    request = context.request
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
    def retry_for_acc_balance():
        response = request.hugosave_get_request(
            path=ah.balance_urls["balances"],
            headers=ah.get_user_header(context, uid),
        )

        b1 = ah.get_balance(response, product_code)
        # print("Context.data:-", context.data["users"])

        if check_status_distribute(response, 200):
            if precision == "approx":
                assert amount - 1 <= b1 <= amount + 1
            elif precision == "exact":
                assert b1 == amount

    retry_for_acc_balance()


@Step(
    "I check the balance of the wallet with product code ([^']*) for user ([^']*) and the balance should have decreased to ([^']*) ([^']*) plus the fees"
)
def step_impl(context, product_code, uid, amount, currency):

    request = context.request
    amount = float(amount)
    charges = context.data["users"][uid]["charges"]
    total_amount = amount - charges

    @retry(AssertionError, tries=40, delay=20, logger=None)
    def retry_for_acc_balance():
        response = request.hugosave_get_request(
            path=ah.balance_urls["balances"],
            headers=ah.get_user_header(context, uid),
        )
        balance = ah.get_balance(response, product_code)
        if check_status_distribute(response, 200):
            assert balance == total_amount, f"Expected balance: {total_amount}, but received response: {response}"

    retry_for_acc_balance()


@Step(
    "I transfer ([^']*) ([^']*) from user ([^']*) to user ([^']*) using ([^']*) QR code"
)
def transfer_hugo_payee(context, amount, currency, from_user, to_user, mode):
    request = context.request
    if mode == "Dynamic":
        amount = context.data["users"][to_user]["inquiry_info"]["amount"]
    submit_acc_details = context.data["users"][to_user]["inquiry_info"][
        "transfer_out_account_details"
    ]

    data = {
        "amount": amount,
        "description": "test txn",
        "transfer_out_account_details": submit_acc_details,
    }

    user_authorisation_token = context.data["users"][from_user][
        "user_authorisation_token"
    ]
    headers = ah.get_user_header(context, from_user)
    headers["x-final-user-authorisation-token"] = user_authorisation_token

    response = request.hugosave_post_request(
        ah.payee_urls["qr_payment"],
        data=data,
        headers=headers,
    )

    if check_status_distribute(response, "200"):
        assert "intentId" in response["data"], f"Expected intent id in response, but received response: {response}"


@Step("I edit the payee ([^']*) details for the user ([^']*) and expect a status code of ([^']*)")
def step_impl(context, payee_identifier, uid, expected_status_code):
    request = context.request

    user_payees = context.data["users"][uid]["payees"]
    payee_info = user_payees[payee_identifier]  # This is now a dict

    updated_data = {
        "nick_name": "Andrew Huts",
        "email": "test@gmail.com",
        "phone_number": "+924711402",
        "is_favorite": True,
    }

    payee_info["updated_data"] = updated_data

    response = request.hugosave_put_request(
        path=ah.payee_urls["payee"].replace("{payee-id}", payee_info["id"]),
        data=updated_data,
        headers=ah.get_user_header(context, uid),
    )

    assert check_status_distribute(response, expected_status_code), f"The expected status code is: {expected_status_code}, but received the response: {response}"


@Step("I check if the payee ([^']*) details are updated for the user ([^']*) and expect a status of ([^']*)")
def step_impl(context, payee_identifier, uid, expected_status):
    request = context.request

    user_payees = context.data["users"][uid]["payees"]
    payee_info = user_payees[payee_identifier]  # dict

    expected_updated_data = payee_info["updated_data"]

    response = request.hugosave_get_request(
        path=ah.payee_urls["payee"].replace("{payee-id}", payee_info["id"]),
        headers=ah.get_user_header(context, uid),
    )

    if check_status_distribute(response, "200"):

        assert response["data"]["status"] == expected_status, f"The expected status is: {expected_status}, but received the response: {response}"

        actual_data = {
            "nick_name": response["data"]["nickName"],
            "email": response["data"]["email"],
            "phone_number": response["data"]["phoneNumber"],
            "is_favorite": response["data"]["isFavorite"],
        }

        assert actual_data == expected_updated_data, (
            f"Payee details mismatch for {payee_identifier}. "
            f"Expected: {expected_updated_data}, Actual: {actual_data}"
        )


@Step("I add the user ([^']*) as External Payee ([^']*) for the user ([^']*) with External Account Number in the ([^']*) and expect a status of ([^']*)")
def step_impl(context, payee_profile_identifier, payee_identifier,user_profile_identifier, bank_name, expected_status):
    request = context.request
    #inquiry
    account_details = ah.get_pk_account_details(context, bank_name)
    data = {
        "inquiry": {
            "country": "PAK",
            "code_details": {
                "pk_account": account_details
            },
        }
    }
    response = request.hugosave_post_request(
        ah.payee_urls["inquiry"],
        headers=ah.get_user_header(context, user_profile_identifier),
        data=data,
    )

    #add payee
    payee_data = {
        "transfer_out_account_details": response["data"]["transferOutAccountDetails"]
    }
    user_authorisation_token = context.data["users"][user_profile_identifier][
        "user_authorisation_token"
    ]

    headers = ah.get_user_header(context, user_profile_identifier)

    headers["x-final-user-authorisation-token"] = user_authorisation_token

    response = request.hugosave_post_request(
        path=ah.payee_urls["root"], data=payee_data, headers=headers
    )

    if check_status_distribute(response, "200"):
        assert response["data"]["status"] == expected_status, f"Error adding payee to user : {user_profile_identifier}, with payee user : {payee_identifier['user_profile_id']}"
        context.data["users"][user_profile_identifier][payee_identifier] = response["data"]


@Step("I check if the user ([^']*) is added as a External Payee ([^']*) for the user ([^']*) and expect a status of ([^']*)")
def step_impl(context, payee_profile_identifier, payee_identifier, uid, expected_status):
    request = context.request
    payee_id = context.data["users"][uid][payee_identifier]["payeeId"]

    @retry(AssertionError, tries=15, delay=10, logger=None)
    def retry_for_payee_status():
        response = request.hugosave_get_request(
            path=ah.user_profile_urls["payees-list"],
            headers=ah.get_user_header(context, uid),
        )

        assert check_status_distribute(response, 200), f"Failed to get payees list. Response: {response}"

        payees_list = response.get("data", {}).get("payees", [])
        found_payee = None
        for p in payees_list:
            if p["payeeId"] == payee_id:
                found_payee = p
                break

        assert found_payee, f"Payee with ID '{payee_id}' was not found in the user's payees list."
        assert found_payee["status"] == expected_status, f"Expected status: {expected_status}, but received status: {found_payee['status']} for payee {payee_id}"

    retry_for_payee_status()

    # If retry is successful, update the context
    context.data["users"][uid].setdefault("payees", {})
    context.data["users"][uid]["payees"][payee_profile_identifier] = {
        "id": payee_id,
        "updated_data": {},
    }


@Step("I get the user cash wallets for the user ([^']*) and expect the account status of ([^']*)")
def get_user_cash_accounts(context, uid, expected_status):
    request = context.request
    response = request.hugosave_get_request(
        path=ah.user_profile_urls["get_all_cash_wallets"],
        headers=ah.get_user_header(context, uid)
    )

    if check_status_distribute(response, 200):
        for cash_wallet in response["data"]["userCashWallets"]:
            assert cash_wallet["accountStatus"] == expected_status, f"The expected status is: {expected_status}, but received the response: {response}"
            context.data["users"][uid]["user_cash_wallets"] = response["data"]

@Step("I create a schedule for Payee Payments ([^']*) and expect status ([^']*)")
def step_impl(context, payee_identifier, expected_status_code):
    request = context.request
    schedule_payee_payments_dto = DataClassParser.parse_row(
        context.table.rows[0], data_class=CreatePayPaymentsScheduleDTO
    )
    user_profile_identifier = schedule_payee_payments_dto.user_profile_identifier
    payee_id = ah.get_payee_id(context, payee_identifier, user_profile_identifier)
    amount = schedule_payee_payments_dto.amount
    schedule_payee_payments_dto.schedule_pay_payee = get_schedule_payee_payments_data(
        context, payee_id, amount
    )

    schedule_payee_payments_dto.target_week = 0
    schedule_payee_payments_dto.frequency = schedule_payee_payments_dto.frequency
    if schedule_payee_payments_dto.frequency == "MONTHLY":
        schedule_payee_payments_dto.target_weekdays = list(WeekDay)[random.randrange(1, 6)].name
        schedule_payee_payments_dto.target_week = random.randrange(1, 5)
    elif schedule_payee_payments_dto.frequency == "WEEKLY":
        schedule_payee_payments_dto.target_weekdays = list(WeekDay)[random.randrange(1, 6)].name
    response = request.hugosave_post_request(
        path = ah.map_schedule_urls["root"],
        data = schedule_payee_payments_dto.get_dict(),
        headers = ah.get_user_header(context, user_profile_identifier),
    )

    assert check_status_distribute(response, expected_status_code) and "scheduleId" in response["data"], f"Failed to create a schedule for payee payments schedule.\nReceived response: {response}"
    context.data[schedule_payee_payments_dto.schedule_identifier] = response["data"]


@Step("I check if user ([^']*) is in favourites of ([^']*)")
def check_payee(context, payee_identifier,uid):
    request = context.request

    response = request.hugosave_get_request(
        ah.user_profile_urls["payees-list"],
        headers=ah.get_user_header(context, uid),
    )

    if check_status_distribute(response, "200"):
        for payee in response["data"]["payees"]:
            assert payee["isFavorite"] == True, f"Payee is not added a favourite, Received response: {response}"

@Step(
    "I add the user ([^']*) as External Payee ([^']*) for the user ([^']*) with the Country ([^']*) and expect a status code of ([^']*) and status of ([^']*)")

def step_impl(context, payee_profile_identifier, payee_identifier, user_profile_identifier, country, status_code, expected_status):
    request = context.request

    currencies_response = request.hugosave_get_request(
        ah.payee_urls["currency-config"],
        headers=ah.get_user_header(context, user_profile_identifier),
    )

    currency = ""
    for item in currencies_response["data"]["currenciesWithSupportedCountries"]:
        for supported_country in item["supportedCountriesInfo"]:
            if supported_country["code"] == country:
                currency = item["currencyInfo"]["code"]
                break
        if currency:
            break

    params = {
        "country": country,
        "currency": currency,
    }
    payee_config_response = request.hugosave_get_request(
        ah.payee_urls["payee-config"],
        params=params,
        headers=ah.get_user_header(context, user_profile_identifier),
    )

    bank_field_names = ah.extract_bank_details_only_field_names(payee_config_response)

    payee_config_details = ah.generate_random_test_data(bank_field_names, country)

    payee_config_details.update({
        "address_line_1": f"{random.randint(100, 999)} {ah.generate_random_word(7)} Street",
        "city": ah.generate_random_word(6),
        "local_code": ah.generate_random_number_string(5),
        "state": ah.generate_random_word(4),
        'country': country,
        'currency': currency,
        'payee_country_code': country,
        'icon': ""
    })

    payee_data = {
        "payee_config_details": payee_config_details
    }

    user_authorisation_token = context.data["users"][user_profile_identifier][
        "user_authorisation_token"
    ]

    headers = ah.get_user_header(context, user_profile_identifier)
    headers["x-final-user-authorisation-token"] = user_authorisation_token

    response = request.hugosave_post_request(
        path=ah.payee_urls["root"], data=payee_data, headers=headers
    )

    if check_status_distribute(response, status_code):
        if status_code != "200":
            assert response["headers"]["message"] == expected_status, f"Able to add more payees than the limit for the user : {user_profile_identifier}"
        else:
            assert response["data"]["status"] == expected_status, f"Error adding payee to user : {user_profile_identifier}, with payee user : {payee_identifier['user_profile_id']}"
            context.data["users"][user_profile_identifier][payee_identifier] = response["data"]


@Step("I Restore the Payee ([^']*) for the user ([^']*) and check if the payee is restored successfully")
def step_impl(context, payee_profile_identifier, user_profile_identifier):
    request = context.request

    payee_id = context.data["users"][user_profile_identifier]["payees"][payee_profile_identifier]

    response = request.hugosave_post_request(
        ah.payee_urls["restore-payee"].replace("{payee-id}",payee_id["id"]),
        headers=ah.get_user_header(context, user_profile_identifier),
    )

    assert check_status_distribute(response, "200"), f"Failed to Restore payee.\nReceived : {response}"


@step("I check if the payee ([^']*) is removed for the user ([^']*)")
def step_impl(context, payee_profile_identifier, user_profile_identifier):
    request = context.request

    try:
        payee_id = context.data["users"][user_profile_identifier]["payees"][payee_profile_identifier]
    except KeyError as e:
        raise AssertionError(f"Could not find required context data for payee or user: {e}")

    response = request.hugosave_get_request(
        ah.user_profile_urls["payees-list"],
        headers=ah.get_user_header(context, user_profile_identifier),
    )

    assert check_status_distribute(response, 200), \
        f"Failed to get payees list. Response status not 200. Response: {response}"

    payees_list = response.get("data", {}).get("payees", [])

    deleted_payee_found = False

    for payee in payees_list:
        if payee.get("payeeId") == payee_id["id"]:
            # Found the payee, now check its 'deleted' status
            if payee.get("deleted") == True:
                deleted_payee_found = True
            break

    assert deleted_payee_found, \
        f"Payee with ID {payee_id} was either not found in the list, or its 'deleted' flag was not set to 'true'."

