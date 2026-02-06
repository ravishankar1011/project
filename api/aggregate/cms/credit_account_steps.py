import uuid

from hugoutils.utilities.dataclass_util import DataClassParser

from tests.api.aggregate.cms import cms_helper
from tests.api.aggregate.cms.cms_dataclass import CreateCreditAccountRequestDTO
from behave import *
from retry import retry

from tests.util.common_util import check_status

use_step_matcher("re")


@Then(
    "I create below credit accounts and verify account status is ([^']*) and status code is ([^']*)"
)
def create_credit_account(context, expected_account_status, expected_status_code):
    request = context.request
    create_account_req_list = DataClassParser.parse_rows(
        context.table.rows, data_class=CreateCreditAccountRequestDTO
    )
    context.data = {} if context.data is None else context.data
    customer_profile_id = context.data["config_data"]["customer_profile_id"]
    for create_account_req in create_account_req_list:
        data = create_account_req.get_dict()
        if not create_account_req.product_id in context.data:
            data["product_id"] = str(uuid.uuid4())
        else:
            data["product_id"] = context.data[create_account_req.product_id]
        if create_account_req.end_customer_profile_id in context.data:
            data["end_customer_profile_id"] = context.data[
                create_account_req.end_customer_profile_id
            ].end_customer_profile_id
        else:
            data['end_customer_profile_id'] = str(uuid.uuid4())

        data['account_param'] = {
            "approved_limit": data["approved_limit"],
            "interest_rate": data["interest_rate"]
        }
        response = request.hugoserve_post_request(
            cms_helper.credit_account_urls["create"],
            data=data,
            headers=cms_helper.get_headers(customer_profile_id),
        )
        check_status(response, expected_status_code)
        if expected_status_code == "200":
            assert (
                    response["data"]["account_status"] == "ACCOUNT_INITIATED"
                    or response["data"]["account_status"] == expected_account_status
            )
            account_id = response["data"]["credit_account_id"]
            context.data[create_account_req.account_id] = account_id
            context.data["CAN"] = response["data"]["credit_account_number"]

        @retry(exceptions=AssertionError, tries=30, delay=2, logger=None)
        def retry_for_account_creation():
            response = request.hugoserve_get_request(
                cms_helper.credit_account_urls["get_details"].replace(
                    "$account_id$", account_id
                ),
                headers=cms_helper.get_headers(customer_profile_id),
            )
            check_status(response, "200")
            cms_helper.assert_values(
                "Account Status",
                account_id,
                expected_account_status,
                response["data"]["account_status"],
            )

        if (
                expected_status_code == "200"
                and response["data"]["account_status"] != expected_account_status
        ):
            retry_for_account_creation()


@Then("I create the following transaction codes and verify status code is ([^']*)")
def create_transaction_codes(context, expected_status_code):
    request = context.request
    context.data = {} if context.data is None else context.data
    customer_profile_id = context.data['config_data']['customer_profile_id']

    for row in context.table:
        txn_code_payload = {
            'transaction_code': row['transaction_code'],
            'iso_code': row.get('iso_code', ""),
            'description': row.get('description', "")
        }

        response = request.hugoserve_post_request(
            cms_helper.txn_code_urls['create'],
            data=txn_code_payload,
            headers=cms_helper.get_headers(customer_profile_id),
        )

        check_status(response, expected_status_code)


@Then("I create bucket config for product ([^']*) and verify status code is ([^']*)")
def create_bucket_config(context, product_id_key, expected_status_code):
    request = context.request
    context.data = {} if context.data is None else context.data
    customer_profile_id = context.data['config_data']['customer_profile_id']

    product_id = context.data.get(product_id_key, str(uuid.uuid4()))

    buckets = []
    for row in context.table:
        bucket = {
            'bucket_name': row['bucket_name'],
            'bucket_code': row['bucket_code'],
            'txn_codes': [code.strip() for code in row['txn_codes'].split(",")],
            'interest_type': row['interest_type'],
            'repayment_priority': int(row['repayment_priority']),
            'limit_percentage': float(row['limit_percentage']),
            'apr': float(row['apr'])
        }
        buckets.append(bucket)

    default_bucket_code = buckets[0]['bucket_code']

    payload = {
        'product_id': product_id,
        'buckets': buckets,
        'default_bucket_code': default_bucket_code,
        'interest_bucket_code': default_bucket_code
    }

    response = request.hugoserve_post_request(
        cms_helper.bucket_config_urls['create'],
        data=payload,
        headers=cms_helper.get_headers(customer_profile_id),
    )
    check_status(response, expected_status_code)

@Given(
    "I attempt to close the following credit accounts and verify status code is ([^']*)"
)
def close_credit_account(context, status_code):
    request = context.request
    customer_profile_id = context.data['config_data']['customer_profile_id']
    for row in context.table:
        credit_account_id = context.data.get(row['account_id'])
        if credit_account_id is None:
            credit_account_id = str(uuid.uuid4())
        response = request.hugoserve_delete_request(
            cms_helper.credit_account_urls["close"].replace("$account_id$", credit_account_id),
            headers=cms_helper.get_headers(customer_profile_id),
        )
        assert response.get("headers", {}).get("status_code") == status_code, "Expected status_code 200"
        if status_code == 200:
            assert response.get("data", {}).get("account_status") ==  row['account_status'], "Account status is not 'ACCOUNT_CLOSED'"
