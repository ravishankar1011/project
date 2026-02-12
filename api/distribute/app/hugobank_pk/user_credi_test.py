import json
import time
from behave import *
import tests.api.distribute.app_helper as ah
use_step_matcher("re")

from tests.util.common_util import check_status_distribute
import tests.api.distribute.app_helper as ah


@step("I load existing PLUS user ([^']*)")
def load_existing_user(context, user_alias):
    with open("tests/api/distribute/app/hugobank_pk/user_data.json") as f:
        users = json.load(f)

    user = users[user_alias]

    if context.data.get("users") is None:
        context.data["users"] = {}

    context.data["customer"] = "HUGOBANK"


    context.data["users"][user_alias] = {
        "userProfileId": user["userProfileId"],
        "org_Id": user["orgId"],
        "deviceId": user["deviceId"],

        # 🔑 MUST match app_helper
        "private_key": ah.deserialize_private_key(user["keys"]["privateKey"]),
        "user_details": user["user_details"],
        "wallet": user["wallet"],

        # 🔐 Required by helper internals
        "current_device": "device_1",
        "user_devices": {
            "device_1": {
                "x-device-id": user["deviceId"],
                "os": "Android",
                "os-build-number": "BP2A.250605.031.A3",
                "os-version": "16",
                "device-type": "MOBILE",
                "device-brand-name": "Google",
                "app-first-install-time": "1769169930717",
                "app-version": "2.1.202507030",
                "app-build-version": "2025070801",
                "app-bundle-identifier": "com.hugosave.test"
            }
        }
    }


# @step("I regenerate authentication headers for user ([^']*)")
# def regenerate_auth_headers(context, user_alias):
#     user = context.data["users"][user_alias]
#
#     epoch = str(int(time.time() * 1000))
#
#     device_info = {
#         "x-device-id": user["deviceId"],
#         "x-epoch": epoch
#     }
#
#     binded_signature = ah.get_binded_signature(
#         private_key=user["privateKey"],
#         device_info=device_info
#     )
#
#
#     context.data["users"][user_alias]["headers"] = {
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#         "x-user-profile-id": user["userProfileId"],
#         "x-device-id": user["deviceId"],
#         "x-binded-signature": binded_signature,
#         "x-epoch": epoch,
#         "x-enforce-auth": "true",
#         "x-org-id": user["orgId"]
#     }


from retry import retry

@step("I fetch user details for user ([^']*)")
def fetch_user_details(context, uid):
    request = context.request

    @retry(Exception, tries=3, delay=5)
    def _fetch():
        response = request.hugosave_get_request(
            path=ah.user_profile_urls["details"],
            headers=ah.get_user_header(context, uid),
            params={"is-full-info": True}
        )
        assert response["headers"]["statusCode"] == "200"
        return response["data"]

    context.data["users"][uid]["profile"] = _fetch()


@step("I load existing CREDIT card for user ([^']*)")
def load_existing_credit_card(context, uid):
    with open("tests/api/distribute/app/hugobank_pk/user_data.json") as f:
        users = json.load(f)

    if uid not in users:
        raise Exception(f"User {uid} not found in user_data.json")

    user = users[uid]

    if "cards" not in user or "credit" not in user["cards"]:
        raise Exception(f"No CREDIT card found for user {uid}")

    credit_card = user["cards"]["credit"]

    # Ensure user context exists
    if context.data.get("users") is None:
        context.data["users"] = {}

    if uid not in context.data["users"]:
        context.data["users"][uid] = {}

    # Attach credit card to runtime context
    context.data["users"][uid]["credit_card"] = {
        "card_id": credit_card["cardId"],
        "card_account_id": credit_card["cardAccountId"],
        "cardType": credit_card["cardType"],
        "category": credit_card["category"],
        "cardStatus": credit_card["cardStatus"],
        "nameOnCard": credit_card["nameOnCard"],
        "adminBlocked": credit_card["adminBlocked"]
    }
    context.data["users"][uid]["card_account_id"] = credit_card["cardAccountId"]
    context.data["users"][uid]["card_id"] = credit_card["cardId"]
    context.data["users"][uid]["user_cash_wallets"] = {
        "userCashWallets": [
            {
                "productCode": user["wallet"]["productCode"],
                "userCardAccounts": [
                    {
                        "cardAccountId": user["cards"]["credit"]["cardAccountId"]
                    }
                ]
            }
        ]
    }



