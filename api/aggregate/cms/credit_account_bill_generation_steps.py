from datetime import datetime
from time import sleep

from behave import *
from dateutil.relativedelta import relativedelta
from retry import retry

from tests.api.aggregate.cms import cms_helper
from tests.util.common_util import check_status

use_step_matcher("re")

@Given("I register KMS Namespace for CMS and verify status code as ([^']*)")
def register_kms_namespace(context, expected_status_code):

    customer_profile_id = context.data['config_data']['customer_profile_id']
    request = context.request

    response = request.hugoserve_post_request(
        cms_helper.admin_urls["register_kms_namespace"],
        headers=cms_helper.get_headers(customer_profile_id),
    )

    check_status(response, expected_status_code)


@Given(
    "I have mocked the following transactions for ([^']*) in the current billing cycle and status code is ([^']*)"
)
def create_mock_transactions(context, account_id, expected_status_code):
    request = context.request
    context.data = {} if context.data is None else context.data
    customer_profile_id = context.data['config_data']['customer_profile_id']
    mock_transactions = []
    credit_account_id = context.data.get(account_id)
    today = datetime.utcnow()
    for row in context.table:
        day = int(row["day"])
        months = int(row.get("months_to_shift", 0))
        direction = row.get("month_direction", "CURRENT").upper()
        if direction == "PAST":
            txn_date = today.replace(day=1) - relativedelta(months=months)
        elif direction == "FUTURE":
            txn_date = today.replace(day=1) + relativedelta(months=months)
        else:  # CURRENT_MONTH
            txn_date = today
        txn_datetime = txn_date.replace(day=day, hour=10, minute=40, second=26)
        txn_time_iso = txn_datetime.isoformat() + "Z"
        transaction = {
            'amount':row['amount'],
            'txn_type': row['txn_type'],
            'txn_time': txn_time_iso,
            'txn_code': row['txn_code'],
            'txn_status': row['txn_status'],
        }
        mock_transactions.append(transaction)
    payload = {
        'credit_account_id': credit_account_id,
        'receiver': {
            "account_holder_name": "HUGOHUB",
            "country": "SGP",
            "currency": "SGD",
            "code_details": {"sg_bank_details": {
                "swift_bic": "DBSSSGSGXXX",
                "account_number": "123456789",
            }
            }
        },
        'mock_txns' : mock_transactions
    }
    response = request.hugoserve_post_request(
            cms_helper.dev_urls['mock_transaction'],
            data=payload,
            headers=cms_helper.get_headers(customer_profile_id),
        )
    check_status(response, expected_status_code)
    wait_until_all_mock_transactions_are_settled(
            context,
            request,
            credit_account_id,
            mock_transactions,
            customer_profile_id
    )

@retry(exceptions=AssertionError, tries=25, delay=2, logger=None)
def wait_until_all_mock_transactions_are_settled(context, request, credit_account_id, expected_txns, customer_profile_id):
    response = request.hugoserve_get_request(
        cms_helper.credit_account_urls["credit_account_transactions"].replace("$account_id$", credit_account_id),
        headers=cms_helper.get_headers(customer_profile_id, origin="CUSTOMER"),
    )

    all_actual_transactions = response["data"]["transactions"]
    expected_set = {
        (float(txn["amount"]), txn["txn_type"], txn["txn_status"]) for txn in expected_txns
    }
    settled_actual_set = {
        (float(txn["amount"]), txn["txn_type"], txn["txn_status"])
        for txn in all_actual_transactions
    }
    assert expected_set.issubset(settled_actual_set), f"Still waiting for transactions. Got settled: {settled_actual_set}"

    updated_mock_txns = []
    remaining_actuals = all_actual_transactions.copy()

    for expected in expected_txns:
        match = next(
            (
                actual for actual in remaining_actuals
                if float(actual["amount"]) == float(expected["amount"])
                   and actual["txn_type"] == expected["txn_type"]
                   and actual["txn_status"] == expected["txn_status"]
            ),
            None
        )
        if match:
            updated = expected.copy()
            updated["txn_id"] = match["transaction_id"]
            updated_mock_txns.append(updated)
            remaining_actuals.remove(match)
        else:
            updated_mock_txns.append(expected)

    context.data["account_id"] = context.data.get("account_id", {})
    context.data["account_id"][credit_account_id] = context.data["account_id"].get(credit_account_id, {})
    context.data["account_id"][credit_account_id]["transactions"] = updated_mock_txns


@Then("I Wait some time to get the transactions updated")
def wait_some_time(context):
    sleep(10)


@when("I generate the credit bill for account ([^']*) and verify status code is ([^']*)")
def generate_bill(context, credit_account_id,expected_status_code):
    request = context.request
    credit_account_id = context.data.get(credit_account_id)
    customer_profile_id = context.data['config_data']['customer_profile_id']
    bill_date = datetime.utcnow().replace(day = 1)
    bill_date_str = bill_date.isoformat() + "Z"
    payload = {
        "account_id": credit_account_id,
        "bill_date": bill_date_str
    }
    response = request.hugoserve_post_request(
        cms_helper.dev_urls['generate_bill'],
        data=payload,
        headers=cms_helper.get_headers(customer_profile_id),
    )

    assert response["headers"]["status_code"] == expected_status_code, "Bill generation failed"
    if expected_status_code == "200":
        tad = float(context.table[0]['tad'])
        if tad == 0:
            retry_for_bill_generation(request, credit_account_id, customer_profile_id, 0)
        else:
            retry_for_bill_generation(request, credit_account_id, customer_profile_id)
            verify_interest_txn(request, credit_account_id, customer_profile_id)


@retry(exceptions=AssertionError, tries=25, delay=2, logger=None)
def retry_for_bill_generation(request, credit_account_id, customer_profile_id, total_amount_due=None):
    url = cms_helper.credit_account_urls["get_latest_bill"].replace("$account_id$", credit_account_id)
    response = request.hugoserve_get_request(
        url,
        headers=cms_helper.get_headers(customer_profile_id),
    )
    assert response["headers"]["status_code"] == "200", "Fetching latest bill failed"
    bill = response["data"]
    assert bill is not None, "No bill found in latest-bill response"
    status = bill["bill_status"]
    assert status == "BILL_GENERATED", f"Expected bill_status BILL_GENERATED, got {status}"
    if total_amount_due is not None:
        assert total_amount_due == bill["total_amount_due"], "Expected Total Amount Due is Different"


def verify_interest_txn(request, credit_account_id, customer_profile_id):
    response = request.hugoserve_get_request(
        cms_helper.credit_account_urls["credit_account_transactions"].replace("$account_id$", credit_account_id),
        headers=cms_helper.get_headers(customer_profile_id, origin="CUSTOMER"),
    )
    transactions = response["data"]["transactions"]
    interest_txn = None
    for txn in transactions:
        if txn["sub_txn_type"] == "INTEREST":
            interest_txn = txn
            break
    assert interest_txn is not None, "No interest transaction found in response"
    assert interest_txn["txn_status"] == "TRANSACTION_SETTLED"
