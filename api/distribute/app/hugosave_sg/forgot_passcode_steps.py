import json

from behave import *
import tests.api.distribute.app_helper as ah
from tests.util.common_util import check_status_distribute
from retry import retry

use_step_matcher("re")

@Step("I initiate forgot passcode for user ([^']*) and expect the status ([^']*)")
def initiate_forgot_passcode(context, uid: str, status: str):
    request = context.request
    response = request.hugosave_post_request(
        path = ah.forgot_passcode_token_urls["initiate"],
        headers = ah.forgot_passcode_headers(context, uid),
    )
    ah.store_journey_id(context, response)
    if check_status_distribute(response, 200):
        assert response["data"]["forgotPasscodeStatus"] == status
        context.data["users"][uid]["initiate_forgot_passcode"] = (
            response.get("data")
        )


@Step("I check the status of initiate forgot passcode for user ([^']*)")
def step_impl(context, user_profile_identifier: str):
    request = context.request
    user_data = context.data["users"].get(user_profile_identifier)

    if not user_data:
        raise AssertionError(
            f"User data not found for '{user_profile_identifier}'. Ensure user details are loaded into context."
        )

    try:
        user_name = user_data["submit_mobile_verification_response"]["userName"]
        verification_token = user_data["submit_mobile_verification_response"][
            "verificationToken"
        ]
        session_id = user_data["initiate_forgot_passcode"]["forgotPasscodeSessionId"]
    except KeyError as e:
        raise AssertionError(
            f"Missing expected data for user '{user_profile_identifier}': {e}. Verify 'submit_mobile_verification_response' and 'initiate_forgot_passcode' are correctly populated in context."
        )

    headers = {
        "x-user-name": user_name,
        "x-device-id": context.data["users"][user_profile_identifier]["current_device_info"]["x-device-id"],
        "x-verification-token": verification_token,
    }

    response = request.hugosave_get_request(
        path=ah.forgot_passcode_token_urls["check-initiate-status"].replace(
            "{session-id}", session_id
        ),
        headers=headers,
    )

    assert check_status_distribute(response, 200)


@Step("I initiate the ([^']*) journey within the ([^']*) for user ([^']*) and expect a journey status of ([^']*)")
def step_impl(context, journey_type, step_code, uid, status):
    request = context.request
    journey_id = ah.get_journey_id(context, uid, journey_type, step_code)
    response = request.hugosave_post_request(
        path = ah.forgot_passcode_token_urls["journey-initiate"].replace(
            "{journey-id}", journey_id
        ),
        headers = ah.forgot_passcode_headers(context, uid),
        data={},
    )

    if check_status_distribute(response, "200"):
        assert response["data"]["journeyStatus"] == status
        context.data["users"][uid]["journey_initiate_response"] = (
            response.get("data")
        )


@Step("I process the ([^']*) journey within the ([^']*) for user ([^']*) and expect a journey status of ([^']*)")
def step_impl(context, journey_type, step_code, uid, status):
    request = context.request
    journey_id = ah.get_journey_id(context, uid, journey_type, step_code)

    data_builder = ah.JOURNEY_DATA_BUILDERS.get(journey_type, ah.get_default_data)
    data = data_builder(context, uid)

    response = request.hugosave_post_request(
        path = ah.forgot_passcode_token_urls["process-forgot-passcode-journey"].replace(
            "{journey-id}", journey_id
        ),
        headers = ah.forgot_passcode_headers(context, uid),
        data = data,
    )

    if check_status_distribute(response, "200"):
        assert response["data"]["journeyStatus"] == status, f"Expected status {status}, but received the response: {response}"


@Step("I submit the ([^']*) journey within the ([^']*) for user ([^']*) and expect a journey status of ([^']*)")
def step_impl(context, journey_type, step_code, uid, status):
    request = context.request
    journey_id = ah.get_journey_id(context, uid, journey_type, step_code)
    if context.data["users"][uid]["journey_initiate_response"]["data"].get("sessionId"):
        submit_session_id = context.data["users"][uid]["journey_initiate_response"]["data"]["sessionId"]
        body = {
            "data": json.dumps(
                {"submit_session_id": submit_session_id, "submitted_otp": 123456}
            )
        }
    else:
        data_builder = ah.JOURNEY_DATA_BUILDERS.get(journey_type, ah.get_default_data)
        body = data_builder(context, uid)

    response = request.hugosave_post_request(
        path = ah.forgot_passcode_token_urls["journey-submit"].replace(
            "{journey-id}", journey_id
        ),
        headers = ah.forgot_passcode_headers(context, uid),
        data = body,
    )

    if check_status_distribute(response, "200"):
        assert response["data"]["journeyStatus"] == status
        context.data["users"][uid]["journey_submit_response"] = (
            response.get("data")
        )


