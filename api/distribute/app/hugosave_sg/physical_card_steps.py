from behave import *
from hugoutils.utilities.dataclass_util import DataClassParser

from tests.api.distribute.app.hugosave_sg.app_dataclass import MockTransactionRequestDTO
from retry import retry
import tests.api.distribute.app_helper as ah
from tests.util.common_util import check_status_distribute

use_step_matcher("re")


@Step("I order a ([^']*) for ([^']*) with card name as ([^']*) and expect a status code of ([^']*) and expect a card status of ([^']*)")
def order_card(
    context,
    card_type: str,
    uid: str,
    card_name: str,
    expected_status_code: str,
    expected_status
):
    request = context.request
    order_card_req = {}
    if context.table:
        if "credit_limit" in context.table.headings:
            credit_limit = int(context.table.rows[0]["credit_limit"])

    if card_type == "virtual card":
        product_code = "CARD_PRODUCT_VIRTUAL_CARD_VISA"
        path = ah.card_urls["order_virtual_card"]
        card_account_id = ah.get_card_account_id(context, uid)
        order_card_req["card_account_id"] = card_account_id
    else:
        path = ah.card_urls["order_card"]
        if context.data["customer"] == "HUGOBANK":
            if card_type == "physical visa card":
                product_code = "CARD_PRODUCT_PHYSICAL_CARD_VISA"
                card_account_id = ah.get_card_account_id(context, uid)
                order_card_req["card_account_id"] = card_account_id
            elif card_type == "Physical Visa Credit Card":
                product_code = "CARD_PRODUCT_PHYSICAL_SECURED_CREDIT_CARD_VISA"
            else:
                product_code = "CARD_PRODUCT_PHYSICAL_CARD_PAYPAK",
                card_account_id = ah.get_card_account_id(context, uid)
                order_card_req["card_account_id"] = card_account_id
        elif context.data["customer"] == "HUGOSAVE":
            product_code = "CARD_PRODUCT_PHYSICAL_CARD"
            card_account_id = ah.get_card_account_id(context, uid)
            order_card_req["card_account_id"] = card_account_id
        else:
            product_code = "CARD_PRODUCT_PHYSICAL_DEBIT_CARD_VISA"

    order_card_req.update({
        "product_code": product_code,
    })

    if card_type == "virtual card":
        order_card_req.update(
            {
                "card_label": "Gold Rewards Card",
                "validity": 36,
                "issuance_fee": 25.00,
            }
        )
    elif card_type == "Physical Visa Credit Card":
        order_card_req.update(
            {
                "funding_details":
                {
                    "approved_limit": credit_limit,
                    # "approved_limit": 6000,
                    "earn_interest_on_lien": True
                }
            }
        )
    elif context.data["customer"] == "HUGOBANK":
        order_card_req["address_type"] = "HOME_ADDRESS"
    elif context.data["customer"] == "CDV":
        order_card_req["address_type"] = "CURRENT_ADDRESS"

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
            context.data["users"][uid]["card_id"] = response["data"]["cardId"]
            # -------------------------------For testing purpose-----------------
            context.data["users"][uid]["card_account_id"] = response["data"]["cardAccountId"]
            # -------------------------------------------------------------------
        else:
            assert expected_status == response["headers"]["message"], f"Expected status: {expected_status}, but received response: {response}"


@Step(
    "I wait for card status as ([^']*) to activate ([^']*) card for user ([^']*)"
)
def get_card_id(
    context,
    card_status: str,
    card_type,
    uid: str,
):
    request = context.request
    # card_account_id = ah.get_card_account_id(context, uid)
    card_account_id = context.data["users"][uid]["card_account_id"]
    # ------------------------------------------
    print("Card account id is:->",card_account_id)
    # ------------------------------------------
    @retry(AssertionError, delay=20, tries=20, logger=None)
    def wait_for_card_status():
        response = request.hugosave_get_request(
            path=ah.card_urls["cards"].replace("{card-account-id}", card_account_id),
            headers=ah.get_user_header(context, uid),
        )
        if check_status_distribute(response, 200):
            if response["data"]["cards"]:
                for card in response["data"]["cards"]:
                    if card["cardType"] == card_type:
                        if card["cardId"] == context.data["users"][uid]["card_id"]:
                            # -------------------------------
                            print("Card id is:-> ",context.data["users"][uid]["card_id"])
                            # -------------------------------
                            assert card["cardStatus"] == card_status, f"Expected card status: {card_status}, but received: {card}"
                            context.data["users"][uid]["cards"] = response["data"][
                                "cards"
                            ]
            else:
                assert False,f"Expected cards in response but received response: {response}"
    wait_for_card_status()


