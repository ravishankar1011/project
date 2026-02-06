import json

from behave import *
from retry import retry

use_step_matcher("re")
import tests.api.distribute.app_helper as ah
from tests.util.common_util import check_status_distribute

RANGE_MODIFIER_PAYLOADS = {
    "with below soft limit": {"amount": 20, "description": "test txn"},
    "with more than soft limit": {"amount": 1001, "description": "test txn"},
}

JOURNEY_BODY_BUILDERS = {
    "PASSCODE": ah.get_passcode_body,
    "OTHER_JOURNEYS": ah.get_other_journey_body,
}

@Step("I initiate the initial user authorisation to ([^']*) for user ([^']*) and expect a status of ([^']*)")
def get_initial_authentication_token(context, action, uid, expected_status):
    request = context.request
    response = request.hugosave_post_request(
        path=ah.get_user_authorisation_token_urls["initial-initiate"],
        headers=ah.get_user_header(context, uid),
        params={"action": action},
    )
    ah.store_journey_id(context, response)
    if check_status_distribute(response, "200"):
        assert response["data"]["userAuthorisationStatus"] == expected_status
        context.data["users"][uid][
            "user_authorisation_initial_initiate_response"
        ] = response["data"]
        if "userAuthorisationToken" in response["data"]:
            context.data["users"][uid]["user_initial_authorisation_token"] = response["data"]["userAuthorisationToken"]


@Step("I initiate the final user authorisation to ([^ ]+) and expect a user authorisation status as ([^']*) for user ([^ ]+)(?: (.*))?")
def step_impl(context, action, expected_status, uid, range_modifier=None):
    request = context.request
    headers = ah.get_user_header(context, uid)
    headers["x-initial-user-authorisation-token"] = context.data["users"][uid]["user_initial_authorisation_token"]

    payload = RANGE_MODIFIER_PAYLOADS.get(range_modifier, {})
    if action == "PAY_PAYEE":
        amount_data = (
            payload if payload else {"amount": 1001, "description": "test txn"}
        )
        data = {
            "data": json.dumps(amount_data),
            "query_params": {"filter": ""},
            "path": "path",
        }
    else:
        data = {"data": "{}", "query_params": {"filter": ""}, "path": "path"}

    response = request.hugosave_post_request(
        path=ah.get_user_authorisation_token_urls["final-initiate"],
        headers=headers,
        params={"action": action},
        data=data,
    )
    ah.store_journey_id(context, response)

    if check_status_distribute(response, "200"):
        assert response["data"]["userAuthorisationStatus"] == expected_status, f"Expected a user authorisation status: {expected_status}, but received the response: {response}"
        context.data["users"][uid][
            "user_final_authorisation_token_response"
        ] = response["data"]
        if "userAuthorisationToken" in response["data"]:
            context.data["users"][uid]["user_authorisation_token"] = response["data"]["userAuthorisationToken"]



@Step("I initiate the ([^']*) journey within the ([^']*) for user ([^']*) to authorise the user and expect a status ([^']*)")
def step_impl(context, journey_type, step_code, uid, status):
    request = context.request
    headers = ah.get_user_header(context, uid)
    journey_id = ah.get_journey_id(context, uid, journey_type, step_code)
    response = request.hugosave_post_request(
        path=ah.get_user_authorisation_token_urls["journey-initiate"].replace(
            "{journey-id}", journey_id
        ),
        headers=headers,
        data={},
    )
    context.data["users"][uid]["journey_initiate_response"] = response["data"]
    if check_status_distribute(response, "200"):
        assert response["data"]["journeyStatus"] == status



