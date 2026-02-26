import random
import string
import uuid
import time
import base64
import hashlib
import hmac
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
import json


ORG_ID_HUGOBANK_PK = "HUGOBANK_PK"
ORG_ID_HUGOSAVE_SG = "HUGOSAVE_SG"
ORG_ID_HUGOSAVE_CDV = "CDV_SG"

app_base_url = "/app/v2"
auth_base_url = "/profile/v1"
notification_base_url = "/notification/v1"
progress_onboarding_base_url = "/onboard/progress"
initial_onboarding_base_url = "/onboard/initial"
reward_base_url = "/reward/v2"
documents_base_url = "/documents"
behavioural_base_url = "/behavioural/v2"
org_base_url = "/org/v1"

auth_user_urls = {
    "root": auth_base_url + "/user",
    "create": auth_base_url + "/user/create-user",
    "authenticate-user": auth_base_url + "/authenticate",
}

account_urls = {
    "root": app_base_url + "/account",
}

dev_urls = {
    "root": app_base_url + "/dev",
    "deposit": app_base_url + "/dev/transaction/deposit",
    "compliance": app_base_url + "/dev/compliance/status/update",
    "compliance_update": app_base_url + "/dev/user/account-level/update",
    "schedule_trigger": app_base_url + "/dev/tickle/schedule/{schedule-id}",
    "mock_card_transaction": app_base_url + "/dev/card/{card-id}/mock-transaction",
    "settle_investment_txn": app_base_url + "/dev/investment/{intent-id}",
    "deposit_hugosave_account": app_base_url + "/dev/customer/deposit",
    "list_hugo_balances": app_base_url + "/dev/hugo",
    "card_activation_token": app_base_url + "/dev/card/{card-id}/activation-token",
    "block_deposits": app_base_url + "/dev/block/deposits",
    "unblock_deposits": app_base_url + "/dev/block/deposits",
    "block_merchant_transactions": app_base_url + "/customer-user/block/debits",
    "unblock_merchant_transactions": app_base_url + "/customer-user/block/debits",
    "update": auth_base_url + "/customer-user/update",
    "clear_roundup_schedule": app_base_url + "/dev/clear-roundups",
    "settle-all-txn": app_base_url + "/dev/investment/settle-withdraw",
    "questionnaire": app_base_url + "/internal/questionnaire",
    "credit_mock_txn": app_base_url + "/dev/credit/mock-transactions",
    "generate_credit_bills": app_base_url + "/dev/credit/generate-bill",
    "reset_cool_off": auth_base_url + "/dev/user/cool-off",
    "update_status": auth_base_url + "/dev/user/journey/update",
    "accept-mandate": app_base_url + "/dev/accept/mandate-id",
    "authorize-mandate": app_base_url + "/dev/authorize/mandate-id"
}

customer_user_urls = {
    "root": app_base_url + "/customer-user",
    "operator-action": auth_base_url + "/customer-user/operator-action",
}

customer_urls = {
    "search": app_base_url + "/customer/users/search"
}

cms_urls = {
    "root": app_base_url + "/credit-account",
    "balance": app_base_url + "/credit-account/{account-id}/balance",
    "bills": app_base_url + "/credit-account/{account-id}/bills",
}

user_profile_urls = {
    "root": app_base_url + "/user-profile",
    "details": auth_base_url + "/user",
    "status": app_base_url + "/user-profile/status",
    "client_flags": app_base_url + "/user-profile/client-flags",
    "map-list": app_base_url + "/user-profile/maps",
    "card_name": app_base_url + "/user-profile/card-names",
    "cards": app_base_url + "/user-profile/cards",
    "credit-account-list": app_base_url + "/user-profile/credit-accounts",
    "payees-list": app_base_url + "/user-profile/payees",
    "add_addresses": app_base_url + "/user-profile/address",
    "get_addresses": app_base_url + "/user-profile/address",
    "get_all_cash_wallets": app_base_url + "/user-profile/cash-wallets",
    "config_inquiry": app_base_url + "/user-profile/config-inquiry"
}

payee_urls = {
    "root": app_base_url + "/payee",
    "list": app_base_url + "/payee/list",
    "pay_payee": app_base_url + "/payee/{payee-id}/pay",
    "payee": app_base_url + "/payee/{payee-id}",
    "submit-otp": app_base_url + "/payee/{payee-id}/submit-otp",
    "inquiry": app_base_url + "/payee/inquiry",
    "qr_payment": app_base_url + "/payee/pay",
    "payee-config": app_base_url + "/payee/payee-config",
    "currency-config": app_base_url + "/payee/currency-config",
    "restore-payee": app_base_url + "/payee/{payee-id}/restore",
}

map_urls = {
    "root": app_base_url + "/map",
    "update": app_base_url + "/map/{map-id}",
    "invest": app_base_url + "/map/{map-id}/invest",
    "withdraw": app_base_url + "/map/{map-id}/withdraw",
    "rate": app_base_url + "/map/{map-id}/rate",
}

map_schedule_urls = {
    "root": app_base_url + "/schedule",
    "list": app_base_url + "/schedule",
    "detail": app_base_url + "/schedule/{schedule-id}",
    "update-status": app_base_url + "/schedule/{schedule-id}/status",
    "amount": app_base_url + "/schedule/amount",
    "history": app_base_url + "/schedule/{schedule-id}/history",
    "skip": app_base_url + "/schedule/{schedule-id}/skip",
    "update": app_base_url + "/schedule/{schedule-id}",
}

balance_urls = {
    "root": app_base_url + "/balance",
    "account": app_base_url + "/balance/cash/{acc-id}",
    "map": app_base_url + "/balance/map/{map-id}",
    "balances": app_base_url + "/balance/list",
}

compliance_urls = {
    "root": app_base_url + "/compliance",
    "trust-compliance": app_base_url + "/compliance/trust",
    "initiate-compliance": app_base_url + "/compliance/initiate",
    "submit-compliance": app_base_url + "/compliance/submit",
}

asset_ids = {
    "CASH": "dc3a889c-8199-4683-be3a-7061bb8624c8",
    "GOLD": "524d466e-28a7-44db-b1c4-175953277629",
}

