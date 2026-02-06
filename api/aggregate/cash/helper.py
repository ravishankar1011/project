from typing import Optional
import random

from hugoutils.utilities.dataclass_util import DataClassParser

from tests.api.aggregate.cash.cash_dataclass import (
    CashWalletDTO,
)

cash_providers_config = {
    "DBS Bank Ltd": {"supports_integration_test": True, "max_wait_time": 360},
    "Pseudo Provider": {"supports_integration_test": True, "max_wait_time": 360},
    "HugoBank Limited": {"supports_integration_test": True, "max_wait_time": 120},
}

def __get_provider_id(context, provider_name: str, customer_profile_id: str):
    provider_region = "SG"
    if provider_name == "HugoBank Limited":
        provider_region = "PK"

    provider_list = context.request.hugoserve_get_request(
        path="/cash/v1/provider",
        params={"region": provider_region},
        headers=__get_default_cash_headers(customer_profile_id),
    )["data"]["providers"]

    return next(
        provider["provider_id"]
        for provider in provider_list
        if provider["name"] == provider_name
    )

def __validate_provider(provider_name):
    if provider_name not in cash_providers_config:
        raise RuntimeError(f"No such provider found. Provider name: {provider_name}")

    if not cash_providers_config[provider_name]["supports_integration_test"]:
        raise RuntimeError(
            f"Integration tests are not supported for provider {provider_name}"
        )


def __get_default_cash_headers(
    customer_profile_id: str,
    idempotency_key: Optional[str] = None,
    customer_access_key: str = None,
    origin: Optional[str] = "CUSTOMER",
):
    if origin == "" or origin is None:
        origin = "CUSTOMER"

    if idempotency_key is None:
        idempotency_key = str(random.randint(1, 99999999))

    return {
        "x-customer-profile-id": customer_profile_id,
        "x-customer-access-key": customer_access_key,
        "x-idempotency-key": idempotency_key,
        "x-origin-id": origin,  # need to send this dynamically
    }


def __fetch_bank_account(customer_profile_id, context, bank_account_id: str):
    response = context.request.hugoserve_get_request(
        f"/cash/v1/cash-wallet/{bank_account_id}/details",
        headers=__get_default_cash_headers(customer_profile_id),
    )
    return DataClassParser.dict_to_object(response["data"], CashWalletDTO)