@step("I fetch wallet balance for user ([^']*)")
def fetch_wallet_balance(context, user_alias):
    response = context.request.hugosave_get_request(
        path="/app/v2/balance/list",
        headers=ah.get_user_header(context, user_alias)
    )

    assert response["headers"]["statusCode"] == "200"

    balances = response["data"]["cashBalances"]
    context.data["users"][user_alias]["cashBalances"] = balances

    wallet_code = context.data["users"][user_alias]["wallet"]["productCode"]

    for wallet in balances:
        if wallet["productCode"] == wallet_code:
            context.data["users"][user_alias]["currentBalance"] = wallet["balance"]
            context.data["users"][user_alias]["currency"] = wallet["currency"]
            break

    context.data["users"][user_alias]["user_cash_wallets"] = {
        "userCashWallets": response["data"]["cashBalances"]
    }

@step("I store activated card details for user ([^']*)")
def store_activated_card_details(context, uid):
    cards = context.data["users"][uid]["cards"]

    # pick PHYSICAL card
    card = next(c for c in cards if c["cardType"] == "PHYSICAL")

    card_details = {
        "cardId": card["cardId"],
        "cardAccountId": card["cardAccountId"],
        "cardType": card["cardType"],
        "category": card["category"],
        "scheme": card["scheme"],
        "cardStatus": card["cardStatus"],
        "nameOnCard": card["nameOnCard"],
        "cardLast4Digits": card.get("cardLast4Digits"),
        "channels": card["cardTxnChannelDetails"]["channelDetails"],
        "userActionDetails": card["userActionDetails"]
    }

    with open("tests/api/distribute/app/hugobank_pk/card_details.json", "w") as f:
        json.dump({uid: card_details}, f, indent=2)

@Step("I fetch credit account list for user ([^']*)")
def fetch_credit_account_list(context, uid):
    request = context.request

    response = request.hugosave_get_request(
        path=ah.user_profile_urls["credit-account-list"],
        headers=ah.get_user_header(context, uid),
    )

    if check_status_distribute(response, 200):
        context.data["users"][uid]["credit_accounts"] = response["data"]["creditAccounts"]
        print("Credit accounts details -----------:", response["data"])

@Step("I fetch card intents list for user ([^']*)")
def fetch_card_intents_list(context, uid):
    request = context.request
    card_id = context.data["users"][uid]["card_id"]

    response = request.hugosave_get_request(
        path=ah.intent_urls["list_intents_for_cards"].replace("{card-id}", card_id),
        headers=ah.get_user_header(context, uid),
    )

    if check_status_distribute(response, 200):
        context.data["users"][uid]["card_intents"] = response["data"]
        print("Card intents:", response["data"])

@Step("I fetch credit account balance for user ([^']*)")
def fetch_credit_account_list(context, uid):
    request = context.request
    credit_account_id = context.data["users"][uid]["credit_accounts"][0]["creditAccountId"]
    response = request.hugosave_get_request(
        path=ah.cms_urls["balance"].replace("{account-id}", credit_account_id),
        headers=ah.get_user_header(context, uid),
    )

    print("---------context structure-----",context.data["users"])

    if check_status_distribute(response, 200):
        context.data["users"][uid]["credit_account_balance"] = response["data"]
        print("---------------Credit account balance-------------- ",response["data"])
        print("----------------Credit accounts details -----------:", context.data["users"][uid]["credit_accounts"])