@Step("I submit forgot passcode of user ([^']*) and expect a status of ([^']*)")
def step_impl(context, uid: str, status):
    request = context.request
    user_data = context.data["users"].get(uid)
    user_profile_id = ah.get_user_profile_id(uid, context)
    if not user_data:
        raise AssertionError(
            f"User data not found for '{uid}'. "
            f"Ensure user details are loaded into context."
        )

    try:
        session_id = user_data["initiate_forgot_passcode"]["forgotPasscodeSessionId"]
    except KeyError as e:
        raise AssertionError(
            f"Missing expected data for user '{uid}': {e}. "
            f"Verify 'submit_mobile_verification_response' and 'initiate_forgot_passcode' "
            f"are correctly populated in context."
        )

    body = {"forgot_passcode_session_id": session_id, "forgot_passcode_journey": "OTP"}

    response = request.hugosave_post_request(
        path = ah.forgot_passcode_token_urls["final-submit"],
        headers = ah.forgot_passcode_headers(context, uid),
        data = body
    )
    if check_status_distribute(response, "200"):
        assert response["data"]["forgotPasscodeStatus"] == status or response["data"]["forgotPasscodeStatus"] == "FORGOT_PASSCODE_SUCCESS", f"Expected the status: {status}, but received the response: {response}"


@Step("I get the forgot password token for user ([^']*) and expect a status of ([^']*)")
def step_impl(context, uid: str, expected_status):
    request = context.request
    user_data = context.data["users"].get(uid)
    if not user_data:
        raise AssertionError(
            f"User data not found for '{uid}'. Ensure user details are loaded into context."
        )

    try:
        session_id = user_data["initiate_forgot_passcode"]["forgotPasscodeSessionId"]
    except KeyError as e:
        raise AssertionError(
            f"Missing expected data for user '{uid}': {e}. Verify 'submit_mobile_verification_response' and 'initiate_forgot_passcode' are correctly populated in context."
        )

    @retry(AssertionError, delay=20, tries=5, logger=None)
    def wait_for_card_status():
        response = request.hugosave_get_request(
            path = ah.forgot_passcode_token_urls["final-status"].replace(
                "{session-id}", session_id
            ),
            headers = ah.forgot_passcode_headers(context, uid),
        )
        if check_status_distribute(response, "200"):
            assert response["data"]["forgotPasscodeStatus"] == expected_status
            forgot_passcode_token = response.get("data", {}).get("forgotPasscodeToken")
            context.data["users"][uid]["forgot_passcode_token"] = forgot_passcode_token
    wait_for_card_status()

@Step("I update the password for user ([^']*) and expect a status code of ([^']*)")
def step_impl(context, uid: str, expected_status_code):
    request = context.request
    user_data = context.data["users"].get(uid)
    user_profile_id = ah.get_user_profile_id(uid, context)
    if not user_data:
        raise AssertionError(
            f"User data not found for '{uid}'. "
            f"Ensure user details are loaded into context."
        )

    try:
        user_name = user_data["submit_mobile_verification_response"]["userName"]
        verification_token = user_data["submit_mobile_verification_response"][
            "verificationToken"
        ]
        forgot_passcode_token = user_data["forgot_passcode_token"]
    except KeyError as e:
        raise AssertionError(
            f"Missing expected data for user '{uid}': {e}. "
            f"Verify 'submit_mobile_verification_response' and 'forgot_passcode_token' "
            f"are correctly populated in context."
        )

    headers = ah.forgot_passcode_headers(context, uid)
    headers["x-forgot-passcode-token"] = forgot_passcode_token
    body = {"passcode": "333333"}

    response = request.hugosave_post_request(
        path = ah.forgot_passcode_token_urls["update-passcode"],
        headers = headers,
        data = body,
    )

    assert check_status_distribute(response, expected_status_code), f"Unable to update the passcode, received response: {response}"
