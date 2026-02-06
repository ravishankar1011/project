from behave import *
import tests.api.distribute.app_helper as ah
from tests.util.common_util import check_status_distribute


use_step_matcher("re")

@Step("I enter the current passcode for the user ([^']*) and expect an authentication status of ([^']*)")
def validate_current_passcode(context, uid, expected_status):
    request = context.request
    request_data = {
        "user_name": context.data["users"][uid]["user_name"],
        "passcode": context.data["users"][uid]["user_details"]["password"]
    }
    headers= ah.get_create_account_header(context, uid)
    if context.data["customer"] == "HUGOBANK":
        headers["x-verification-token"] = context.data["users"][uid]["user_devices"]["device_1"]["sign_in_verification_token"]
    validate_current_passcode_response = request.hugosave_post_request(
        headers= headers,
        path = ah.auth_user_urls["authenticate-user"],
        data = request_data
    )

    if check_status_distribute(validate_current_passcode_response, "200"):
        assert validate_current_passcode_response["data"]["authenticationStatus"] == "AUTHENTICATION_SUCCESSFUL", f"The entered passcode could not be validated, the returned response is: {validate_current_passcode_response}"


@Step("I update passcode for the user ([^']*) and expect a status code of ([^']*)")
def update_passcode(context, uid, expected_status_code):
    request = context.request

    headers = ah.get_user_header(context, uid)
    headers["x-final-user-authorisation-token"] = ah.get_user_authorisation_token(context, uid)
    passcode = ah.get_rand_number(6)
    update_passcode_response = request.hugosave_put_request(
        path = ah.account_management_urls["update-passcode"],
        data = {"passcode": passcode},
        headers = headers,
    )

    assert check_status_distribute(update_passcode_response, expected_status_code), f"Error updating the passcode, returned response:{update_passcode_response}"
    context.data["users"][uid]["user_details"]["password"] = passcode



@Step("I enter incorrect passcode for the user ([^']*) and expect a status of ([^']*)")
def check_incorrect_passcode(context, uid, expected_status):
    request = context.request
    request_data = {
        "user_name": context.data["users"][uid]["user_name"],
        "passcode": "0" + ah.get_rand_number(5)
    }
    check_incorrect_passcode_response = request.hugosave_post_request(
        headers= ah.get_create_account_header(context, uid),
        path = ah.auth_user_urls["authenticate-user"],
        data = request_data
    )

    if check_status_distribute(check_incorrect_passcode_response, "200"):
        assert check_incorrect_passcode_response["data"]["authenticationStatus"] == expected_status
