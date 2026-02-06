from behave import *

from retry import retry
import tests.api.distribute.app_helper as ah
from tests.util.common_util import check_status_distribute

use_step_matcher("re")

@Step("I create a mandate ([^']*) for the user ([^']*) and expect a status code of ([^']*) and a status of ([^']*)")
def step_impl(context, mandate_identifier, user_profile_identifier, expected_status_code, expected_status):
    request = context.request
    path = ah.mandate_urls["create-mandate"]
    user_authorisation_token = context.data["users"][user_profile_identifier][
        "user_authorisation_token"
    ]

    headers = ah.get_user_header(context, user_profile_identifier)
    headers["x-final-user-authorisation-token"] = user_authorisation_token

    data = ah.get_mandate_payload(mandate_identifier)

    response = request.hugosave_post_request(path=path, data=data, headers=headers)

    if check_status_distribute(response, expected_status_code):
        if expected_status_code == "200":
            assert response["data"]["mandateStatus"] == expected_status
            mandate_data = response.get("data", {})
            user_mandates = context.data["users"][user_profile_identifier].setdefault("mandates", {})
            user_mandates[mandate_identifier] = mandate_data


@Step("I verify mandate ([^']*) for user ([^']*) is created with status code ([^']*)")
def step_impl(context, mandate_identifier, user_profile_identifier, expected_status_code):
    request = context.request

    mandate_id = context.data["users"][user_profile_identifier]["mandates"][mandate_identifier]["mandateId"]
    path = ah.mandate_urls["get-mandate"].replace("mandate-id", mandate_id)
    user_authorisation_token = context.data["users"][user_profile_identifier][
        "user_authorisation_token"
    ]

    headers = ah.get_user_header(context, user_profile_identifier)
    headers["x-final-user-authorisation-token"] = user_authorisation_token

    @retry(AssertionError, tries=15, delay=5)
    def retry_for_mandate_status():
        response = request.hugosave_get_request(path=path, headers=headers)

        actual_status = response["data"]["mandateStatus"]
        assert actual_status == "MANDATE_CREATED", (
            f"Mandate status check failed. "
            f"Expected: MANDATE_CREATED, "
            f"Actual: {actual_status}"
        )

    retry_for_mandate_status()


@Step("I ([^']*) the Mandate ([^']*) for user ([^']*)")
def step_impl(context, mandate_status, mandate_identifier, user_profile_identifier):
    request = context.request

    mandate_id = context.data["users"][user_profile_identifier]["mandates"][mandate_identifier]["mandateId"]
    if mandate_status == "accept":
        path = ah.dev_urls["accept-mandate"].replace("mandate-id", mandate_id)
    else:
        path = ah.dev_urls["authorize-mandate"].replace("mandate-id", mandate_id)
    headers = ah.get_user_header(context, user_profile_identifier)

    response = request.hugosave_post_request(path=path, headers=headers)

    check_status_distribute(response, "200")

    authorize_mandate_response = response.get("data", {})
    context.data["users"][user_profile_identifier].setdefault(
        "authorize-mandate-response", authorize_mandate_response
    )