card_urls = {
    "root": app_base_url + "/card",
    "activation_token": app_base_url + "/dev/card/{card-id}/activation-token",
    "activate_card": app_base_url + "/card/{card-id}/activate/physical",
    "update_status": app_base_url + "/card/{card-id}/status",
    "card_details": app_base_url + "/card/{card-id}",
    "secure_card_details": app_base_url + "/card/{card-id}/secure-details",
    "replace_card": app_base_url + "/card/{card-id}/replace",
    "auto_top_up": app_base_url + "/cash-wallet/{cash-wallet-id}/auto-top-up",
    "order_card": app_base_url + "/card/issue-card",
    "order_virtual_card": app_base_url + "/card/issue-virtual-card",
    "cards": app_base_url + "/card-account/{card-account-id}/cards",
    "transfer": app_base_url + "/card-account/{card-account-id}/transfer",
    "update_limits" : app_base_url + "/card/{card-id}/limits",
    "get_limits": app_base_url + "/card/{card-id}/txn-channel",
    "get_limit_history": app_base_url + "/card/{card-id}/limits/history",
}

# Credit Card related URLs
credit_card_urls = {
    "get_product_config": app_base_url + "/credit-account/product-config/CREDIT_ACCOUNT_SECURED_CREDIT_CARD_PRODUCT",
    "show_card_pin": app_base_url + "/card/{card-id}/show-pin",
    "update_credit_limit" : app_base_url + "/credit-account/{account-id}/credit-limit",
    "get_cash_advance_limit": app_base_url + "/credit-account/{account-id}/cash-advance-limit",
    "request_cash_advance": app_base_url + "/credit-account/{account-id}/cash-advance",
    "get_credit_account_bills": app_base_url + "/credit-account/{account-id}/bills",
    "get_credit_account_latest_bill": app_base_url + "/credit-account/{account-id}/latest-bill",
    "pay_credit_account_bill": app_base_url + "/credit-account/{account-id}/pay-bill",
    "close_credit_account" : app_base_url + "/credit-account/{account-id}/close",
}

progress_onboarding_urls = {
    "initiate-progress-onboarding": auth_base_url + progress_onboarding_base_url + "/initiate",
    "initiate-onboarding-journey": auth_base_url + progress_onboarding_base_url + "/journey/{journey-id}/initiate",
    "onboarding-journey-status": auth_base_url + progress_onboarding_base_url + "/journey/{journey-id}/status",
    "submit-onboarding-journey": auth_base_url + progress_onboarding_base_url + "/journey/{journey-id}/submit",
    "process-onboarding-journey": auth_base_url + progress_onboarding_base_url + "/journey/{journey-id}/process",
    "submit-progress-onboarding": auth_base_url + progress_onboarding_base_url + "/submit",
    "progress-onboarding-status": auth_base_url + progress_onboarding_base_url + "/status",
    "progress-onboarding-update": auth_base_url + progress_onboarding_base_url + "/journey/{journey-id}/update",
}

roundup_urls = {
    "root": app_base_url + "/roundup",
    "enable": app_base_url + "/roundup/status",
    "update_sweep_vault": app_base_url + "/roundup/sweep-details",
    "transfer": app_base_url + "/roundup/transfer",
    "sweep": app_base_url + "/roundup/sweep",
    "trigger": app_base_url + "/roundup/trigger",
}

intent_urls = {
    "root": app_base_url + "/intent",
    "list_intents_for_map": app_base_url + "/intent/map/{map-id}",
    "list_spend_view_intents": app_base_url + "/intent/spend",
    "list_intents_for_account": app_base_url + "/intent/cash/{cash-wallet-id}",
    "list_intents_for_cards": app_base_url + "/intent/card/{card-id}",
    "list_intents_for_roundup": app_base_url + "/intent/roundup"
}

cash_urls = {
    "root": app_base_url + "/cash",
    "get-details": app_base_url + "/cash-wallets",
    "transfer": app_base_url + "/cash/{cash-wallet-id}/transfer",
    "auto_top_up": app_base_url + "/cash/{cash-wallet-id}/auto-top-up",
    "update_cash_wallet_status": app_base_url + "/cash/{cash-wallet-id}/status",
    "update_cash_wallet_txn_status": app_base_url + "/cash/{cash-wallet-id}/transactions/status",
    "cash-wallet-details": app_base_url + "/cash/{cash-wallet-id}",
    "create-dynamic-qr": app_base_url + "/cash/{cash-wallet-id}/qr-code",
    "exchange-rate": app_base_url + "/cash/{cash-wallet-id}/exchange-rate",
}

device_urls = {
    "root": notification_base_url + "/pn",
    "list": notification_base_url + "/pn/list",
    "delete": notification_base_url + "/pn/token",
}

note_urls = {
    "root": app_base_url + "/note",
    "get_note": app_base_url + "/note/intent-id/{intent_id}",
}

reward_urls = {
    "gold": app_base_url + "/dev/reward-gold",
    "cash": app_base_url + "/dev/reward-cash",
    "claim": reward_base_url + "/user-reward/{user-reward-id}/claim",
    "unlocked": reward_base_url + "/user-reward/unlocked"
}

questionnaire_urls = {
    "root": auth_base_url + "/questionnaire",
    "list": org_base_url + "/questionnaire/list",
    "details": auth_base_url + "/questionnaire/questionnaire-name",
    "user-questionnaire": auth_base_url + "/questionnaire/user-questionnaire",
    "update": auth_base_url + "/questionnaire/user-questionnaire/{user-questionnaire-id}",
    "submit": auth_base_url + "/questionnaire/user-questionnaire/{user-questionnaire-id}/submit",
    "list-user-questionnaire": auth_base_url + "/questionnaire/list-user-questionnaire",
}

token_urls = {
    "user-authentication-token": app_base_url + "/user-authorise/initial/initiate"
}

verification_urls = {
    "root": auth_base_url + "/verify/verify-mobile",
    "submit": auth_base_url + "/verify/verify-mobile",
}

