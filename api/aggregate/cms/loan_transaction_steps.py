from behave import *
from hugoutils.utilities.dataclass_util import DataClassParser
from retry import retry

import copy

from tests.api.aggregate.cms import cms_helper
from tests.api.aggregate.cms.cms_dataclass import LoanDisbursementRequestDTO, DevDepositRequestDTO
from tests.util.common_util import check_status

from json.decoder import JSONDecodeError

use_step_matcher("re")


def get_loan_account_balance(request, customer_profile_id, account_id):
    response = request.hugoserve_get_request(
        cms_helper.loan_account_urls["balance"].replace("$account_id$", account_id),
        headers=cms_helper.get_headers(customer_profile_id),
    )
    check_status(response, "200")
    return response["data"]


def assert_balance_settlement_status(response, settled_amount, original_la_available_balance):
    available_loan_balance = original_la_available_balance - settled_amount

    cms_helper.assert_values(
        "lent_balance_check", "", response["lent_balance"], settled_amount
    )
    cms_helper.assert_values(
        "recovered_balance_check", "", 0, response["recovered_balance"]
    )
    cms_helper.assert_values(
        "available_balance_check",
        "",
        response["available_balance"],
        available_loan_balance,
    )


def update_balance(ledger, amount, sign):
    if sign:
        ledger['total_balance'] += amount
        ledger['available_balance'] += amount
    else:
        ledger['total_balance'] = amount
        ledger['available_balance'] = amount
    return ledger


def adjust_ledger(key, is_credit, modified, remaining_amount):
    if key in modified:
        ledger = modified[key]
        if is_credit:
            ledger = update_balance(ledger, remaining_amount, True)
        else:
            diff = ledger['available_balance'] - remaining_amount
            ledger = update_balance(ledger, max(0, diff), False)
            remaining_amount = max(0, -diff)
        modified[key] = ledger
    return remaining_amount


def update_ledgers(ledgers, case, amount):
    modified = copy.deepcopy(ledgers)
    remaining_amount = amount

    if case == "partial_interest":
        adjust_ledger('LA_RECOVERED', True, modified, remaining_amount)
        adjust_ledger('LA_LENT_INTEREST', False, modified, remaining_amount)
    elif case == "la_opening":
        adjust_ledger('LA_LENT_PRINCIPAL', True, modified, remaining_amount)
        adjust_ledger('LA_AVAILABLE', False, modified, remaining_amount)
    elif case == "partial_principal" or case == "full_recovery":
        adjust_ledger('LA_RECOVERED', True, modified, remaining_amount)
        remaining_amount = adjust_ledger('LA_LENT_INTEREST', False, modified, remaining_amount)
        adjust_ledger('LA_LENT_PRINCIPAL', False, modified, remaining_amount)

    return modified


@Given("I fetch the original balance for the loan account and store it in the context")
def fetch_original_la_balance(context):
    request = context.request
    customer_profile_id = context.data["config_data"]["customer_profile_id"]
    loan_account_id = ""

    for row in context.table:
        loan_account_id = context.data[row["loan_account_id"]]

    response = get_loan_account_balance(request, customer_profile_id, loan_account_id)

    if "Loan_account_id" not in context.data:
        context.data["loan_account_id"] = {}

    if loan_account_id not in context.data["loan_account_id"]:
        context.data["loan_account_id"][loan_account_id] = {}

    if "available_original_balance" not in context.data["loan_account_id"][loan_account_id]:
        context.data["loan_account_id"][loan_account_id]["available_original_balance"] = response[
            "available_balance"
        ]


@Then("I create loan disbursement transaction and verify transaction status as ([^']*) and status code as ([^']*)")
def initiate_loan_disbursement(context, expected_status, expected_status_code):
    request = context.request
    customer_profile_id = context.data['config_data']['customer_profile_id']

    initiate_la_disbursement_list = DataClassParser.parse_rows(
        context.table.rows, data_class=LoanDisbursementRequestDTO
    )
    loan_account_id = ""

    for row in context.table:
        if row["loan_account_id"] != "EMPTY":
            loan_account_id = row["loan_account_id"]

    for initiate_la_disbursement in initiate_la_disbursement_list:
        if (
                initiate_la_disbursement.loan_account_id in context.data
                and context.data[initiate_la_disbursement.loan_account_id]
        ):
            loan_account_id = context.data[initiate_la_disbursement.loan_account_id]

        response = request.hugoserve_post_request(
            cms_helper.loan_disbursement_urls["initiate"],
            data=initiate_la_disbursement.get_dict(loan_account_id),
            headers=cms_helper.get_headers(customer_profile_id, "CUSTOMER"),
        )

        if expected_status_code != "200":
            check_status(response, expected_status_code)
        else:

            txn_id = response["data"]["transaction_id"]
            if txn_id:
                if "transactions" not in context.data["loan_account_id"][loan_account_id]:
                    context.data["loan_account_id"][loan_account_id]["transactions"] = []

                context.data["loan_account_id"][loan_account_id]["transactions"].append(
                    {"txn_id": txn_id, "amount": initiate_la_disbursement.amount}
                )
            else:
                raise Exception("Transaction ID not found in the response")

            check_status(response, expected_status_code)

            @retry(exceptions=AssertionError, tries=120, delay=2, logger=None)
            def retry_for_loan_txn_get_status():
                get_response = request.hugoserve_get_request(
                    cms_helper.loan_disbursement_urls["get"].replace("$transaction_id$", txn_id),
                    headers=cms_helper.get_headers(customer_profile_id),
                )
                cms_helper.assert_values(
                    "transaction_status",
                    txn_id,
                    expected_status,
                    get_response["data"]["txn_status"],
                )

            retry_for_loan_txn_get_status()


