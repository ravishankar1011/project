import random

from hugoutils.utilities.dataclass_util import DataClassParser
from tests.api.aggregate.cash import helper as cash_helper
from tests.api.aggregate.cash.cash_dataclass import (
    CancelTransactionRequestDTO,
    CloseTransactionRequestDTO,
    InitiateTransactionRequestDTO,
    RefundRequestDTO,
    SettleTransactionRequestDTO,
    UpdateTransactionRequestDTO,
)
import asyncio
from behave import *
from retry import retry

use_step_matcher("re")


@Then(
    "I wait until max time to verify the transaction ([^']*) status as ([^']*) for customerProfileId ([^']*)"
)
def wait_and_verify_transaction_status(
        context, identifier: str, transaction_status: str, customer_profile_identifier: str
):
    request = context.request
    customer_profile_id = context.data[customer_profile_identifier].customer_profile_id
    try:
        transaction_id = context.data[identifier]
    except:
        print(f"\n {identifier} not present in context so ignoring")

    @retry(
        AssertionError,
        tries=40,
        delay=5,
        logger=None,
    )
    def retry_for_transaction_status():
        response = request.hugoserve_get_request(
            f"/cash/v1/transaction/{transaction_id}",
            headers=cash_helper.__get_default_cash_headers(customer_profile_id),
        )

        assert response["headers"]["status_code"] == "200", (
            f"[TraceId: {response['headers']['trace_id']}]\n"
            f"Expect status_code: 200\n"
            f"Actual status_code: {response['headers']['status_code']}"
        )

        assert response["data"] is not None
        assert response["data"]["transaction_status"] == transaction_status
        if response["data"] is not None:
            assert response["data"]["transaction_status"] == transaction_status, (
                f"\nExpect data.transaction_status: {transaction_status}"
                f"\nActual data.transaction_status: {response['data']['transaction_status']}, data: {response['data']}"
            )

        # Validate other fields values

    retry_for_transaction_status()


@Then(
    "I initiate refund for transaction with below details expect the header statuscode ([^']*)"
)
def refund_transaction(context, status_code):
    request = context.request

    refund_tx_request_dto = DataClassParser.parse_row(
        context.table.rows[0], RefundRequestDTO
    )
    refund_tx_request_dto.original_transaction_id = context.data[
        refund_tx_request_dto.original_transaction_id
    ]

    refund_tx_request_dto.customer_profile_id = context.data[
        refund_tx_request_dto.customer_profile_id
    ].customer_profile_id

    response = request.hugoserve_post_request(
        path=f"/cash/v1/transaction/refund",
        data=refund_tx_request_dto.get_dict(),
        headers=cash_helper.__get_default_cash_headers(
            refund_tx_request_dto.customer_profile_id
        ),
    )

    assert response["headers"]["status_code"] == status_code, (
        f"[TraceId: {response['headers']['trace_id']}]\n"
        f"Expect status_code: {status_code}\n"
        f"Actual status_code: {response['headers']['status_code']}"
    )

    if response["headers"]["status_code"] == "200":
        assert "transaction_id" in response["data"], (
            f"\nExpected data object contains transaction_id"
            f"\nActual data: {response['data']}"
        )

    context.data["TxId2"] = response["data"]["transaction_id"]

    assert response["data"]["transaction_status"] == "TRANSACTION_PENDING", (
        f"\nExpect data.account_status: TRANSACTION_PENDING"
        f"\nActual data.account_status: {response['data']['transaction_status']}, data: {response['data']}"
    )