initial_onboarding_urls = {
    "initiate-initial-onboarding": auth_base_url + initial_onboarding_base_url + "/initiate",
    "initial-onboarding-status": auth_base_url + initial_onboarding_base_url + "/status",
    "submit-initial-onboarding": auth_base_url + initial_onboarding_base_url + "/submit",
    "initiate-initial-onboarding-journey": auth_base_url + initial_onboarding_base_url + "/journey/{journey-id}/initiate",
    "process-initial-onboarding-journey": auth_base_url + initial_onboarding_base_url + "/journey/{journey-id}/process",
    "submit-initial-onboarding-journey": auth_base_url + initial_onboarding_base_url + "/journey/{journey-id}/submit",
    "initial-onboarding-journey-status": auth_base_url + initial_onboarding_base_url + "/journey/{journey-id}/status"
}

verify_mobile_urls = {
    "initiate-mobile-verification": auth_base_url + "/verify/verify-mobile",
    "initiate-email-verification": auth_base_url + "/verify/verify-email"
}

verify_email_urls = {
    "initiate-verification": auth_base_url + "/verify/verify-email"
}

get_user_authorisation_token_urls = {
    "initial-initiate": auth_base_url + "/user-authorise/initial/initiate",
    "final-initiate": auth_base_url + "/user-authorise/final/initiate",
    "journey-initiate": auth_base_url + "/user-authorise/journey/{journey-id}/initiate",
    "journey-submit": auth_base_url + "/user-authorise/journey/{journey-id}/submit",
    "final-submit": auth_base_url + "/user-authorise/final/{session-id}/submit",
    "final-status": auth_base_url + "/user-authorise/final/{session-id}/status",
    "process-journey": auth_base_url + "/user-authorise/journey/{journey-id}/process",
    "initial-submit": auth_base_url + "/user-authorise/initial/{session-id}/submit",
    "initial-status": auth_base_url + "/user-authorise/initial/{session-id}/status",
}

forgot_passcode_token_urls = {
    "initiate": app_base_url + "/forgot-passcode/initiate",
    "check-initiate-status": app_base_url + "/forgot-passcode/{session-id}/status",
    "journey-initiate": app_base_url + "/forgot-passcode/journey/{journey-id}/initiate",
    "journey-submit": app_base_url + "/forgot-passcode/journey/{journey-id}/submit",
    "final-submit": app_base_url + "/forgot-passcode/submit",
    "final-status": app_base_url + "/forgot-passcode/{session-id}/status",
    "update-passcode": app_base_url + "/forgot-passcode",
    "process-forgot-passcode-journey": app_base_url + "/forgot-passcode/journey/{journey-id}/process"
}

account_management_urls = {
    "update-passcode": auth_base_url + "/account-management/reset-pin",
    "update_phone_number": auth_base_url + "/account-management/phone-number",
    "update_email": auth_base_url + "/account-management/email",
    "update_mailing_address": auth_base_url + "/account-management/mailing-address",
    "update_name": auth_base_url + "/account-management/name",
    "update_next_of_kin": auth_base_url + "/account-management/next-of-kin"
}

limits_urls = {
    "update-limits": app_base_url + "/user-profile/limits",
    "get-limits": app_base_url + "/user-profile/limits",
}

device_authorisation_urls = {
    "status": auth_base_url + "/device-authorise/status",
    "initiate": auth_base_url + "/device-authorise/initiate",
    "submit": auth_base_url + "/device-authorise/submit",
    "initiate-journey": auth_base_url + "/device-authorise/journey/{journey-id}/initiate",
    "process-journey": auth_base_url + "/device-authorise/journey/{journey-id}/process",
    "submit-journey": auth_base_url + "/device-authorise/journey/{journey-id}/submit"
}

gtw_device_urls = {
    "bind" : "/v2/device/bind"
}

device_management_urls = {
    "list": app_base_url + "/device/list",
    "unbind": app_base_url + "/device/unbind/{device-id}"
}

user_urls = {
    "block": auth_base_url + "/user/block",
    "status": auth_base_url + "/user/status",
}

product_urls = {
    "root": org_base_url + "/product",
    "create": org_base_url + "/product",
    "approve": org_base_url + "/product/{product-id}/approve",
    "transaction_code": org_base_url + "/product/{product-id}/transaction-code"
}


authentication_urls = {
    "authenticate": app_base_url + "/v2/authenticate"
}

bill_payees = {
    "list-operators": app_base_url + "/bill-payments/billers/biller-category",
    "add-bill-payee": app_base_url + "/bill-payments/bill-payee",
    "pay-bill-payee": app_base_url + "/bill-payments/bill-payee/{bill-payee-id}/pay",
    "bill-payee-inquiry": app_base_url + "/bill-payments/bill-payee/{bill-payee-id}/bill-inquiry",
}

document_urls = {
    "root": app_base_url + documents_base_url,
    "get_all_user_documents": app_base_url + documents_base_url + "/user",
    "get_user_document": app_base_url + documents_base_url + "/{user-document-id}",
    "generate_certificate": app_base_url + documents_base_url + "/certificate",
    "generate_statement": app_base_url + documents_base_url + "/statement",
    "update_document_frequency": app_base_url + documents_base_url + "/frequency",
}

virtual_id_urls = {
    "link": app_base_url + "/virtual-id/link",
    "create": app_base_url + "/virtual-id/"
}

mandate_urls = {
    "create-mandate": app_base_url + "/direct-debit",
    "get-mandate": app_base_url + "/direct-debit/mandate-id",
}

behavioural_urls = {
    "onboarding": behavioural_base_url + "/internal/onboarding",
    "push_event": behavioural_base_url + "/event/server",
    "user_quests_dto": behavioural_base_url + "/quests/user-quests",
    "user_state": behavioural_base_url + "/quests/user-state-changed",
    "claim_reward": reward_base_url + "/user-reward/user-reward-id/claim",
    "fetch_claimed_reward": reward_base_url + "/user-reward/claimed",
    "fetch_onboard_dto": behavioural_base_url + "/dev/user",
    "user_quest_profile": behavioural_base_url + "/dev/user-quest-profile",
    "user_referrals": behavioural_base_url + "/quests/user-referrals/unlocked",
    "user_quests": behavioural_base_url + "/dev/user-quests",
    "quests": behavioural_base_url + "/quests",
    "migrate": behavioural_base_url + "/internal/migrate",
    "create_quest": behavioural_base_url + "/internal/create/quest",
    "add_cohort": behavioural_base_url + "/internal/cohort",
    "reset_quest_stats": behavioural_base_url + "/dev/reset-quest-stats/quest-id",
}