@Step("I submit the ([^']*) journey within the ([^']*) for user ([^']*) to authorise the user and expect a status ([^']*)")
def step_user_authorisation_journey(context, journey_type, step_code, uid, expected_status):
    request = context.request
    journey_id = ah.get_journey_id(context, uid, journey_type, step_code)
    url = ah.get_user_authorisation_token_urls["journey-submit"].replace("{journey-id}", journey_id)
    if journey_type == "PASSCODE":
        verification_token = context.data["users"][uid]["journey_initiate_response"][
            "data"
        ]["verificationToken"]
        passcode = ah.get_passcode(context, uid)

        body = {
            "data": json.dumps(
                {"verification_token": verification_token, "passcode": passcode}
            )
        }
    elif context.data["users"][uid]["journey_initiate_response"]["data"].get("sessionId") is not None:
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
            path=url, headers=ah.get_user_header(context, uid), data=body
        )
    if check_status_distribute(response, "200"):
        assert response["data"]["journeyStatus"] == expected_status or response["data"]["journeyStatus"] == "JOURNEY_SUCCESSFUL"
        context.data["users"][uid]["journey_submit_response"] = response["data"]


@Step("I process the ([^']*) journey within the ([^']*) for user ([^']*) to authorise the user and expect a status ([^']*)")
def step_impl(context, journey_type, step_code, uid, status):
    request = context.request
    journey_id = ah.get_journey_id(context, uid, journey_type, step_code)
    url = ah.progress_onboarding_urls["process-onboarding-journey"].replace("{journey-id}", journey_id)
    if journey_type == "PASSCODE":
        verification_token = context.data["users"][uid]["journey_initiate_response"][
            "data"
        ]["verificationToken"]
        passcode = ah.get_passcode(context, uid)
        body = {
            "data": json.dumps(
                {"verification_token": verification_token, "passcode": passcode}
            )
        }
    elif context.data["users"][uid]["journey_initiate_response"]["data"].get("sessionId") is not None:
        submit_session_id = context.data["users"][uid]["journey_initiate_response"][
            "data"
        ]["sessionId"]
        body = {
            "data": json.dumps(
                {"submit_session_id": submit_session_id, "submitted_otp": 123456}
            )
        }
    else:
        data_builder = ah.JOURNEY_DATA_BUILDERS.get(journey_type, ah.get_default_data)
        body = data_builder(context, uid)

    @retry(AssertionError, tries=30, delay=5, logger=None)
    def retry_user_details():
        response = request.hugosave_post_request(
            path=url,
            headers=ah.get_user_header(context, uid),
            data=body
        )
        if check_status_distribute(response, "200"):
            assert response["data"]["journeyStatus"] == status, f"Expected status: {status}, but received response: {response}"

    retry_user_details()


@Step("I submit the final user authorisation for ([^']*) of user ([^']*) and expect a status ([^']*)")
def step_impl(context, action, uid, expected_status):
    request = context.request
    session_id = context.data["users"][uid][
        "user_final_authorisation_token_response"
    ]["authorisationSessionId"]
    headers = ah.get_user_header(context, uid)

    response = request.hugosave_put_request(
        path=ah.get_user_authorisation_token_urls["final-submit"].replace(
            "{session-id}", session_id
        ),
        headers=headers,
    )
    if check_status_distribute(response, "200"):
        assert response["data"]["userAuthorisationStatus"] == expected_status or response["data"]["userAuthorisationStatus"] == "USER_AUTHORISATION_SUCCESS", f"Expected the final user authorisation status to be {expected_status}, but received response: {response}"


@Step("I get the final user authorisation token for ([^']*) of user ([^']*) and expect a status ([^']*)")
def step_impl(context, action, uid, expected_status):
    request = context.request
    session_id = context.data["users"][uid][
        "user_final_authorisation_token_response"
    ]["authorisationSessionId"]
    headers = ah.get_user_header(context, uid)

    @retry(AssertionError, tries=30, delay=10, logger=None)
    def retry_for_authorisation_token():
        response = request.hugosave_get_request(
            path=ah.get_user_authorisation_token_urls["final-status"].replace(
                "{session-id}", session_id
            ),
            headers=headers,
        )
        if check_status_distribute(response, "200"):
            assert response["data"]["userAuthorisationStatus"] == expected_status, f"Expected the final user authorisation status to be {expected_status}, but received response: {response}"
            context.data["users"][uid]["user_authorisation_token"] = response["data"]["userAuthorisationToken"]

    retry_for_authorisation_token()