@Then(
    "I initiate transaction to transfer funds with below details and expect the header statuscode ([^']*) and transaction status as ([^']*)"
)
def initiate_transaction_and_verify_status(context, status_code, txn_status):
    request = context.request

    initiate_tx_request_dto = DataClassParser.parse_row(
        context.table.rows[0], InitiateTransactionRequestDTO
    )

    if context.table.rows[0]["receiver_account_id"] == "":
        transfer_out_details = {
            "account_holder_name": "Jane Smith",
            "country": "SGP",
            "currency": "SGD",
            "code_details": {
                "sg_bank_details": {
                    "account_number": "9876543210",
                    "swift_bic": "DBSSSGSGXXX",
                }
            },
        }
    else:
        cash_wallet_details = context.data[
            context.table.rows[0]["receiver_account_id"]
        ].cash_wallet_details
        transfer_out_details = {
            "account_holder_name": cash_wallet_details.account_holder_name,
            "country": cash_wallet_details.country,
            "currency": cash_wallet_details.currency,
            "code_details": {
                "sg_bank_details": {
                    "account_number": cash_wallet_details.code_details.sg_code_details.account_number,
                    "swift_bic": cash_wallet_details.code_details.sg_code_details.swift_bic,
                }
            },
        }

    initiate_tx_request_dto.transfer_out_details = transfer_out_details

    if initiate_tx_request_dto.cash_wallet_id:
        initiate_tx_request_dto.cash_wallet_id = context.data[
            initiate_tx_request_dto.cash_wallet_id
        ].cash_wallet_id
    else:
        initiate_tx_request_dto.cash_account_id = context.data[
            initiate_tx_request_dto.cash_account_id
        ]

    initiate_tx_request_dto.customer_profile_id = context.data[
        initiate_tx_request_dto.customer_profile_id
    ].customer_profile_id

    if "idempotency_key" in context.table.headings:
        idempotency_key_identifier = context.table.rows[0]["idempotency_key"]
        try:
            idempotency_key = context.data[idempotency_key_identifier]
        except:
            idempotency_key = str(random.randint(1, 99999999))
            context.data[context.table.rows[0]["idempotency_key"]] = idempotency_key
    else:
        idempotency_key = initiate_tx_request_dto.idempotency_key

    response = request.hugoserve_post_request(
        path=f"/cash/v1/transaction/initiate",
        data=initiate_tx_request_dto.get_dict(),
        headers=cash_helper.__get_default_cash_headers(
            initiate_tx_request_dto.customer_profile_id, idempotency_key
        ),
    )

    assert response["headers"]["status_code"] == status_code, (
        f"[TraceId: {response['headers']['trace_id']}]\n"
        f"Expect status_code: {status_code}\n"
        f"Actual status_code: {response['headers']['status_code']}"
    )

    if response["headers"]["status_code"] == "200":
        assert response["headers"]["message"] == "Success"

        assert response["data"]["transaction_status"] == txn_status
        assert (
                "data" in response
        ), f"\nExpected non-empty data object, found empty. Response:{response}"

        assert "transaction_id" in response["data"], (
            f"\nExpected data object contains transaction_id"
            f"\nActual data: {response['data']}"
        )
        initiate_tx_request_dto.transaction_id = response["data"]["transaction_id"]
        context.data[initiate_tx_request_dto.identifier] = (
            initiate_tx_request_dto.transaction_id
        )


@Then(
    "I initiate transaction to transfer funds with below details and expect the header statuscode ([^']*)"
)
def initiate_transaction_and_verify_status(context, status_code):
    request = context.request

    initiate_tx_request_dto = DataClassParser.parse_row(
        context.table.rows[0], InitiateTransactionRequestDTO
    )

    if context.table.rows[0]["receiver_account_id"] == "":
        transfer_out_details = {
            "account_holder_name": "Jane Smith",
            "country": "SGP",
            "currency": "SGD",
            "code_details": {
                "sg_bank_details": {
                    "account_number": "9876543210",
                    "swift_bic": "DBSSSGSGXXX",
                }
            },
        }
    else:
        cash_wallet_details = context.data[
            context.table.rows[0]["receiver_account_id"]
        ].cash_wallet_details
        transfer_out_details = {
            "account_holder_name": cash_wallet_details.account_holder_name,
            "country": cash_wallet_details.country,
            "currency": cash_wallet_details.currency,
            "code_details": {
                "sg_bank_details": {
                    "account_number": cash_wallet_details.code_details.sg_code_details.account_number,
                    "swift_bic": cash_wallet_details.code_details.sg_code_details.swift_bic,
                }
            },
        }
    initiate_tx_request_dto.transfer_out_details = transfer_out_details

    initiate_tx_request_dto.cash_wallet_id = context.data[
        initiate_tx_request_dto.cash_wallet_id
    ].cash_wallet_id

    initiate_tx_request_dto.customer_profile_id = context.data[
        initiate_tx_request_dto.customer_profile_id
    ].customer_profile_id

    response = request.hugoserve_post_request(
        path=f"/cash/v1/transaction/initiate",
        data=initiate_tx_request_dto.get_dict(),
        headers=cash_helper.__get_default_cash_headers(
            initiate_tx_request_dto.customer_profile_id
        ),
    )

    assert response["headers"]["status_code"] == status_code, (
        f"[TraceId: {response['headers']['trace_id']}]\n"
        f"Expect status_code: {status_code}\n"
        f"Actual status_code: {response['headers']['status_code']}"
    )

    if response["headers"]["status_code"] == "200":
        assert response["headers"]["message"] == "Success"
        assert (
                "data" in response
        ), f"\nExpected non-empty data object, found empty. Response:{response}"

        assert "transaction_id" in response["data"], (
            f"\nExpected data object contains transaction_id"
            f"\nActual data: {response['data']}"
        )
        initiate_tx_request_dto.transaction_id = response["data"]["transaction_id"]
        context.data[initiate_tx_request_dto.identifier] = (
            initiate_tx_request_dto.transaction_id
        )