onboarding_fields = [
    "email",
    "first_name",
    "account_type",
    "time_zone",
    "roundups_enabled",
    "profile_status",
]

quest_user_profile_entity_fields = [
    "account_type",
    "time_zone",
    "roundups_enabled",
    "profile_status",
]


def get_user_header(uid, context):
    return {
        "x-user-profile-id": uid,
        "app-build-version": context.data["config_data"]["app-build-version"],
    }


def determine_org_id(distribute_endpoint):
    if "hugobank" in distribute_endpoint:
        return ORG_ID_HUGOBANK_PK
    elif "hugosave" in distribute_endpoint:
        return ORG_ID_HUGOSAVE_SG
    elif "cdv" in distribute_endpoint:
        return ORG_ID_HUGOSAVE_CDV
    return ORG_ID_HUGOSAVE_SG  # Default

def get_create_account_header(context, uid):
    device_info = get_device_info(context, uid)
    return {
            "x-verification-token": context.data["users"][uid][
                "submit_mobile_verification_response"
            ]["verificationToken"],
            "x-device-id": device_info["x-device-id"],
            "app-build-version": device_info["app-build-version"],
            "device-type": device_info["device-type"],
            "device-brand-name": device_info["device-brand-name"],
            "os": device_info["os"],
            "os-build-number": device_info["os-build-number"],
            "x-org-id": context.data["org_id"]
    }



def get_initial_onboarding_headers(context, uid):
    device_info = get_device_info(context, uid)
    return {
        "x-user-profile-id": get_user_profile_id(uid, context),
        "x-authentication-token": context.data["users"][uid][
            "create_new_user_response"
        ]["authenticationToken"],
        "x-device-id": device_info["x-device-id"],
        "x-org-id": context.data["org_id"]
    }


def get_portal_header(uid, context):
    return {
        "x-user-profile-id": uid,
        "x-origin-id": "PORTAL",
        "x-principal-id": get_portal_principle_id(context),
        "x-principal-access-key": "FlBRW4cSWvIp1ST3PBBqQv6vlFnx3pS2owj9wVrsqUYzAstSl7XqdlKQsHw9xYsK",
        "app-build-version": "2.1.202507030",
        "x-enforce-auth": "false",
        "x-portal-operator-id": "f2b73384-e640-4e75-9342-497a7b3c7e16",
        "x-org-id": context.data["org_id"]
    }


def get_user_header(context, uid):
    user_profile_id = get_user_profile_id(uid,context)
    device_info = get_device_info(context, uid)
    concatenated_headers = concatenated_header_values_binded_signature(device_info, user_profile_id)
    binded_signature = create_signature(context.data["users"][uid]["private_key"], concatenated_headers)
    return {
            "x-user-profile-id": user_profile_id,
            "x-device-id": device_info["x-device-id"],
            "x-binded-signature": binded_signature,
            "x-epoch": str(int(time.time()*1000)),
            "x-enforce-auth": "true",
            "os": device_info["os"],
            "os-build-number": device_info["os-build-number"],
            "os-version": device_info["os-version"],
            "device-type": device_info["device-type"],
            "device-brand-name": device_info["device-brand-name"],
            "app-first-install-time": device_info["app-first-install-time"],
            "app-version": device_info["app-version"],
            "app-build-version": device_info["app-build-version"],
            "app-bundle-identifier": device_info["app-bundle-identifier"],
            "x-org-id": context.data["org_id"]
    }


def get_device_authorisation_header(context, uid):
    device_info = get_device_info(context, uid)
    user_profile_id = get_user_profile_id(uid, context)
    return {
            "x-user-profile-id": user_profile_id,
            "app-build-version": device_info["app-build-version"],
            "x-device-id": device_info["x-device-id"],
            "x-org-id": context.data["org_id"]
    }


def get_questionnarie_authorisation_header(uid, context):
    device_info = get_device_info(context, "UID1")
    return {
        "app-build-version": context.data["config_data"]["app-build-version"],
        "x-device-id": device_info["x-device-id"],
        "x-org-id": uid
    }


def get_customer_user_headers(uid, context):
    return {
        "x-user-profile-id": uid,
        "app-build-version": context.data["config_data"]["app-build-version"],
        "x-operator-id": "123456",
    }


def get_header(context):
    return {
        "app-build-version": context.data["config_data"]["app-build-version"],
        "x-verification-token": context.data["users"]["verification-token"],
        "x-device-id": context.data["device_info"]["x-device-id"],
    }


def get_auth_header(uid, context):
    return {
        "x-initiation-signature": uid,
        "app-build-version": context.data["config_data"]["app-build-version"],
    }


def get_user_profile_id(uid, context):
    try:
        return context.data["users"][uid]["create_new_user_response"]["userProfileId"]
    except Exception:
        return ""


def get_uuid():
    return str(uuid.uuid1())


def get_rand_number(n):
    return str(random.randint(pow(10, n - 1), pow(10, n) - 1))


def get_cash_wallet_id(context, user_profile_identifier):
    user_wallets = context.data["users"][user_profile_identifier][
        "user_cash_wallets"
    ]
    if context.data["customer"] == "HUGOSAVE":
        product_code = "CASH_WALLET_SAVE"
    elif context.data["customer"] == "HUGOBANK":
        product_code = "CASH_WALLET_CURRENT"
    else:
        product_code = "CASH_WALLET_DIGITAL"

    account_id = None
    for wallet in user_wallets["userCashWallets"]:
        if wallet["productCode"] == product_code:
            account_id = wallet["cashWalletId"]
    return account_id


def get_cash_wallet_id_by_product_code(context, user_profile_identifier, product_code):
    user_wallets = context.data["users"][user_profile_identifier][
        "user_cash_wallets"
    ]
    account_id = None
    for wallet in user_wallets["userCashWallets"]:
        if wallet["productCode"] == product_code:
            account_id = wallet["cashWalletId"]
    return account_id


