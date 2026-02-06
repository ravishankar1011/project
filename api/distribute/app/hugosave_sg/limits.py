from behave import *
import tests.api.distribute.app_helper as ah
from tests.util.common_util import check_status_distribute
from retry import retry

use_step_matcher("re")

limit_type_map = {
    "Internal Transfer out": "To other HugoBank A/c",
    "External Credit": "Daily Receiving Limit",
    "External Transfer out": "To other bank A/c",
    "Per Transaction": "Per Transaction Limit",
    "Daily": "Daily",
    "Monthly": "Monthly"
}


@Step("I edit the ([^']*) limits for user ([^']*) to ([^']*) ([^']*) and expect a status code of ([^']*)")
def step_impl(context, limit_type, uid, limit, currency, expected_status_code):
    global limit_id

    check_limit_display_text = limit_type_map.get(limit_type, "")
    request = context.request
    headers = ah.get_user_header(context, uid)

    response = request.hugosave_get_request(
        path=ah.limits_urls["get-limits"],
        headers=headers,
    )

    limits_data = response.get("data", {}).get("limits", [])
    if not limits_data:
        raise Exception(f"No limits found for user {uid}")

    update_limit_dto = []
    for limit_entry in limits_data:
        if limit_entry["displayTitle"] == check_limit_display_text:
            limit_id = limit_entry.get("limitId")
            context.data["users"][uid]["limit_id"] = limit_id
            update_limit_dto.append({"limit_id": limit_id, "value": limit})
            break

    if not update_limit_dto:
        raise Exception(f"No valid limit IDs found for user {uid}")

    user_authorisation_token = context.data["users"][uid].get(
        "user_authorisation_token"
    )
    headers["x-final-user-authorisation-token"] = user_authorisation_token
    body = {"update_limit_dto": update_limit_dto}

    response = request.hugosave_put_request(
        path=ah.limits_urls["update-limits"], headers=headers, data=body
    )

    assert check_status_distribute(response, expected_status_code), f"Expected status code: {expected_status_code}, but received response: {response}"


@Step(
    "I check if the hard limits are updated to ([^']*) for user ([^']*)"
)
def step_impl(context, updated_hard_limit_range, uid):
    request = context.request
    user_prof_id = ah.get_user_profile_id(uid, context)
    headers = ah.get_user_header(context, uid)

    @retry(AssertionError, tries=40, delay=5, logger=None)
    def retry_user_limits_details():
            response = request.hugosave_get_request(
                path=ah.limits_urls["get-limits"],
                headers=headers,
            )

            edited_limit_id = context.data["users"][uid].get("limit_id")
            if not edited_limit_id:
                raise AssertionError(
                    f"Limit ID not found in context for user {uid}"
                )

            matched_limit = next(
                (
                    limit
                    for limit in response.get("data", {}).get("limits", [])
                    if limit.get("limitId") == edited_limit_id
                ),
                None,
            )

            if matched_limit is None:
                raise AssertionError(
                    f"Limit ID {edited_limit_id} not found in limits for user {user_prof_id}"
                )

            actual_value = matched_limit.get("userSetValue")
            expected_value = float(updated_hard_limit_range)

            assert (
                float(actual_value) == expected_value
            ), f"Expected hard limit {expected_value}, but found {actual_value} for user {user_prof_id}"

    retry_user_limits_details()

@Step("I deposit ([^']*) ([^']*) which is more than daily receiving limit of into wallet with product code ([^']*) to check limits for user ([^']*) and expect a status of ([^']*)")
def step_impl(context, amount, currency, product_type, uid, expected_status_code):
    global acc_id, response
    request = context.request
    amount_list = amount.split(" ")
    for item in amount_list:
        if item.isnumeric():
            amount = item

    if product_type == "CASH_WALLET_SAVE" or product_type == "CASH_WALLET_CURRENT":
        acc_id = ah.get_cash_wallet_id(context, uid)
        response = request.hugosave_put_request(
            path=ah.dev_urls["deposit"],
            data={"amount": amount},
            headers=ah.get_user_header(context, uid),
        )
    elif product_type == "CASH_WALLET_SPEND":
        acc_id = ah.get_spend_account_id(context, uid)
        funding_acc_id = ah.get_cash_wallet_id(context, uid)
        url = ah.cash_urls["transfer"].replace("{cash-wallet-id}", acc_id)
        headers = ah.get_user_header(context, uid)
        response = request.hugosave_put_request(
            path=url,
            data={
                "amount": amount,
                "transfer_type": "TRANSFER_IN",
                "funding_cash_wallet_id": funding_acc_id,
            },
            headers=headers,
        )

    assert check_status_distribute(response, expected_status_code), f"Dev Deposit request failed.\nReceived : {response}"