@Then(
    "I update transaction with transaction_id ([^']*) with the negative_transfer_allowed as ([^']*) and expect the header statuscode ([^']*) and transaction status as ([^']*)"
)
def update_transaction_and_verify_status(
        context,
        transaction_id: str,
        negative_transfer_allowed: bool,
        status_code: str,
        message,
):
    request = context.request

    update_tx_request_dto = DataClassParser.parse_row(
        context.table.rows[0], UpdateTransactionRequestDTO
    )

    update_tx_request_dto.transaction_id = context.data[
        update_tx_request_dto.transaction_id
    ]
    update_tx_request_dto.customer_profile_id = context.data[
        update_tx_request_dto.customer_profile_id
    ].customer_profile_id
    response = request.hugoserve_put_request(
        path=f"/cash/v1/transaction/{update_tx_request_dto.transaction_id}",
        data=update_tx_request_dto.get_dict(),
        headers=cash_helper.__get_default_cash_headers(
            update_tx_request_dto.customer_profile_id
        ),
    )

    assert response["headers"]["status_code"] == status_code, (
        f"[TraceId: {response['headers']['trace_id']}]\n"
        f"Expect status_code: {status_code}\n"
        f"Actual status_code: {response['headers']['status_code']}"
    )

    if response["headers"]["status_code"] == "200":
        assert response["headers"]["message"] == "Success"

        assert response["data"]["transaction_status"] == message
        assert (
                "data" in response
        ), f"\nExpected non-empty data object, found empty. Response:{response}"

        assert "transaction_id" in response["data"], (
            f"\nExpected data object contains transaction_id"
            f"\nActual data: {response['data']}"
        )
    else:
        assert response["headers"]["message"] == message


@Then(
    "I cancel transaction with transaction_id ([^']*) with the negative_transfer_allowed as ([^']*) and expect the header statuscode ([^']*) and transaction status as ([^']*)"
)
def cancel_transaction_and_verify_status(
        context,
        transaction_id: str,
        negative_transfer_allowed: bool,
        status_code: str,
        message,
):
    request = context.request

    cancel_txn_request_dto = DataClassParser.parse_row(
        context.table.rows[0], CancelTransactionRequestDTO
    )

    cancel_txn_request_dto.transaction_id = context.data[
        cancel_txn_request_dto.transaction_id
    ]
    cancel_txn_request_dto.customer_profile_id = context.data[
        cancel_txn_request_dto.customer_profile_id
    ].customer_profile_id
    response = request.hugoserve_put_request(
        path=f"/cash/v1/transaction/{cancel_txn_request_dto.transaction_id}/cancel",
        data=cancel_txn_request_dto.get_dict(),
        headers=cash_helper.__get_default_cash_headers(
            cancel_txn_request_dto.customer_profile_id
        ),
    )

    assert response["headers"]["status_code"] == status_code, (
        f"[TraceId: {response['headers']['trace_id']}]\n"
        f"Expect status_code: {status_code}\n"
        f"Actual status_code: {response['headers']['status_code']}"
    )

    if response["headers"]["status_code"] == "200":
        assert response["headers"]["message"] == "Success"

        assert response["data"]["transaction_status"] == message
        assert (
                "data" in response
        ), f"\nExpected non-empty data object, found empty. Response:{response}"

        assert "transaction_id" in response["data"], (
            f"\nExpected data object contains transaction_id"
            f"\nActual data: {response['data']}"
        )