def get_dummy_user_data(req):
    random_number = get_rand_number(5)
    update_account_data = {
        "client_flags": {"LITE": "True"} if "client_flags" in req else None,
        "address": (
            {
                "address_line_1": "line1" + random_number,
                "address_line_2": "line2" + random_number,
                "address_line_3": "line3" + random_number,
                "address_line_4": "line4" + random_number,
                "city": "city" + random_number,
                "state": "state" + random_number,
                "country_code": "SGP",
                "local_code": random_number,
            }
            if "address" in req
            else None
        ),
        "dob": "19" + get_rand_number(2) + "-02-01" if "dob" in req else None,
        "name": "First" + random_number if "name" in req else None,
        "last_name": "Last" + random_number if "last_name" in req else None,
        "nationality": "SGP" if "nationality" in req else None,
        "phone_number": "373" + get_rand_number(9),
        "email": get_rand_number(5) + "@gmail.com",
        "document_number": (
            "T" + get_rand_number(7) + "S" if "document_number" in req else None
        ),
        "document_expiry_date": (
            "14-09-203" + get_rand_number(1) + " 00:00:00"
            if "document_expiry_date" in req
            else None
        ),
        "tax_id_number": get_rand_number(6) if "tax_id_number" in req else None,
    }

    return {k: v for k, v in update_account_data.items() if k in req}


def _get_sg_bank_details(account_number: str) -> dict:
    return {
        "country": "SGP",
        "currency": "SGD",
        "bank_name": "DBS",
        "code_details": {
            "sg_bank_details": {
                "account_number": account_number,
                "swift_bic": "DBSSSGSGXXX",
            }
        },
    }


def _get_pk_bank_details(
    context, payee_profile_identifier: str, account_number: str, case: str
) -> dict:
    pk_bank_details = {
        "country": "PAK",
        "currency": "PKR",
        "bank_name": "HugoBank Limited",
        "code_details": {
            "pk_bank_details": {
                "account_number": account_number,
                "bank_name": "HugoBank Limited",
                "currency": "PKR",
            }
        },
    }

    if case == "valid_iban":
        iban = context.data["users"][payee_profile_identifier]["iban"]
        pk_bank_details["code_details"]["pk_bank_details"]["iban"] = iban
    else:
        pk_bank_details["code_details"]["pk_bank_details"]["bank_bic"] = "HUGOPKKA"

    return pk_bank_details


def get_add_payee_data(
    context,
    name: str,
    payee_profile_identifier: str,
    account_number: str,
    email: str,
    phone_number: str,
    case: str,
) -> dict:

    if context.data["customer"] == "HUGOSAVE":
        bank_details_config = _get_sg_bank_details(account_number)
    else:
        bank_details_config = _get_pk_bank_details(
            context, payee_profile_identifier, account_number, case
        )

    req = {
        "name": name,
        "email": email,
        "phone_number": phone_number,
        "is_favorite": True,
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "zip": "12345",
            "country": "USA",
        },
        "transfer_out_account_details": {
            "account_holder_name": name,
            "country": bank_details_config["country"],
            "currency": bank_details_config["currency"],
            "code_details": bank_details_config["code_details"],
            "bank_name": bank_details_config["bank_name"],
        },
    }

    if case == "invalid_swift_bic":
        if "sg_bank_details" in req["transfer_out_account_details"]["code_details"]:
            req["transfer_out_account_details"]["code_details"]["sg_bank_details"][
                "swift_bic"
            ] = "DBSSSGSGXYX"
        else:
            print(
                "Warning: invalid_swift_bic case applied to non-Singaporean bank details."
            )
    if case == "invalid_currency":
        req["transfer_out_account_details"]["currency"] = "ABC"

    return req


def get_payee_with_raast(context, name, raast_id)->dict:
    return {
        "transfer_out_account_details": {
            "account_holder_name": name,
            "bank_name": "HugoBank Limited",
            "country": "PAK",
            "currency": "PKR",
            "code_details": {
                "pk_bank_details": {
                    "virtual_id_details": {
                        "virtual_id_type": "MOBILE",
                        "virtual_id_value": raast_id
                    }
                }
            }
        }
    }


def filter_gold_vault(maps):
    return list(filter(lambda c: c["map_name"] != "GOLD_VAULT", maps))


def get_user_map_id(context, map_identifier, user_profile_identifier):
    user_maps = context.data["users"][user_profile_identifier]["user_details_response"]["userMaps"]
    map_id = None

    for map_data in user_maps:
        if map_data["mapType"] == map_identifier:
            return map_data["userMapId"]

    return context.data["users"][user_profile_identifier][map_identifier]["userMapId"]


def get_balance(response, product_code):
    balance = None
    if product_code in ("CASH_WALLET_SAVE", "CASH_WALLET_SPEND", "CASH_WALLET_CURRENT", "CASH_WALLET_DIGITAL"):
        for account_balance in response["data"]["cashBalances"]:
            if account_balance["productCode"] == product_code:
                return account_balance["balance"]
    elif product_code == "CASH_WALLET_ROUNDUP":
        return response["data"]["roundUpBalance"]["balance"]



def get_balance_by_product(response, product_code):
    for account_balance in response["data"]["cashBalances"]:
        if account_balance["productCode"] == product_code:
            return account_balance["balance"]

    return None


def get_card_id(context, uid, card_tag):
    # TODO updated this to return cardId by productCode
    return context.data["users"][uid][card_tag]["card_id"]


def get_card_account_id(context, user_identifier):
    for cash_wallet in context.data["users"][user_identifier]["user_cash_wallets"]["userCashWallets"]:
        if context.data["customer"] == "HUGOBANK":
            if cash_wallet["productCode"] == "CASH_WALLET_CURRENT" :
                for card_account in cash_wallet["userCardAccounts"]:
                  return card_account["cardAccountId"]
        elif context.data["customer"] == "HUGOSAVE":
            if cash_wallet["productCode"] == "CASH_WALLET_SPEND" :
                for card_account in cash_wallet["userCardAccounts"]:
                    return card_account["cardAccountId"]
        else:
            if cash_wallet["productCode"] == "CASH_WALLET_DIGITAL" :
                for card_account in cash_wallet["userCardAccounts"]:
                    return card_account["cardAccountId"]

    return None