@Step("I check card status is ([^']*) for user ([^']*) for ([^']*) card")
def check_card_status(context, card_status, uid, card_type):
    request = context.request
    card_id = ah.get_card_id(context, uid, card_type)

    response = request.hugosave_get_request(
        path=ah.card_urls["card_details"].replace("{card-id}", card_id),
        headers=ah.get_user_header(context, uid),
    )
    if check_status_distribute(response, 200):
        assert (
            response["data"]["cardStatus"] == card_status
        ), f"Expected Card status: {card_status}, received response: {response}"
        context.data["users"][uid]["cards"] = response["data"]


@Step("I fetch secure card details for user ([^']*) for ([^']*) card")
def get_secure_card_details(context, uid, card_type):
    request = context.request
    card_id = ah.get_card_id(context, uid, card_type)

    response = request.hugosave_get_request(
        path=ah.card_urls["secure_card_details"].replace("{card-id}", card_id),
        headers=ah.get_user_header(context, uid),
    )
    if check_status_distribute(response, "200"):
        assert card_id == response["data"]["cardId"], f"Expected card Id: {card_id}, but received response: {response}"


@Step("I update the card status of the ([^']*) card to ([^']*) for user ([^']*) and expect a status code of ([^']*)")
def update_card_status(
    context, card_type, card_status_action, uid, expected_status_code
):
    request = context.request
    card_id = ah.get_card_id(context, uid, card_type)

    headers = ah.get_user_header(context,uid)
    if "user_authorisation_token" in context.data["users"][uid]:
        headers["x-final-user-authorisation-token"] = context.data["users"][uid]["user_authorisation_token"]

    response = request.hugosave_put_request(
        path=ah.card_urls["update_status"].replace("{card-id}", card_id),
        headers=headers,
        data={"card_id": card_id, "card_status_action": card_status_action},
    )
    assert check_status_distribute(response, expected_status_code), f"The expected status code is: {expected_status_code}, but received response: {response}"


@Step("Invalid card scenario, ([^']*), for user ([^']*) with status ([^']*)")
def invalid_card_cases(context, case, uid, status_code):
    request = context.request
    headers=ah.get_user_header(context, uid)

    if "user_authorisation_token" in context.data["users"][uid]:
        headers["x-final-user-authorisation-token"] = context.data["users"][uid]["user_authorisation_token"]

    if case == "activate_missing_card_id":
        activation_token = "123456789"
        response = request.hugosave_put_request(
            path=ah.card_urls["activate_card"],
            headers = headers,
            data={"card_id": None, "card_token": activation_token},
        )
        assert check_status_distribute(response, status_code), f"Expected status code: {status_code}, but received response: {response}"

    elif case == "activate_invalid_card_id":
        activation_token = "123456789"
        response = request.hugosave_put_request(
            path=ah.card_urls["activate_card"].replace("{card-id}", "abcdefgh"),
            headers=headers,
            data={"card_id": "abcdefgh", "card_token": activation_token},
        )
        assert check_status_distribute(response, status_code), f"Expected status code: {status_code}, but received response: {response}"

    elif case == "get_details_invalid_card_id":
        card_id = "abcdefgh"
        response = request.hugosave_get_request(
            path=ah.card_urls["card_details"].replace("{card-id}", card_id),
            headers=headers,
        )
        assert check_status_distribute(response, status_code), f"Expected status code: {status_code}, but received response: {response}"

    elif case == "get_secure_invalid_card_id":
        card_id = "abcdefgh"
        response = request.hugosave_get_request(
            path=ah.card_urls["secure_card_details"].replace("{card-id}", card_id),
            headers=headers,
        )
        assert check_status_distribute(response, status_code), f"Expected status code: {status_code}, but received response: {response}"

    elif case == "update_status_missing_card_id":
        response = request.hugosave_put_request(
            path=ah.card_urls["update_status"].replace("{card-id}", ""),
            headers=headers,
            data={"card_id": None, "card_status_action": "BLOCK"},
        )
        assert check_status_distribute(response, status_code), f"Expected status code: {status_code}, but received response: {response}"

    elif case == "update_status_invalid_card_id":
        response = request.hugosave_put_request(
            path=ah.card_urls["update_status"].replace("{card-id}", "abcdefgh"),
            headers=headers,
            data={"card_id": "abcdefgh", "card_status_action": "BLOCK"},
        )
        assert check_status_distribute(response, status_code), f"Expected status code: {status_code}, but received response: {response}"