@Then(
    "I close transaction with transaction_id ([^']*) with the negative_transfer_allowed as ([^']*) and expect the header statuscode ([^']*) and transaction status as ([^']*)"
)
def close_transaction_and_verify_status(
        context,
        transaction_id: str,
        negative_transfer_allowed: bool,
        status_code: str,
        message,
):
    request = context.request

    close_tx_request_dto = DataClassParser.parse_row(
        context.table.rows[0], CloseTransactionRequestDTO
    )

    close_tx_request_dto.transaction_id = context.data[
        close_tx_request_dto.transaction_id
    ]
    customer_profile_id = context.data[
        close_tx_request_dto.customer_profile_id
    ].customer_profile_id
    response = request.hugoserve_put_request(
        path=f"/cash/v1/transaction/{close_tx_request_dto.transaction_id}/close",
        data=close_tx_request_dto.get_dict(),
        headers=cash_helper.__get_default_cash_headers(customer_profile_id),
    )

    assert response["headers"]["status_code"] == status_code, (
        f"[TraceId: {response['headers']['trace_id']}]\n"
        f"Expect status_code: {status_code}\n"
        f"Actual status_code: {response['headers']['status_code']}"
    )

    if response["headers"]["status_code"] == "200":
        assert response["headers"]["message"] == "Success"

        assert response["data"]["transaction_status"] == message
        assert (
                "data" in response
        ), f"\nExpected non-empty data object, found empty. Response:{response}"

        assert "transaction_id" in response["data"], (
            f"\nExpected data object contains transaction_id"
            f"\nActual data: {response['data']}"
        )


@Then(
    "I update transaction with transaction_id ([^']*) with the negative_transfer_allowed as ([^']*) and expect the header statuscode ([^']*)"
)
def update_transaction_and_verify_status(
        context, transaction_id: str, negative_transfer_allowed: bool, status_code: str
):
    request = context.request

    update_tx_request_dto = DataClassParser.parse_row(
        context.table.rows[0], UpdateTransactionRequestDTO
    )

    update_tx_request_dto.transaction_id = context.data[
        update_tx_request_dto.transaction_id
    ]
    update_tx_request_dto.customer_profile_id = context.data[
        update_tx_request_dto.customer_profile_id
    ].customer_profile_id
    response = request.hugoserve_put_request(
        path=f"/cash/v1/transaction/{update_tx_request_dto.transaction_id}",
        data=update_tx_request_dto.get_dict(),
        headers=cash_helper.__get_default_cash_headers(
            update_tx_request_dto.customer_profile_id
        ),
    )

    assert response["headers"]["status_code"] == status_code, (
        f"[TraceId: {response['headers']['trace_id']}]\n"
        f"Expect status_code: {status_code}\n"
        f"Actual status_code: {response['headers']['status_code']}"
    )

    if response["headers"]["status_code"] == "200":
        assert response["headers"]["message"] == "Success"

        assert (
                "data" in response
        ), f"\nExpected non-empty data object, found empty. Response:{response}"

        assert "transaction_id" in response["data"], (
            f"\nExpected data object contains transaction_id"
            f"\nActual data: {response['data']}"
        )