def get_funding_id(context, user_profile_identifier):
        for cash_wallet in context.data["users"][user_profile_identifier]["user_cash_wallets"]["userCashWallets"]:
            if context.data["customer"] == "HUGOBANK":
                if cash_wallet["productCode"] == "CASH_WALLET_CURRENT" :
                    for card_account in cash_wallet["userCardAccounts"]:
                        return card_account["fundingId"]


def get_spend_account_id(context, user_identifier):
    for cash_wallet in context.data["users"][user_identifier]["user_cash_wallets"]["userCashWallets"]:
        if(context.data["customer"] == "HUGOBANK"):
            if ( cash_wallet["productCode"] == "CASH_WALLET_CURRENT" ):
                return cash_wallet["cashWalletId"]
        else:
            if ( cash_wallet["productCode"] == "CASH_WALLET_SPEND" ):
                return cash_wallet["cashWalletId"]

    return None


def get_initial_onboarding_id(uid, context):
    try:
        return context.data["users"][uid]["initiate_initial_onboarding_response"][
            "onboardingId"
        ]
    except Exception:
        return ""


def get_progress_onboarding_id(context, uid):
    try:
        return context.data["users"][uid]["initiate_onboarding_response"][
            "onboardingId"
        ]
    except Exception:
        return "Could not find progress onboarding Id"


def get_journey_id(context, uid, journey_type, step_code):
    journey_id = context.data["journey_details"][step_code][journey_type]
    return journey_id


def store_journey_id(context, response):
    journey_step_list = response["data"]["journeySteps"]
    context.data["journey_details"] = {}
    for journey_step in journey_step_list:
        if journey_step["stepCode"]:
            context.data["journey_details"][journey_step["stepCode"]] = {}
            journey_step_resolution = journey_step
            journeys = journey_step_resolution["journeys"]
            for journey in journeys:
                if journey["journey"]:
                    journey_id = journey["journeyId"]
                    context.data["journey_details"][journey_step["stepCode"]][journey["journey"]] = journey_id


def get_user_authorisation_journey_id(context, uid, journey_type, step_code):
    journey_step_list = context.data["users"][uid]["user_final_authorisation_token_response"]["journeySteps"]
    journey_step_resolution = None
    journey_id = None
    for journey_step in journey_step_list:
        if journey_step["stepCode"] == step_code:
            journey_step_resolution = journey_step
    journeys = journey_step_resolution["journeys"]
    for journey in journeys:
        if journey["journey"] == journey_type:
            journey_id = journey["journeyId"]
    return journey_id


def get_forgot_passcode_journey_id(context, uid, journey_type, step_code):
    journey_step_list = context.data["users"][uid]["initiate_forgot_passcode"]["journeySteps"]
    journey_step_resolution = None
    journey_id = None
    for journey_step in journey_step_list:
        if journey_step["stepCode"] == step_code:
            journey_step_resolution = journey_step
    journeys = journey_step_resolution["journeys"]
    for journey in journeys:
        if journey["journey"] == journey_type:
            journey_id = journey["journeyId"]
    return journey_id


def get_passcode(context, user_profile_identifier):
    return context.data["users"][user_profile_identifier]["user_details"]["password"]


def get_user_name_verification_header(context, device_info):
        return {
            "os": device_info["os"],
            "os-build-number": device_info["os-build-number"],
            "os-version": device_info["os-version"],
            "device-brand-name": device_info["device-brand-name"],
            "x-device-id": device_info["x-device-id"],
            "device-type": device_info["device-type"],
            "app-first-install-time": device_info["app-first-install-time"],
            "app-version": device_info["app-version"],
            "app-bundle-identifier": device_info["app-bundle-identifier"],
            "app-build-version": device_info["app-build-version"],
            "x-epoch": str(device_info["x-epoch"]),
            "x-initiation-signature": get_initiation_signature(device_info),
            "x-org-id": context.data["org_id"],
            "x-location-coordinates": device_info["x-location-coordinates"],
        }


def forgot_passcode_headers(context, uid):
    user_data = context.data["users"][uid]
    headers = get_user_header(context, uid)
    user_name = user_data["submit_mobile_verification_response"]["userName"]
    verification_token = user_data["submit_mobile_verification_response"][
        "verificationToken"
    ]
    headers["x-user-name"] = user_name
    headers["x-verification-token"] = verification_token
    return headers


def concatenated_header_values_binded_signature(device_info, user_profile_id):
    concatenated_headers = ""
    headers_order_list = [
        "os",
        "os-build-number",
        "os-version",
        "device-brand-name",
        "device-type",
        "app-first-install-time",
        "app-version",
        "app-bundle-identifier",
        "app-build-version",
    ]
    for i, header in enumerate(headers_order_list):
        concatenated_headers += device_info[header]
        concatenated_headers += ":"
    current_epoch_ms = int(time.time()*1000)
    nearest_10_min_epoch = getNearest600Epoch(current_epoch_ms)
    concatenated_headers += str(nearest_10_min_epoch) + ":"
    concatenated_headers += user_profile_id
    return concatenated_headers


def get_nearest_10_min_epoch(current_epoch_ms):
    ten_mins_in_ms = 600*1000
    remainder = current_epoch_ms % ten_mins_in_ms
    nearest_10_min_epoch = current_epoch_ms - remainder
    return nearest_10_min_epoch


def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent = 65537,
        key_size = 4096
    )
    public_key = private_key.public_key()
    return private_key, public_key


def serialize_public_key(public_key: rsa.RSAPublicKey) -> str:
    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')
    return pem_public_key


def create_signature(private_key: rsa.RSAPrivateKey, message: str) -> str:
    message_bytes = message.encode("utf-8")
    signature_bytes = private_key.sign(
        message_bytes,
        padding.PKCS1v15(),
        hashes.SHA512()
    )
    return base64.b64encode(signature_bytes).decode("utf-8")


