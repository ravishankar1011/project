from behave import *
from hugoutils.utilities.dataclass_util import DataClassParser
from retry import retry

from tests.api.aggregate.cash import helper as cash_helper
from tests.api.aggregate.cash.cash_dataclass import (
    CashDevDepositRequestDTO
)

use_step_matcher("re")

@Given(
    "I deposit an amount of ([^']*) into ([^']*) using cash DevDeposit and expect the header status ([^']*)"
)
def deposit_using_cash_dev(
    context, amount: float, account_identifier: str, status_code: str
):
    request = context.request

    dev_deposit_dto = DataClassParser.parse_row(
        context.table.rows[0], CashDevDepositRequestDTO
    )

    cash_wallet_id = context.data[account_identifier].cash_wallet_id
    dev_deposit_dto.cash_wallet_id = cash_wallet_id
    dev_deposit_dto.amount = amount
    customer_profile_id = context.data[
        dev_deposit_dto.customer_profile_id
    ].customer_profile_id

    check_initial_balance_response = request.hugoserve_get_request(
        path=f"/cash/v1/cash-wallet/{cash_wallet_id}/balance",
        headers=cash_helper.__get_default_cash_headers(customer_profile_id),
    )
    assert (
        "data" in check_initial_balance_response
    ), f"\nExpected non empty data object, found empty. Response:{check_initial_balance_response}"

    initial_total_balance = check_initial_balance_response["data"]["total_balance"]
    initial_available_balance = check_initial_balance_response["data"][
        "available_balance"
    ]

    context.data["initial_total_balance_" + cash_wallet_id] = initial_total_balance
    context.data["initial_available_balance_" + cash_wallet_id] = initial_available_balance

    deposit_response = request.hugoserve_post_request(
        path=f"/cash/v1/dev/transaction/deposit",
        data=dev_deposit_dto.get_dict(),
        headers=cash_helper.__get_default_cash_headers(customer_profile_id),
    )
    assert deposit_response["headers"]["status_code"] == status_code
    if deposit_response["headers"]["status_code"] == "200":
        assert deposit_response["headers"]["message"] == "Success"


@Then(
    "I wait until max time to verify bank account ([^']*) with an increased balance of ([^']*) for customerProfileId ([^']*)"
)
def verify_bank_account_balance(
    context, identifier, amount_increased, customer_profile_identifier
):
    request = context.request
    customer_profile_id = context.data[customer_profile_identifier].customer_profile_id
    cash_wallet_id = context.data[identifier].cash_wallet_id

    expected_total_balance = float(
        context.data["initial_total_balance_" + cash_wallet_id]
    ) + float(amount_increased)
    expected_available_balance = float(
        context.data["initial_available_balance_" + cash_wallet_id]
    ) + float(amount_increased)

    @retry(
        AssertionError,
        tries=cash_helper.cash_providers_config["DBS Bank Ltd"]["max_wait_time"] / 5,
        delay=3,
        logger=None,
    )
    def retry_for_bank_account_status():
        response = request.hugoserve_get_request(
            path=f"/cash/v1/cash-wallet/{cash_wallet_id}/balance",
            headers=cash_helper.__get_default_cash_headers(customer_profile_id),
        )
        trace_id = response["headers"].get("trace_id", "N/A")

        assert "data" in response, (
            f"[TraceId: {trace_id}] [Cash Wallet Id: {cash_wallet_id}]\n"
            f"Expected non-empty data object, found empty. Response: {response}"
        )

        actual_total_balance = response["data"]["total_balance"]
        actual_available_balance = response["data"]["available_balance"]

        assert expected_total_balance == actual_total_balance, (
            f"[TraceId: {trace_id}] [AccountId: {cash_wallet_id}]\n"
            f"Expect total_balance: {expected_total_balance}\n"
            f"Actual total_balance: {actual_total_balance}"
        )

        assert expected_available_balance == actual_available_balance, (
            f"[TraceId: {trace_id}] [AccountId: {cash_wallet_id}]\n"
            f"Expect available_balance: {expected_available_balance}\n"
            f"Actual available_balance: {actual_available_balance}"
        )

    retry_for_bank_account_status()