@Step("I replace the ([^']*) card for user ([^']*) and expect a card status of ([^']*)")
def replace_card(context, card_type, uid, card_status):
    request = context.request
    card_id = ah.get_card_id(context, uid, card_type)

    context.data["users"][uid]["old_card_id"] = card_id

    response = request.hugosave_post_request(
        path=ah.card_urls["replace_card"].replace("{card-id}", card_id),
        data={"card-id": card_id},
        headers=ah.get_user_header(context, uid),
    )
    if check_status_distribute(response, "200"):
        assert response["data"]["cardStatus"] == card_status, f"Unexpected Card Status, Received response: {response}"
        context.data["users"][uid]["cards"] = response["data"]
        context.data["users"][uid]["card_id"] = response["data"]["cardId"]


@Step("I check old card status is ([^']*) for user ([^']*) and get new card id")
def check_old_card_status(context, old_card_status, uid):
    request = context.request
    card_id = context.data["users"][uid]["old_card_id"]

    response = request.hugosave_get_request(
        path=ah.card_urls["card_details"].replace("{card-id}", card_id),
        headers=ah.get_user_header(context, uid),
    )
    if check_status_distribute(response, "200"):
        assert (
            response["data"]["cardStatus"] == old_card_status
        ), f"Expected Card status: {old_card_status}\nActual Card status: {response['data']['cardStatus']}"


@Step("I create below transaction for ([^']*) card for user profile id and expect a status code of ([^']*)")
def create_transaction_auth_success(context, card_type, expected_status_code):
    request = context.request
    card_request_dto_list = DataClassParser.parse_rows(
        context.table, MockTransactionRequestDTO
    )

    for card_request_dto in card_request_dto_list:
        card_id = ah.get_card_id(context, card_request_dto.user_profile_identifier, card_type)

        # ----------------just for testing---------------------------
        print("-----------------card ID is:----------------",card_id)
        # -----------------------------------------------------------

        @retry(AssertionError, tries=40, delay=15, logger=None)
        def retry_for_transaction_creation_success():
            response = request.hugosave_post_request(
                path=ah.dev_urls["mock_card_transaction"].replace("{card-id}", card_id),
                data=card_request_dto.get_dict(),
                headers=ah.get_user_header(
                    context, card_request_dto.user_profile_identifier,
                ),
            )

            assert (
                    response["headers"]["statusCode"] == expected_status_code
            ), f"Expected transaction success: {expected_status_code}.\nReceived : {response}"
        retry_for_transaction_creation_success()


