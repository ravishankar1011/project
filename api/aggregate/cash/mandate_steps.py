import time

from hugoutils.utilities.dataclass_util import DataClassParser
from retry import retry

from tests.api.aggregate.cash.cash_dataclass import MandateTransactionRequestDTO, MandateRequestDTO
from behave import *
import tests.api.aggregate.cash.helper as cash_helper

use_step_matcher("re")


@Given(
    "I create a Mandate ([^']*) on Cash Wallet ([^']*) Customer Profile ([^']*) and expect header status code as ([^']*) and mandate status as ([^']*)"
)
def create_mandate_on_cash_wallet(
        context,
        mandate_identifier: str,
        cash_wallet_identifier: str,
        customer_profile_identifier: str,
        status_code: str,
        mandate_status: str
):
    request = context.request
    customer_profile_id = context.data[customer_profile_identifier].customer_profile_id

    mandate_request_dto = DataClassParser.parse_row(
        context.table.rows[0], data_class=MandateRequestDTO
    )

    mandate_request_dto.cash_wallet_id = context.data[cash_wallet_identifier].cash_wallet_id
    mandate_request_dto.debtor_account_details = {
        "account_holder_name": "MDT",
        "country": "SGP",
        "currency": "SGD",
        "code_details": {
            "sg_bank_details": {
                "account_number": "1234567890",
                "swift_bic": "DBSSSGS0XXX"
            }
        }
    }

    response = request.hugoserve_post_request(
        path="/cash/v1/mandate",
        data=mandate_request_dto.get_dict(),
        headers=cash_helper.__get_default_cash_headers(customer_profile_id),
    )

    assert (
            response["headers"]["status_code"] == status_code
    ), (
        f"\nExpect Status Code: {status_code}"
        f"\nActual Status Code: {response['headers']['status_code']}"
    )

    if response["headers"]["status_code"] == "200":
        assert (
                response["data"]["mandate_status"] == mandate_status
        ), (
            f"\nExpected Status: {mandate_status}"
            f"\nActual Status: {response['data']['mandate_status']}"
        )
        context.data[mandate_identifier] = response["data"]["mandate_id"]


@Then("I authorize the Mandate ([^']*) for Customer profile ([^']*) and expect header status code as ([^']*)")
def authorise_mandate(
        context,
        mandate_identifier: str,
        customer_profile_identifier: str,
        status_code: str
):
    request = context.request
    customer_profile_id = context.data[customer_profile_identifier].customer_profile_id

    mandate_id = context.data[mandate_identifier]

    response = request.hugoserve_post_request(
        path=f"/cash/v1/dev/mandate/{mandate_id}/authorize",
        headers=cash_helper.__get_default_cash_headers(customer_profile_id),
    )

    assert (
            response["headers"]["status_code"] == status_code
    ), (
        f"\nExpect Status Code: {status_code}"
        f"\nActual Status Code: {response['headers']['status_code']}"
    )

    time.sleep(3)


@Then("I accept the Mandate ([^']*) for Customer profile ([^']*) and expect header status code as ([^']*)")
def accept_mandate(
        context,
        mandate_identifier: str,
        customer_profile_identifier: str,
        status_code: str
):
    request = context.request
    customer_profile_id = context.data[customer_profile_identifier].customer_profile_id

    mandate_id = context.data[mandate_identifier]

    response = request.hugoserve_post_request(
        path=f"/cash/v1/dev/mandate/{mandate_id}/accept",
        headers=cash_helper.__get_default_cash_headers(customer_profile_id),
    )

    assert (
            response["headers"]["status_code"] == status_code
    ), (
        f"\nExpect Status Code: {status_code}"
        f"\nActual Status Code: {response['headers']['status_code']}"
    )


@Then("I verify Mandate ([^']*) for Customer Profile ([^']*) is created and expect header status code as ([^']*) and mandate_status as ([^']*)")
def get_mandate(
        context,
        mandate_identifier: str,
        customer_profile_identifier: str,
        status_code: str,
        mandate_status: str
):
    request = context.request
    customer_profile_id = context.data[customer_profile_identifier].customer_profile_id

    mandate_id = context.data[mandate_identifier]

    @retry(
        AssertionError,
        tries=10,
        delay=5,
        logger=None,
    )
    def retry_for_mandate_status():
        response = request.hugoserve_get_request(
            path=f"/cash/v1/mandate/{mandate_id}",
            headers=cash_helper.__get_default_cash_headers(customer_profile_id),
        )

        assert (
                response["headers"]["status_code"] == status_code
        ), (
            f"\nExpect Status Code: {status_code}"
            f"\nActual Status Code: {response['headers']['status_code']}"
        )

        if response["headers"]["status_code"] == "200":
            assert (
                    response["data"]["mandate_status"] == mandate_status
            ), (
                f"\nExpected Status: {mandate_status}"
                f"\nActual Status: {response['data']['mandate_status']}"
            )
            context.data[mandate_identifier] = response["data"]["mandate_id"]
    retry_for_mandate_status()


@Then("I initiate a Mandate Transaction ([^']*) with Mandate ([^']*) and Cash Wallet ([^']*) for Customer Profile ([^']*) with below details and expect header status code as ([^']*) and transaction status as ([^']*)")
def mandate_transaction(
        context,
        transaction_identifier: str,
        mandate_identifier: str,
        cash_wallet_identifier: str,
        customer_profile_identifier: str,
        status_code: str,
        transaction_status: str
):
    request = context.request
    customer_profile_id = context.data[customer_profile_identifier].customer_profile_id


    mandate_transaction_request_dto = DataClassParser.parse_row(
        context.table.rows[0], data_class=MandateTransactionRequestDTO
    )

    mandate_transaction_request_dto.cash_wallet_id = context.data[cash_wallet_identifier].cash_wallet_id
    mandate_transaction_request_dto.mandate_id = context.data[mandate_identifier]

    response = request.hugoserve_post_request(
        path=f"/cash/v1/transaction/mandate",
        data=mandate_transaction_request_dto.get_dict(),
        headers=cash_helper.__get_default_cash_headers(customer_profile_id),
    )

    assert (
            response["headers"]["status_code"] == status_code
    ), (
        f"\nExpect Status Code: {status_code}"
        f"\nActual Status Code: {response['headers']['status_code']}"
    )

    if status_code == "200":
        assert (
                response["data"]["transaction_status"] == transaction_status
        ), (
            f"\nExpected Status: {transaction_status}"
            f"\nActual Status: {response['data']['transaction_status']}"
        )
        context.data[transaction_identifier] = response["data"]["transaction_id"]
    else :
        assert (
                response["headers"]["message"] == transaction_status
        ), (
            f"\nExpected Error Message: {transaction_status}"
            f"\nActual Error Message: {response['headers']['message']}"
        )