@Then(
    "I settle transaction to transfer funds with below details and expect the header statuscode ([^']*) and transaction_status as ([^']*)"
)
def settle_transaction_and_verify_status(
        context,
        status_code: str,
        message: str,
):
    request = context.request

    settle_tx_request_dto = DataClassParser.parse_row(
        context.table.rows[0], SettleTransactionRequestDTO
    )

    settle_tx_request_dto.transaction_id = context.data[
        settle_tx_request_dto.transaction_id
    ]
    settle_tx_request_dto.customer_profile_id = context.data[
        settle_tx_request_dto.customer_profile_id
    ].customer_profile_id
    idempotency_key = settle_tx_request_dto.idempotency_key
    if (
            settle_tx_request_dto.overdraft_funding_cash_wallet_id is not None
            and settle_tx_request_dto.overdraft_funding_cash_wallet_id != ""
    ):
        settle_tx_request_dto.overdraft_funding_cash_wallet_id = context.data[
            settle_tx_request_dto.overdraft_funding_cash_wallet_id
        ].cash_wallet_id
    else:
        settle_tx_request_dto.overdraft_funding_cash_wallet_id = None

    response = request.hugoserve_put_request(
        path=f"/cash/v1/transaction/{settle_tx_request_dto.transaction_id}/settle",
        data=settle_tx_request_dto.get_dict(),
        headers=cash_helper.__get_default_cash_headers(
            settle_tx_request_dto.customer_profile_id, idempotency_key
        ),
    )
    assert response["headers"]["status_code"] == status_code, (
        f"[TraceId: {response['headers']['trace_id']}]\n"
        f"Expect status_code: {status_code}\n"
        f"Actual status_code: {response['headers']['status_code']}"
    )

    if response["headers"]["status_code"] == "200":
        assert "transaction_id" in response["data"], (
            f"\nExpected data object contains transaction_id"
            f"\nActual data: {response['data']}"
        )
        assert response["data"]["transaction_status"] == message, (
            f"\nExpect data.account_status: {message}"
            f"\nActual data.account_status: {response['data']['transaction_status']}, data: {response['data']}"
        )
    else:
        assert response["headers"]["message"] == message


@Then(
    "I settle transaction to transfer funds with below details and expect the header statuscode ([^']*)"
)
def settle_transaction_and_verify_status(
        context,
        status_code: str,
):
    request = context.request

    settle_tx_request_dto = DataClassParser.parse_row(
        context.table.rows[0], SettleTransactionRequestDTO
    )

    settle_tx_request_dto.transaction_id = context.data[
        settle_tx_request_dto.transaction_id
    ]
    settle_tx_request_dto.customer_profile_id = context.data[
        settle_tx_request_dto.customer_profile_id
    ].customer_profile_id

    if (
            settle_tx_request_dto.overdraft_funding_cash_wallet_id is not None
            and settle_tx_request_dto.overdraft_funding_cash_wallet_id != ""
    ):
        settle_tx_request_dto.overdraft_funding_cash_wallet_id = context.data[
            settle_tx_request_dto.overdraft_funding_cash_wallet_id
        ].cash_wallet_id
    else:
        settle_tx_request_dto.overdraft_funding_cash_wallet_id = None

    if "idempotency_key" in context.table.headings:
        idempotency_key_identifier = context.table.rows[0]["idempotency_key"]
        try:
            idempotency_key = context.data[idempotency_key_identifier]
        except:
            idempotency_key = str(random.randint(1, 99999999))
            context.data[context.table.rows[0]["idempotency_key"]] = idempotency_key
    else:
        idempotency_key = settle_tx_request_dto.idempotency_key

    response = request.hugoserve_put_request(
        path=f"/cash/v1/transaction/{settle_tx_request_dto.transaction_id}/settle",
        data=settle_tx_request_dto.get_dict(),
        headers=cash_helper.__get_default_cash_headers(
            settle_tx_request_dto.customer_profile_id, idempotency_key
        ),
    )

    assert response["headers"]["status_code"] == status_code, (
        f"[TraceId: {response['headers']['trace_id']}]\n"
        f"Expect status_code: {status_code}\n"
        f"Actual status_code: {response['headers']['status_code']}"
    )

    if response["headers"]["status_code"] == "200":
        assert "transaction_id" in response["data"], (
            f"\nExpected data object contains transaction_id"
            f"\nActual data: {response['data']}"
        )