@Step("I submit the initial user authorisation for ([^']*) for user ([^']*) and expect an user authorisation status of ([^']*)")
def submit_initial_user_authorisation(context, user_action, uid, expected_status):
    request = context.request
    session_id = context.data["users"][uid]["user_authorisation_initial_initiate_response"]["authorisationSessionId"]
    headers = ah.get_user_header(context, uid)
    response = request.hugosave_put_request(
        path = ah.get_user_authorisation_token_urls["initial-submit"].replace("{session-id}", session_id),
        headers = headers,
    )
    if check_status_distribute(response, "200"):
        assert response["data"]["userAuthorisationStatus"] == expected_status, f"Expected the status {expected_status}, but received response: {response}"


@Step("I check the status of initial user authorisation for user ([^']*) and expect an user authorisation status of ([^']*)")
def initial_user_authorisation_status(context, uid, expected_status):
    request = context.request
    session_id = context.data["users"][uid][
        "user_authorisation_initial_initiate_response"
    ]["authorisationSessionId"]
    headers = ah.get_user_header(context, uid)

    @retry(AssertionError, tries=30, delay=10, logger=None)
    def retry_for_authorisation_token():
        response = request.hugosave_get_request(
            path=ah.get_user_authorisation_token_urls["initial-status"].replace(
                "{session-id}", session_id
            ),
            headers=headers,
        )
        if (response["headers"]["statusCode"] == "200"):
            assert response["data"]["userAuthorisationStatus"] ==  expected_status, f"Expected an user authorisation status of {expected_status}, but received the response: {response}"
            context.data["users"][uid]["user_initial_authorisation_token"] = response["data"]["userAuthorisationToken"]

    retry_for_authorisation_token()


@Step("I process authorisation journey ([^']*) status of user ([^']*)")
def process(context, journey_type, uid):
    request = context.request
    journey_id = ah.get_journey_id(context, uid, journey_type)
    url = ah.get_user_authorisation_token_urls["process-journey"].replace("{journey-id}", journey_id)

    if journey_type == "PASSCODE":
        passcode = ah.get_passcode(context, uid)
        verification_token = context.data["users"][uid]["journey_initiate_response"][
            "data"
        ]["verificationToken"]
        body = {
            "data": json.dumps(
                {"verification_token": verification_token, "passcode": passcode}
            )
        }
    else:
        submit_session_id = context.data["users"][uid]["journey_initiate_response"][
            "data"
        ]["sessionId"]
        body = {"data": json.dumps({"session_id": submit_session_id, "otp": "123456"})}

    @retry(AssertionError, tries=30, delay=5, logger=None)
    def retry_user_details():
        response = request.hugosave_post_request(
            path=url, headers=ah.get_user_header(context, uid) , data = body
        )

        if check_status_distribute(response, 200):
            assert response["data"]["journeyStatus"] != "JOURNEY_PROCESSED", f"Failed to process journey, received response: {response}"

    retry_user_details()


@Step("I check status of ([^']*) journey within the ([^']*) for the user ([^']*), the user authorisation journey status should be ([^']*)")
def check_journey_status(context, journey_type, step_code, uid, expected_status):
    request = context.request
    journey_id = ah.get_journey_id(context, uid, journey_type, step_code)
    url = ah.progress_onboarding_urls["onboarding-journey-status"].replace("{journey-id}", journey_id)

    @retry(AssertionError, tries=30, delay=15, logger=None)
    def retry_journey_status():
        journey_status_response = request.hugosave_get_request(
            path=url,
            headers=ah.get_user_header(context, uid)
        )
        assert journey_status_response["data"]["journeyStatus"] == expected_status

    retry_journey_status()