@Step(
    "I enable auto-top-up of ([^']*) SGD for user ([^']*) with trigger amount ([^']*) SGD to ([^']*) account with ([^']*)"
)
def enable_auto_top_up(
    context, top_up_amount, uid, top_up_trigger_amount,product_code, id_type
):
    request = context.request
    user_data = context.data["users"][uid]

    cash_wallet_id = ah.get_cash_wallet_id_by_product_code(context,uid,product_code)

    is_external = False
    if product_code in ("CASH_WALLET_SAVE","CASH_WALLET_CURRENT"):
        is_external = True
    else:
        is_external = False

    data = {
        "top_up_trigger_amount": top_up_trigger_amount,
        "auto_top_up_enabled": True,
        "top_up_amount": top_up_amount,
        "is_external": is_external,
    }

    if id_type == "Cash Wallet ID":
        data["cash_wallet_id"] = cash_wallet_id
    else:
        if "Mandate-" in id_type:
            mandate_key = id_type.split('-')[1]
        else:
            mandate_key = id_type
        mandate_id = user_data["mandates"][mandate_key]["mandateId"]
        data["mandate_id"] = mandate_id

    response = request.hugosave_put_request(
        path=ah.card_urls["auto_top_up"].replace("{cash-wallet-id}", cash_wallet_id),
        headers=ah.get_user_header(context, uid),
        data=data
    )
    assert check_status_distribute(response, "200"), f"Expected status code: 200, but received response: {response}"


@Step("I disable auto-top-up of ([^']*) for user ([^']*)")
def disable_auto_top_up(context, product_code ,uid):
    request = context.request
    cash_wallet_id = ah.get_cash_wallet_id_by_product_code(context,uid,product_code)

    response = request.hugosave_put_request(
        path=ah.card_urls["auto_top_up"].replace("{cash-wallet-id}", cash_wallet_id),
        headers=ah.get_user_header(context, uid),
        data={"auto_top_up_enabled": False,
              "is_external": False,
              "cash_wallet_id": cash_wallet_id}
    )
    assert check_status_distribute(response, "200"), f"Expected status code: 200, but received response: {response}"


@Step("I withdraw ([^']*) SGD from card account of user ([^']*)")
def step_impl(context, amount, uid):
    request = context.request

    acc_id = ah.get_spend_account_id(context, uid)
    account_id = ah.get_cash_wallet_id_by_product_code(context,uid,"CASH_WALLET_SAVE")

    amount = float(amount)
    url = ah.cash_urls["transfer"].replace("{cash-wallet-id}", acc_id)
    headers = ah.get_user_header(context, uid)
    response = request.hugosave_put_request(
        path=url,
        data={
            "funding_cash_wallet_id": account_id,
            "amount": amount,
            "transfer_type": "TRANSFER_OUT",
        },
        headers=headers,
    )
    assert check_status_distribute(response, "200"), f"Expected status code: 200, but received response: {response}"


@Step("I add a new ([^']*) Address to order a Card for user ([^']*) and expect a status code of ([^']*)")
def step_impl(context, address_type, uid, expected_status_code):
    request = context.request
    submit_address_type = ""

    data = ""
    if address_type == "Home":
        submit_address_type = "HOME_ADDRESS"
        data = {
            "address": [
            {
                "address_line_1": "2 Orchard Link",
                "address_line_2": "#04-01",
                "address_line_3": "Scape",
                "address_line_4": "",
                "city": "Pakistan",
                "state": "Karachi",
                "country_code": "PAK",
                "local_code": "237978",
                "is_mailing_address": "true",
                "address_type": submit_address_type,
            }
            ]
        }
    else:
      submit_address_type = "WORK_ADDRESS"
      data = {
          "address": [
              {
                  "address_line_1": "3 Kings Landing",
                  "address_line_2": "#07-01",
                  "address_line_3": "Wolf",
                  "address_line_4": "",
                  "city": "Pakistan",
                  "state": "Karachi",
                  "country_code": "PAK",
                  "local_code": "238916",
                  "is_mailing_address": "false",
                  "address_type": submit_address_type,
              }
          ]
      }

    response = request.hugosave_post_request(
        path=ah.user_profile_urls["add_addresses"],
        data=data,
        headers=ah.get_user_header(context, uid),
    )
    assert check_status_distribute(response, expected_status_code), f"Expected the status code: {expected_status_code}, but received the response: {response}"


@Step("I check if the ([^']*) Address is added successfully for the user ([^']*)")
def step_impl(context, address_type, uid):
    request = context.request
    check_address_type = ""

    if address_type == "Home":
        check_address_type = "HOME_ADDRESS"
    else:
        check_address_type = "WORK_ADDRESS"
    params = {"address-type": check_address_type}

    response = request.hugosave_get_request(
        path=ah.user_profile_urls["add_addresses"],
        params=params,
        headers=ah.get_user_header(context, uid),
    )
    assert check_status_distribute(response, "200")
    if not check_address_type in context.data["users"][uid]:
        context.data["users"][uid][check_address_type] = {}
        context.data["users"][uid][check_address_type]["address_id"] = response["data"]["userAddressId"]