def concatenated_header_values_initiation_signature(device_info):
    concatenated_headers = ""
    headers_order_list = [
        "os",
        "os-build-number",
        "os-version",
        "device-brand-name",
        "device-type",
        "app-first-install-time",
        "app-version",
        "app-bundle-identifier",
        "app-build-version",
        "x-epoch",
    ]
    for i, header in enumerate(headers_order_list):
        if header == "x-epoch":
            currentEpoch = device_info["x-epoch"]
            nearest600Epoch = getNearest600Epoch(currentEpoch)
            concatenated_headers += str(nearest600Epoch)
        else:
            concatenated_headers += device_info[header]
        if i != len(headers_order_list) - 1:
            concatenated_headers += ":"
    return concatenated_headers


def getNearest600Epoch(currentEpoch):
    secondsElapsedAfter600 = currentEpoch % (600 * 1000)
    return currentEpoch - secondsElapsedAfter600


def get_initiation_signature(device_info):
    concatenated_header = concatenated_header_values_initiation_signature(device_info)
    encryptionSaltSecret = generateSecret(concatenated_header, 3)
    secret_key = str(encryptionSaltSecret).encode("utf-8")
    message = concatenated_header.encode("utf-8")
    hmac_hash = hmac.new(secret_key, message, hashlib.sha256).hexdigest()
    return hmac_hash


def generateSecret(str, SECRET_MODULUS):
    byte_sum = sum(ord(c) for c in str)
    return byte_sum % SECRET_MODULUS


def generate_device_details():
    current_time = int(time.time()*1000)
    device_details = {
        "os": "Android",
        "os-build-number": "BP2A.250605.031.A3",
        "os-version": "16",
        "device-brand-name": "Google",
        "x-device-id": f"{get_rand_number(6)}",
        "device-type": "MOBILE",
        "app-first-install-time": str(current_time - (604800*1000)),  # Install time of one week ago
        "app-version": "2.1.202507030",
        "app-bundle-identifier": "com.hugosave.test",
        "app-build-version": "2025070801",
        "x-epoch": current_time,
        "x-location-coordinates": "31,72"
    }
    return device_details


def get_create_user_details(
    context,
    uid,
    user_name_type,
    legal_name,
    email,
    account_type,
    name,
    phone_number,
    referral_code,
    security_answers,
    non_security_answers,
    account_usage_selected_options,
):
    return {
        "name": name,
        "user_name_type": user_name_type,
        "user_name": context.data["users"][uid]["user_name"],
        "password": get_rand_number(6),
        "phone_number": phone_number,
        "account_type": account_type,
        "legal_name": legal_name,
        "email": email,
        "referral_code": referral_code,
        "security_answers": security_answers,
        "non_security_answers": non_security_answers,
        "accountUsageSelectedOptions": account_usage_selected_options,
    }

def get_presigned_url(context, uid, document_type, detail_type, proof_type, customer):
    if customer == "HUGOBANK":
        if proof_type == None:
            document_list = context.data["users"][uid]["initiate_journey_response"]["data"][detail_type]
        else:
            document_list = context.data["users"][uid]["initiate_journey_response"]["data"][detail_type][proof_type]
        if document_type in document_list:
            return{"file_path": "tests/api/distribute/steps/test-docs/Front.png", "upload_url": document_list[document_type]["uploadUrl"]}

    else:
        return{"file_path": "tests/api/distribute/steps/test-docs/Front.png", "upload_url": context.data["users"][uid]["initiate_journey_response"]["data"][detail_type]["uploadUrl"]}


def get_hugosave_additional_details_data(context, uid):
    return {"data": json.dumps({"same_as_registered_address": True})}


def get_cdv_additional_details_data(context, uid):
    return {
        "data": json.dumps(
            {
                "current_address": {
                    "address_line_1": "123 ORCHARD ROAD",
                    "address_line_2": "#10-05",
                    "address_line_3": "ORCHARD TOWERS",
                    "address_line_4": "",
                    "city": "Singapore",
                    "state": "Singapore",
                    "country_code": "SGP",
                    "local_code": "238858"
                },
                "address_proof": {
                    "type": "NATIONAL_IDENTITY",
                },
                "citizenships": ["ABW"]
            }
        )
    }


def get_verify_income_details(context, uid):
    return {
        "data": json.dumps(
            {
                "source_category": "SPONSOR_STUDENT"
            }
        )
    }


def get_passcode_body(context, user_profile_identifier):
    verification_token = context.data["users"][user_profile_identifier][
        "journey_initiate_response"
    ]["data"]["verificationToken"]
    passcode = get_passcode(context, user_profile_identifier)
    return {
        "data": json.dumps(
            {"verification_token": verification_token, "passcode": passcode}
        )
    }


def get_other_journey_body(context, user_profile_identifier):
    submit_session_id = context.data["users"][user_profile_identifier][
        "journey_initiate_response"
    ]["data"]["sessionId"]
    return {"data": json.dumps({"session_id": submit_session_id, "otp": 123456})}


def get_trust_data(context, uid):
    agreements = context.data["users"][uid]["initiate_journey_response"]["data"][
        "agreements"
    ]
    if "agreements" in context.data["users"][uid]["initiate_journey_response"]["data"]:
        for agreement in agreements:
            agreement["accepted"] = True
    return {
        "data": json.dumps(
            {
                "video_url": context.data["users"][uid]["initiate_journey_response"][
                    "data"
                ]["videoUrl"],
                "agreements": agreements,
                "video_seen": True,
            }
        )
    }


def get_pk_account_details(context, bank_name):
    account_details = {}

    if bank_name == "Test Bank Raast":
        suffix = str(random.randint(0, 99999)).zfill(10)
        prefix = "102"
        account_number = prefix + suffix
        account_details = {
            "account_number": account_number,
            "bank_bic": "TESTRAAST",
        }
    elif bank_name == "Test Bank 1Link":
        suffix = str(random.randint(0, 99999)).zfill(9)
        prefix = "1010"
        account_number = prefix + suffix
        account_details = {
            "account_number": account_number,
            "bank_imd": "101010",
        }
    elif bank_name == "Test Bank Raast - 1Link":
        suffix = str(random.randint(0, 99999)).zfill(9)
        prefix = "102"
        account_number = prefix + suffix
        account_details = {
            "account_number": account_number,
            "bank_imd": "103030",
            "bank_bic": "TESTRAAST1LINK",
        }
    else:
        suffix = str(random.randint(0, 99999)).zfill(5)
        prefix = "100"
        account_number = prefix + suffix
        account_details = {
            "account_number": account_number,
            "bank_bic": "BAHLPKKA",
            "bank_imd": "627197"
        }
    return account_details


