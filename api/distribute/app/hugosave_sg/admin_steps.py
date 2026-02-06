from behave import *
import tests.api.distribute.app_helper as ah
from tests.api.distribute.app_helper import get_portal_header
from tests.util.common_util import check_status_distribute
from retry import retry

use_step_matcher("re")


@Step("I ([^']*) the ([^']*) account for user ([^']*)")
def block_deposits(context, action,product_code, user_profile_identifier):
    request = context.request
    cash_wallet_id = ah.get_cash_wallet_id_by_product_code(context,user_profile_identifier,product_code)
    user_profile_id = ah.get_user_profile_id(user_profile_identifier,context)

    url = ah.cash_urls["update_cash_wallet_status"].replace("{cash-wallet-id}",cash_wallet_id)

    response = request.hugosave_put_request(
            path = url,
            headers=ah.get_portal_header(user_profile_id, context),
            data = { "account_status_action": action}
        )

    assert check_status_distribute(response, "200"), f"Failed to {action} : {response}"


@Step("I ([^']*) merchant transactions for ([^']*)")
def block_merchant_transactions(context, case, uid):
    request = context.request

    response = None
    headers=ah.get_user_header(context, uid)
    headers['x-enforce-auth'] = "False"
    if case == "block":
        url = ah.dev_urls["block_merchant_transactions"]
        response = request.hugosave_put_request(
            url,
            headers=headers,
        )
    elif case == "unblock":
        url = ah.dev_urls["unblock_merchant_transactions"]
        response = request.hugosave_delete_request(
            url,
            headers=headers,
        )

    assert check_status_distribute(response, "200"), f"Failed to {case} merchant transactions.\nReceived : {response}"


@Step("I ([^']*) the ([^']*) of ([^']*) for a user ([^']*) and expect a status code of ([^']*)")
def block_transactions(context, action ,target,product_code, uid, expected_status_code):
    request = context.request

    user_profile_id = ah.get_user_profile_id(uid,context)
    headers = get_portal_header(user_profile_id,context)
    cash_wallet_id = ah.get_cash_wallet_id_by_product_code(context,uid,product_code)

    body = {}
    if (target == "INTERNAL_DEBITS" and action == "BLOCK"):
        body = { "internal_debit_status_action" : "BLOCK_TRANSACTIONS"}

    elif (target == "INTERNAL_CREDITS" and action == "BLOCK"):
        body = { "internal_credit_status_action" : "BLOCK_TRANSACTIONS"}

    elif (target == "INTERNAL_CREDITS" and action == "UNBLOCK"):
        body = { "internal_credit_status_action" : "UNBLOCK_TRANSACTIONS" }

    elif (target == "INTERNAL_DEBITS" and action == "UNBLOCK"):
        body = { "internal_debit_status_action" : "UNBLOCK_TRANSACTIONS" }

    elif (target == "EXTERNAL_DEBITS" and action == "UNBLOCK"):
        body = { "external_debit_status_action" : "UNBLOCK_TRANSACTIONS" }

    elif (target == "EXTERNAL_DEBITS" and action == "BLOCK"):
        body = { "external_debit_status_action" : "BLOCK_TRANSACTIONS" }

    elif (target == "EXTERNAL_CREDITS" and action == "UNBLOCK"):
        body = { "external_credit_status_action" : "UNBLOCK_TRANSACTIONS" }

    elif (target == "EXTERNAL_CREDITS" and action == "BLOCK"):
        body = { "external_credit_status_action" : "BLOCK_TRANSACTIONS" }

    response = request.hugosave_put_request(
        path = ah.cash_urls["update_cash_wallet_txn_status"].replace("{cash-wallet-id}",cash_wallet_id),
        headers = headers,
        data = body
    )

    assert check_status_distribute(response, expected_status_code), f"Failed to {action} transactions.\nReceived : {response}"


@Step("I check the status of ([^']*) of ([^']*) for user ([^']*) to be ([^']*)")
def check_status(context , target , product_code , uid ,action):
    request = context.request

    cash_wallet_id = ah.get_cash_wallet_id_by_product_code(context,uid,product_code)

    index=""
    if (target == "INTERNAl_DEBITS"):
        index = "internalDebitStatus"
    elif (target == "INTERNAl_CREDITS"):
        index = "internalCreditStatus"
    elif (target == "EXTERNAL_CREDITS"):
        index = "externalCreditStatus"
    elif (target == "EXTERNAL_DEBITS"):
        index = "externalDebitStatus"

    @retry(AssertionError, tries=40, delay=5, logger=None)
    def retry_user_details():
        response = request.hugosave_get_request(
            path = ah.cash_urls["cash-wallet-details"].replace("{cash-wallet-id}",cash_wallet_id),
            headers = ah.get_user_header(context, uid)
        )

        if check_status_distribute(response, "200"):
            assert response['data'][index] == action,"Transaction status not Updated"

    retry_user_details()

@Step("I check the status of ([^']*) for user ([^']*) to be ([^']*)")
def check_status(context , product_code , uid ,action):
    request = context.request

    cash_wallet_id = ah.get_cash_wallet_id_by_product_code(context,uid,product_code)

    @retry(AssertionError, tries=40, delay=15, logger=None)
    def retry_user_details():
        response = request.hugosave_get_request(
            path = ah.cash_urls["cash-wallet-details"].replace("{cash-wallet-id}",cash_wallet_id),
            headers = ah.get_user_header(context, uid)
        )

        if check_status_distribute(response, "200"):
            assert (response['data']["cashWalletStatus"] == action), "Transaction status not Updated"

    retry_user_details()