@Then(
    "I settle transaction to transfer funds with below details for requested amount less than blocked amount and expect the header statuscode ([^']*) and transaction_status as ([^']*)"
)
def settle_transaction_and_verify_status(
        context,
        status_code: str,
        message: str,
):
    request = context.request

    settle_tx_request_dto = DataClassParser.parse_row(
        context.table.rows[0], SettleTransactionRequestDTO
    )

    settle_tx_request_dto.transaction_id = context.data[
        settle_tx_request_dto.transaction_id
    ]
    settle_tx_request_dto.customer_profile_id = context.data[
        settle_tx_request_dto.customer_profile_id
    ].customer_profile_id
    idempotency_key = settle_tx_request_dto.idempotency_key
    if (
            settle_tx_request_dto.overdraft_funding_cash_wallet_id is not None
            and settle_tx_request_dto.overdraft_funding_cash_wallet_id != ""
    ):
        settle_tx_request_dto.overdraft_funding_cash_wallet_id = context.data[
            settle_tx_request_dto.overdraft_funding_cash_wallet_id
        ].cash_wallet_id
    else:
        settle_tx_request_dto.overdraft_funding_cash_wallet_id = None

    response = request.hugoserve_put_request(
        path=f"/cash/v1/transaction/{settle_tx_request_dto.transaction_id}/settle",
        data=settle_tx_request_dto.get_dict(),
        headers=cash_helper.__get_default_cash_headers(
            settle_tx_request_dto.customer_profile_id, idempotency_key
        ),
    )
    assert response["headers"]["status_code"] == status_code, (
        f"[TraceId: {response['headers']['trace_id']}]\n"
        f"Expect status_code: {status_code}\n"
        f"Actual status_code: {response['headers']['status_code']}"
    )

    if response["headers"]["status_code"] == "200":
        assert "transaction_id" in response["data"], (
            f"\nExpected data object contains transaction_id"
            f"\nActual data: {response['data']}"
        )

        context.data["TxId2"] = response["data"]["transaction_id"]

        assert response["data"]["transaction_status"] == message, (
            f"\nExpect data.account_status: {message}"
            f"\nActual data.account_status: {response['data']['transaction_status']}, data: {response['data']}"
        )
    else:
        assert response["headers"]["message"] == message


@Then(
    "I settle transaction to transfer funds with below details for requested amount less than blocked amount and expect the header statuscode ([^']*)"
)
def settle_transaction_and_verify_status(
        context,
        status_code: str,
):
    request = context.request

    settle_tx_request_dto = DataClassParser.parse_row(
        context.table.rows[0], SettleTransactionRequestDTO
    )

    settle_tx_request_dto.transaction_id = context.data[
        settle_tx_request_dto.transaction_id
    ]
    settle_tx_request_dto.customer_profile_id = context.data[
        settle_tx_request_dto.customer_profile_id
    ].customer_profile_id
    idempotency_key = settle_tx_request_dto.idempotency_key
    if (
            settle_tx_request_dto.overdraft_funding_cash_wallet_id is not None
            and settle_tx_request_dto.overdraft_funding_cash_wallet_id != ""
    ):
        settle_tx_request_dto.overdraft_funding_cash_wallet_id = context.data[
            settle_tx_request_dto.overdraft_funding_cash_wallet_id
        ].cash_wallet_id
    else:
        settle_tx_request_dto.overdraft_funding_cash_wallet_id = None

    response = request.hugoserve_put_request(
        path=f"/cash/v1/transaction/{settle_tx_request_dto.transaction_id}/settle",
        data=settle_tx_request_dto.get_dict(),
        headers=cash_helper.__get_default_cash_headers(
            settle_tx_request_dto.customer_profile_id, idempotency_key
        ),
    )
    assert response["headers"]["status_code"] == status_code, (
        f"[TraceId: {response['headers']['trace_id']}]\n"
        f"Expect status_code: {status_code}\n"
        f"Actual status_code: {response['headers']['status_code']}"
    )


@Then(
    "I check if we are getting same transaction_id for two requests for TxId1 ([^']*) and TxId2 ([^']*)"
)
def idempotency_and_verify_status(context, txid1, txid2):
    assert context.data[txid1] == context.data[txid2]


@Then(
    "I get the deposit transaction ([^']*) details for cash wallet ([^']*) for customerProfileId ([^']*)"
)
def get_transactions(
        context,
        transaction_identifier: str,
        identifier: str,
        customer_profile_identifier: str,
):
    request = context.request
    cash_wallet_id = context.data[identifier].cash_wallet_id
    customer_profile_id = context.data[customer_profile_identifier].customer_profile_id

    @retry(
        AssertionError,
        tries=10,
        delay=5,
        logger=None,
    )
    def retry_for_transaction_details():
        response = request.hugoserve_get_request(
            path=f"/cash/v1/cash-wallet/{cash_wallet_id}/transactions",
            headers=cash_helper.__get_default_cash_headers(customer_profile_id),
        )
        context.data[transaction_identifier] = [txn["transaction_id"] for txn in response["data"]["transactions"] if txn["transaction_type"] == "CREDIT"][0]

    retry_for_transaction_details()