def get_default_data(context, uid):
    return {"data": json.dumps({})}


def get_mandate_payload(mandate_identifier: str) -> dict:
    return {
        "debtor_account_details": {
            "account_holder_name": "John",
            "country": "SGP",
            "currency": "SGD",
            "code_details": {
                "sg_bank_details": {
                    "swift_bic": "DBSSSGS0XXX"
                }
            }
        },
        "segment": "RETAIL"
    }


def extract_bank_details_only_field_names(payee_config_response):

    field_names = set()

    try:
        group_config_map = payee_config_response['data']['groupConfig']
        payment_method_key = next(iter(group_config_map))
        groups = group_config_map[payment_method_key]['groups']

        for group in groups:
            if group.get('groupName') == 'PayeeBankDetails':
                for field in group.get('fields', []):
                    field_name = field.get('fieldName')
                    if field_name:
                        field_names.add(field_name)
                break

    except Exception as e:
        print(f"Error extracting bank field names from config: {e}")
        return set()

    return field_names


def generate_random_word(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length)).capitalize()


def generate_random_number_string(length):
    first_digit = random.choice(string.digits.replace('0', ''))
    remaining_digits = ''.join(random.choice(string.digits) for _ in range(length - 1))
    return first_digit + remaining_digits


def generate_random_alpha_numeric(length):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def generate_random_test_data(field_names_set, country):
    test_data = {}

    for field_name in field_names_set:
        if field_name == "full_name":
            test_data[field_name] = f"{generate_random_word(5)} {generate_random_word(8)}"
        elif field_name == "account_number":
            test_data[field_name] = generate_random_number_string(10)
        elif field_name == "ach_routing_number":
            test_data[field_name] = generate_random_number_string(9)
        elif field_name == "ifsc":
            bank_codes = ['HDFC', 'ICIC', 'SBIN', 'YESB', 'KOTK', 'PUNB', 'UTIB']
            bank_code = random.choice(bank_codes)
            branch_code = generate_random_alpha_numeric(6)
            test_data[field_name] = f"{bank_code}0{branch_code}"
        elif field_name == "swift_bic":
            bank_code = ''.join(random.choice(string.ascii_uppercase) for _ in range(4))
            country_code = ''.join(random.choice(string.ascii_uppercase) for _ in range(2))
            location_code = generate_random_alpha_numeric(2)
            branch_code = generate_random_alpha_numeric(3)
            test_data[field_name] = f"{bank_code}{country_code}{location_code}{branch_code}"
        elif field_name == "iban":
            checksum_and_bank_code = generate_random_number_string(4)
            bban = generate_random_alpha_numeric(24)
            test_data[field_name] = f"ZZ{checksum_and_bank_code}{bban}"
        elif field_name == "bank_code":
            test_data[field_name] = generate_random_alpha_numeric(5)
        elif field_name == "bsb_code":
            test_data[field_name] = generate_random_number_string(6)
        elif field_name == "account_number":
            test_data[field_name] = generate_random_number_string(10)
        elif field_name == "institution_number":
            test_data[field_name] = generate_random_number_string(3)
        elif field_name == "transit_number":
            test_data[field_name] = generate_random_number_string(5)
        elif field_name == "wire_routing_number":
            test_data[field_name] = generate_random_number_string(9)
        elif field_name == "sort_code":
            test_data[field_name] = generate_random_number_string(6)
        else:
            test_data[field_name] = generate_random_word(12)

    return test_data


JOURNEY_DATA_BUILDERS = {
    "HUGOSAVE_ADDITIONAL_DETAILS": get_hugosave_additional_details_data,
    "HUGOSAVE_TRUST": get_trust_data,
    "PASSCODE": get_passcode,
    "CDV_ADDITIONAL_DETAILS": get_cdv_additional_details_data,
    "HUGOBANK_VERIFY_INCOME": get_verify_income_details
}


def get_device_info(context, uid):
    current_device = context.data["users"][uid]["current_device"]
    user_device_list = context.data["users"][uid]["user_devices"]
    return user_device_list[current_device]


def get_user_authorisation_token(context, uid):
    return context.data["users"][uid]["user_authorisation_token"]


def get_device_authentication_token(context, uid, device):
    return context.data["users"][uid]["user_devices"][device]["authentication_token"]


def get_device_id(context, uid, device):
    return context.data["users"][uid]["user_devices"][device]["x-device-id"]


def get_reward_id(context, uid):
    for reward in context.data["users"][uid]["userRewards"]:
        return reward["userRewardId"]


def get_user_document_id(context, uid, document_type, document_code):
    return context.data["users"][uid]["documents"][document_type][document_code]["user_document_id"]


def get_bill_payee_id(context, schedule_identifier, user_profile_identifier):
    return context.data["users"][user_profile_identifier]["biller-info"]["bill-payee-id"]


def get_payee_id(context, payee_identifier, user_profile_identifier):
    return context.data["users"][user_profile_identifier][payee_identifier]["payeeId"]


def get_invalid_location_headers(context, device_info):
    headers = get_user_name_verification_header(context, device_info)
    headers["x-location-coordinates"] = "1340,7887"
    return headers

def get_rand_email():
    user_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    domain = random.choice(["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"])
    return f"{user_name}@{domain}"


def get_portal_principle_id(context):

    if context.data["org_id"] == "HUGOSAVE_SG":
        return "7212248a-0b7f-4ac9-a0c2-52826d65b43c"
    elif context.data["customer"] == "CDV":
        return "3b4e6c8a-0d2f-421e-b9a7-5c8e2d3f1b09"
    else:
        return "7212248a-0b7f-4ac9-a0c2-52826d65b43c"


def get_credit_account_id(context, uid, product_code=None):
    credit_accounts = context.data["users"][uid].get("credit_accounts", [])

    for account in credit_accounts:
        if product_code:
            if account.get("productCode") == product_code:
                return account.get("creditAccountId")
        else:
            return account.get("creditAccountId")

    raise Exception(f"No matching credit account found for user {uid}")