@Step("I update the ([^']*) limit of channel ([^']*) to ([^']*) for user ([^']*) and expect a status code of ([^']*)")
def update_limits(context, card_type , channel_type,limit_amount, uid, expected_status_code):
    request = context.request
    amount = 0.0
    currency = ""
    amount_checks_list = limit_amount.split(" ")
    for item in amount_checks_list:
        try:
            amount = float(item)
        except ValueError:
            if item == "PKR" or item == "SGD":
                currency = item

    user_cards = context.data["users"][uid]["cards"]
    headers = ah.get_user_header(context,uid)
    headers["x-final-user-authorisation-token"] = context.data["users"][
        uid
    ]["user_authorisation_token"]

    card_id = ""
    limit_id = ""
    # for card in user_cards:
    if (user_cards["cardLabel"] == card_type):
        card_id = user_cards["cardId"]
    for channel in user_cards["cardTxnChannelDetails"]["channelDetails"]:
        if channel["channel"] == channel_type:
            limit_id = channel["cardLimitDetails"]["limitId"]

    response = request.hugosave_put_request(
        headers = headers,
        data = { "limit_id": limit_id , "value": amount },
        path = ah.card_urls["update_limits"].replace("{card-id}",card_id)
    )

    assert check_status_distribute(response, expected_status_code), f"The expected status code is: {expected_status_code}, but received response: {response}"

@Step("I check if the ([^']*) limit for the ([^']*) channel is set to ([^']*) for user ([^']*)")
def check_limits(context, card_type, channel_type,limit_amount,uid):
    request = context.request
    amount = 0.0
    currency = ""
    amount_checks_list = limit_amount.split(" ")
    for item in amount_checks_list:
        try:
            amount = float(item)
        except ValueError:
            if item == "PKR" or item == "SGD":
                currency = item

    user_cards = context.data["users"][uid]["cards"]
    card_id = ""
    # for card in user_cards:
    if (user_cards["cardLabel"] == card_type):
        card_id = user_cards["cardId"]

    @retry(AssertionError, tries=10, delay=15, logger=None)
    def retry_check_limit():
        response = request.hugosave_get_request(
            headers = ah.get_user_header(context,uid),
            path = ah.card_urls["get_limits"].replace("{card-id}",card_id)
        )

        if check_status_distribute(response,200):
            max_value=""
            channels = response["data"]["channelDetails"]
            for channel in channels:
                if (channel["channel"] == channel_type):
                    max_value = channel["cardLimitDetails"]["userSetValue"]

            assert max_value == amount, f"Limit Not Updated, received response: {response}"

    retry_check_limit()

@Step("I block the ([^']*) channel ([^']*) for user ([^']*)")
def block_channel(context,card_type,channel_type,uid):
    request = context.request
    # user_cards = context.data["users"][uid]["cards"]

    # -----------for testing-----------------------------
    user_cards = context.data["users"][uid]["cards"][0]
    # ---------------------------------------------------

    card_id = ""
    limit_id = ""
    if (user_cards["cardLabel"] == card_type):
        card_id = user_cards["cardId"]

    headers = ah.get_user_header(context,uid)
    headers["x-final-user-authorisation-token"] = context.data["users"][
        uid
    ]["user_authorisation_token"]

    data = ""
    if (channel_type == "E_COMMERCE"):
        data = {
            "channel": "E_COMMERCE",
            "channel_status": {
                "ecom_status": {
                    "enabled": False
                }
            }
        }
    elif (channel_type == "POS"):
        data = {
            "channel": "POS",
            "channel_status": {
                "pos_status": {
                    "enabled": False
                }
        }
        }
    else:
        data = {
            "channel": "POS",
            "channel_status": {
                "atm_status": {
                    "enabled": True,
                    "local_enabled": True
                }
            }
        }

    response = request.hugosave_put_request(
        headers = headers,
        path = ah.card_urls["get_limits"].replace("{card-id}",card_id),
        data = data
    )

    assert check_status_distribute(response,"200"), f"Failed to block channel, received response: {response}"