@Then(
    "I confirm the deposit transaction ([^']*) for customerProfileId ([^']*) and expect the header status as ([^']*) transaction status as ([^']*)"
)
def get_transactions(
        context,
        transaction_identifier: str,
        customer_profile_identifier: str,
        status_code: str,
        message: str
):
    request = context.request
    customer_profile_id = context.data[customer_profile_identifier].customer_profile_id
    transaction_id = context.data[transaction_identifier]

    response = request.hugoserve_put_request(
        path=f"/cash/v1/transaction/{transaction_id}/confirm",
        data={
            "accept": True if context.table.rows[0]["accept"] == "true" else False
        },
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
                response["data"]["transaction_status"] == message
        ), (
            f"\nExpect Initialisation Status: {message}"
            f"\nActual Initialisation Status: {response['data']['transaction_status']}"
        )
    else:
        assert response["headers"]["message"] == message


@Then(
    "I initiate ([^']*) multiple transactions to transfer funds with respective details and expect the header statuses as ([^']*) and transaction statuses as ([^']*)"
)
def initiate_multiple_transaction_and_verify_statuses(
        context,
        transaction_count: int,
        status_code: str,
        txn_status: str
):
    transaction_count = int(transaction_count)
    request = context.request
    context.data[context.table.rows[0]["identifier"]] = []

    def prepare_and_send(index: int):
        initiate_tx_request_dto = DataClassParser.parse_row(
            context.table.rows[0], InitiateTransactionRequestDTO
        )

        if context.table.rows[0]["receiver_account_id"] == "":
            transfer_out_details = {
                "account_holder_name": "Jane Smith",
                "country": "SGP",
                "currency": "SGD",
                "code_details": {
                    "sg_bank_details": {
                        "account_number": "9876543210",
                        "swift_bic": "DBSSSGSGXXX",
                    }
                },
            }
        else:
            cash_wallet_details = context.data[
                context.table.rows[0]["receiver_account_id"]
            ].cash_wallet_details
            transfer_out_details = {
                "account_holder_name": cash_wallet_details.account_holder_name,
                "country": cash_wallet_details.country,
                "currency": cash_wallet_details.currency,
                "code_details": {
                    "sg_bank_details": {
                        "account_number": cash_wallet_details.code_details.sg_code_details.account_number,
                        "swift_bic": cash_wallet_details.code_details.sg_code_details.swift_bic,
                    }
                },
            }

        initiate_tx_request_dto.transfer_out_details = transfer_out_details

        if initiate_tx_request_dto.cash_wallet_id:
            initiate_tx_request_dto.cash_wallet_id = context.data[
                initiate_tx_request_dto.cash_wallet_id
            ].cash_wallet_id
        else:
            initiate_tx_request_dto.cash_account_id = context.data[
                initiate_tx_request_dto.cash_account_id
            ]

        initiate_tx_request_dto.customer_profile_id = context.data[
            initiate_tx_request_dto.customer_profile_id
        ].customer_profile_id

        response = request.hugoserve_post_request(
            path="/cash/v1/transaction/initiate",
            data=initiate_tx_request_dto.get_dict(),
            headers=cash_helper.__get_default_cash_headers(
                initiate_tx_request_dto.customer_profile_id
            ),
        )

        # Validate response
        assert response["headers"]["status_code"] == status_code, (
            f"[TraceId: {response['headers']['trace_id']}]\n"
            f"Expected: {status_code}, Got: {response['headers']['status_code']}"
        )

        if status_code == "200":
            assert response["data"]["transaction_status"] == txn_status
            assert "transaction_id" in response["data"]
            return response["data"]["transaction_id"]

        return None

    async def run_async():
        loop = asyncio.get_running_loop()
        tasks = [
            loop.run_in_executor(None, prepare_and_send, i) for i in range(transaction_count)
        ]
        results = await asyncio.gather(*tasks)
        context.data[context.table.rows[0]["identifier"]].extend(results)

    asyncio.run(run_async())