@Then(
    "I verify the loan account balance after the transaction and status code as ([^']*)"
)
def verify_latest_la_balance(context, expected_status_code):
    request = context.request
    customer_profile_id = context.data["config_data"]["customer_profile_id"]
    loan_account_id = ""

    for row in context.table:
        loan_account_id = context.data[row["loan_account_id"]]

    original_la_available_balance = context.data["loan_account_id"][loan_account_id]["available_original_balance"]

    transactions = list(context.data["loan_account_id"][loan_account_id]["transactions"])
    settled_amount = sum(txn["amount"] for txn in transactions)

    response = get_loan_account_balance(request, customer_profile_id, loan_account_id)
    assert_balance_settlement_status(response, settled_amount, original_la_available_balance)


@Then("I initiate interest transaction and verify status code as ([^']*)")
def initiate_interest_transaction(context, expected_status_code):
    request = context.request
    customer_profile_id = context.data["config_data"]["customer_profile_id"]

    for row in context.table:
        loan_account_id = context.data[row["loan_account_id"]]
        response = request.hugoserve_post_request(
            cms_helper.dev_urls["initiate_interest_txn"].replace("$loan_account_id$", loan_account_id),
            headers=cms_helper.get_headers(customer_profile_id),
        )
        check_status(response, expected_status_code)


@Then(
    "I Initiate Dev LA Repayment and verify transaction status as ([^']*) and status code as ([^']*)"
)
def verify_payment_dev_deposit_repayment(context, expected_txn_status, expected_status_code):
    request = context.request
    customer_profile_id = ""
    purpose = ""
    amount = context.table[0]["amount"]

    if context.table[0]["customer_profile_id"] != "EMPTY":
        customer_profile_id = context.data["config_data"]["customer_profile_id"]

    if context.table[0]["purpose"] != "EMPTY":
        purpose = context.data.get(context.table[0]["purpose"])

    dev_deposit_repayment_data_rows = DataClassParser.parse_rows(
        context.table.rows, data_class=DevDepositRequestDTO
    )

    for dev_deposit_repayment_data in dev_deposit_repayment_data_rows:

        data = dev_deposit_repayment_data.get_dict(customer_profile_id)

        data["purpose"] = purpose

        if dev_deposit_repayment_data:
            response = request.hugoserve_post_request(
                cms_helper.dev_urls["deposit_funds"],
                data=data,
            )

            check_status(response, expected_status_code)
            context.data.setdefault("fund_account", {})["fund_txn_amount"] = amount


@Given("I fetch the original ledgers balances for loan account and verify status code as ([^']*)")
def fetch_original_ledger_balances(context, expected_status_code):
    request = context.request
    customer_profile_id = context.data["config_data"]["customer_profile_id"]

    for row in context.table:
        loan_account_id = context.data.get(row["loan_account_id"])

        @retry(exceptions=(AssertionError, JSONDecodeError), tries=120, delay=2, logger=None)
        def retry_for_ledger_balance():
            url = (
                cms_helper.dev_urls["ledger_balance"].replace("$account_id$", loan_account_id).replace("$product_type$",
                                                                                                         "LOAN_ACCOUNT"))
            headers = cms_helper.get_headers(customer_profile_id)
            response = request.hugoserve_get_request(url, headers=headers)

            check_status(response, expected_status_code)

            ledgers_dict = {
                ledger['ledger_type']: {
                    'ledger_id': ledger['ledger_id'],
                    'total_balance': float(ledger['total_balance']),
                    'available_balance': float(ledger['available_balance'])
                } for ledger in response['data']['ledger_balances']
            }

            context.data['ledgers'] = ledgers_dict

        retry_for_ledger_balance()


@Then("I fetch and verify the latest ledgers balances for loan account and verify status code as ([^']*)")
def fetch_latest_ledger_balances(context, expected_status_code):
    request = context.request
    customer_profile_id = context.data["config_data"]["customer_profile_id"]

    for row in context.table:
        loan_account_id = context.data.get(row["loan_account_id"])
        case = row["case"]

        @retry(exceptions=(AssertionError, JSONDecodeError), tries=2, delay=2, logger=None)
        def retry_for_ledger_balance():
            url = (
                cms_helper.dev_urls["ledger_balance"].replace("$account_id$", loan_account_id).replace("$product_type$",
                                                                                                         "LOAN_ACCOUNT"))
            headers = cms_helper.get_headers(customer_profile_id)
            response = request.hugoserve_get_request(url, headers=headers)

            check_status(response, expected_status_code)

            old_ledgers = copy.deepcopy(context.data['ledgers'])

            if "amount" in row and row["amount"]:
                amount = float(row["amount"])
            else:
                amount = float(context.data.get("fund_account", {}).get("fund_txn_amount", 0))

            updated_ledgers = update_ledgers(old_ledgers, case, amount)

            latest_ledgers = {
                ledger['ledger_type']: {
                    'ledger_id': ledger['ledger_id'],
                    'total_balance': float(ledger['total_balance']),
                    'available_balance': float(ledger['available_balance'])
                } for ledger in response['data']['ledger_balances']
            }

            for key in ['LA_AVAILABLE', 'LA_LENT_INTEREST', 'LA_LENT_PRINCIPAL', 'LA_RECOVERED']:
                if key in updated_ledgers:
                    cms_helper.assert_values('total_balance', "tb", round(updated_ledgers[key]['total_balance'],2),
                                             round(latest_ledgers[key]['total_balance'],2))
                    cms_helper.assert_values('available_balance', "ab", round(updated_ledgers[key]['available_balance'],2),
                                             round(latest_ledgers[key]['available_balance'],2))

        retry_for_ledger_balance()