@Step("I check the status of ([^']*) channel ([^']*) to be ([^']*) for user ([^']*)")
def check_limits(context, card_type, channel_type,status,uid):
    request = context.request
    user_cards = context.data["users"][uid]["cards"]
    card_id = ""
    if (user_cards["cardLabel"] == card_type):
        card_id = user_cards["cardId"]

    if status == "DISABLED":
        expected_status = False
    elif status == "ENABLED":
        expected_status = True

    @retry(AssertionError, tries=10, delay=15, logger=None)
    def retry_check_limit():
        response = request.hugosave_get_request(
            headers = ah.get_user_header(context,uid),
            path = ah.card_urls["get_limits"].replace("{card-id}",card_id)
        )

        if check_status_distribute(response,200):
            saved_status=""
            channels = response["data"]["channelDetails"]
            for channel in channels:
                if (channel["channel"] == channel_type):
                    saved_status = channel["channelStatus"]["ecomStatus"]["enabled"]

            assert saved_status == expected_status, f"Channel Status Not Updated\n, received response: {response}"

    retry_check_limit()

@Step("I unblock the ([^']*) channel ([^']*) for user ([^']*)")
def block_channel(context,card_type,channel_type,uid):
    request = context.request
    # user_cards = context.data["users"][uid]["cards"]

    # -----------for testing-----------------------------
    user_cards = context.data["users"][uid]["cards"][0]
    # ---------------------------------------------------

    card_id = ""
    limit_id = ""
    if (user_cards["cardLabel"] == card_type):
            card_id = user_cards["cardId"]

    headers = ah.get_user_header(context,uid)
    headers["x-final-user-authorisation-token"] = context.data["users"][
        uid
    ]["user_authorisation_token"]

    data = ""
    if (channel_type == "E_COMMERCE"):
        data = {
            "channel": "E_COMMERCE",
            "channel_status": {
                "ecom_status": {
                    "enabled": True,
                    "local_enabled": True
                }
            }
        }
    elif (channel_type == "POS"):
        data = {
            "channel": "POS",
            "channel_status": {
                "pos_status": {
                    "enabled": True,
                    "local_enabled": True
                }
            }
        }
    else:
        data = {
            "channel": "POS",
            "channel_status": {
                "atm_status": {
                    "enabled": False
                }
            }
        }

    response = request.hugosave_put_request(
        headers = headers,
        path = ah.card_urls["get_limits"].replace("{card-id}",card_id),
        data = data
    )

    assert check_status_distribute(response,"200"), f"Failed to unblock channel, received response: {response}"


@then("I activate the ([^']*) card for the user ([^']*) with ([^']*) token, with status ([^']*)")
def get_card_id(
    context,
    card_type,
    uid: str,
    token_case: str,
    expected_status_code,
):
    global activation_token
    request = context.request

    if (
        context.data["users"][uid]["cards"][0]["cardType"]
        == "PHYSICAL"
    ):
        card_id = ah.get_card_id(context, uid, card_type)

        activation_token = ""
        response = request.hugosave_get_request(
            path=ah.card_urls["activation_token"].replace("{card-id}", card_id),
            headers=ah.get_user_header(context, uid),
        )
        if check_status_distribute(response, "200"):
            if token_case == "valid":
                activation_token = response["data"]["activationToken"]
            elif token_case == "invalid":
                activation_token = "None"

            headers = ah.get_user_header(context, uid)
            if "user_authorisation_token" in context.data["users"][uid]:
                headers["x-final-user-authorisation-token"] = context.data["users"][
                    uid
                ]["user_authorisation_token"]

            response = request.hugosave_put_request(
                path=ah.card_urls["activate_card"].replace("{card-id}", card_id),
                data={"card_id": card_id, "card_token": activation_token},
                headers=headers,
            )
            assert check_status_distribute(response, expected_status_code), f"Expected status code: {expected_status_code}, but received response: {response}"