@Then(
    "I settle ([^']*) multiple transactions to transfer funds with respective details and expect the header statuses ([^']*) and transaction statuses as ([^']*)"
)
def settle_multiple_transactions_and_verify_statuses(
        context,
        transaction_count: int,
        status_code: str,
        message: str,
):
    transaction_count = int(transaction_count)
    lst = []
    split = "new_transaction_id" in context.table.headings

    def prepare_and_settle(i):
        request = context.request

        settle_tx_request_dto = DataClassParser.parse_row(
            context.table.rows[0], SettleTransactionRequestDTO
        )

        settle_tx_request_dto.transaction_id = context.data[settle_tx_request_dto.transaction_id][i]

        settle_tx_request_dto.customer_profile_id = context.data[
            settle_tx_request_dto.customer_profile_id
        ].customer_profile_id

        if (
                settle_tx_request_dto.overdraft_funding_cash_wallet_id
                and settle_tx_request_dto.overdraft_funding_cash_wallet_id != ""
        ):
            settle_tx_request_dto.overdraft_funding_cash_wallet_id = context.data[
                settle_tx_request_dto.overdraft_funding_cash_wallet_id
            ].cash_wallet_id
        else:
            settle_tx_request_dto.overdraft_funding_cash_wallet_id = None

        response = request.hugoserve_put_request(
            path=f"/cash/v1/transaction/{settle_tx_request_dto.transaction_id}/settle",
            data=settle_tx_request_dto.get_dict(),
            headers=cash_helper.__get_default_cash_headers(
                settle_tx_request_dto.customer_profile_id
            ),
        )

        assert response["headers"]["status_code"] == status_code, (
            f"[TraceId: {response['headers']['trace_id']}]\n"
            f"Expected status_code: {status_code}\n"
            f"Actual status_code: {response['headers']['status_code']}"
        )

        if status_code == "200":
            assert response["data"]["transaction_status"] == message, (
                f"\nExpected transaction_status: {message}"
                f"\nActual transaction_status: {response['data']['transaction_status']}"
            )
            if split:
                lst.append(response["data"]["transaction_id"])
        else:
            assert response["headers"]["message"] == message

    async def run_async():
        loop = asyncio.get_running_loop()
        tasks = [
            loop.run_in_executor(None, prepare_and_settle, i) for i in range(transaction_count)
        ]
        await asyncio.gather(*tasks)
        if split:
            context.data[context.table.rows[0]["new_transaction_id"]] = lst

    asyncio.run(run_async())


@Then(
    "I wait until max time to verify the group of transactions ([^']*) statuses as ([^']*) amount as ([^']*) for customerProfileId ([^']*)"
)
def wait_and_verify_transaction_statuses_and_amount(
        context,
        identifier: str,
        transaction_status: str,
        amount: float,
        customer_profile_identifier: str
):
    request = context.request
    customer_profile_id = context.data[customer_profile_identifier].customer_profile_id

    @retry(
        AssertionError,
        tries=20,
        delay=5,
        logger=None,
    )
    def retry_for_transaction_status(transaction_id):
        response = request.hugoserve_get_request(
            f"/cash/v1/transaction/{transaction_id}",
            headers=cash_helper.__get_default_cash_headers(customer_profile_id),
        )

        assert response["headers"]["status_code"] == "200", (
            f"[TraceId: {response['headers']['trace_id']}]\n"
            f"Expect status_code: 200\n"
            f"Actual status_code: {response['headers']['status_code']}"
        )

        if response["data"] is not None:
            assert response["data"]["transaction_status"] == transaction_status, (
                f"\nExpect data.transaction_status: {transaction_status}"
                f"\nActual data.transaction_status: {response['data']['transaction_status']}, data: {response['data']}"
            )
            assert response["data"]["amount"] == float(amount), (
                f"\nExpect data.amount: {amount}"
                f"\nActual data.amount: {response['data']['amount']}, data: {response['data']}"
            )

    async def run_async():
        loop = asyncio.get_running_loop()
        tasks = [
            loop.run_in_executor(None, retry_for_transaction_status, context.data[identifier][i]) for i in range(len(context.data[identifier]))
        ]
        await asyncio.gather(*tasks)

    asyncio.run(run_async())
