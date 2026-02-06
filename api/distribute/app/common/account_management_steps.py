import requests
from behave import *

import tests.api.distribute.app_helper as ah
from tests.util.common_util import check_status_distribute
from retry import retry

use_step_matcher("re")

@Step("I unbind the ([^']*) for user ([^']*) and expect a status code of ([^']*)")
def unbind_device(context, device, uid, expected_status_code):
    request = context.request
    device_id = ah.get_device_id(context, uid, device)
    path = ah.device_management_urls["unbind"].replace("{device-id}", device_id)
    final_user_authorisation_token = context.data["users"][uid][
        "user_authorisation_token"
    ]
    headers = ah.get_user_header(context, uid)
    headers["x-final-user-authorisation-token"] = final_user_authorisation_token
    unbind_device_response = request.hugosave_delete_request(
        path=path, headers=headers
    )
    assert check_status_distribute(unbind_device_response, expected_status_code)
    context.data["users"][uid]["user_devices"][device] = {}


@Step("I block user ([^']*) and expect a status code of ([^']*)")
def block_user(context, uid, expected_status_code):
    request = context.request
    final_user_authorisation_token = context.data["users"][uid][
        "user_authorisation_token"
    ]
    headers = ah.get_user_header(context, uid)
    headers["x-final-user-authorisation-token"] = final_user_authorisation_token
    block_response = request.hugosave_put_request(
        path = ah.user_urls["status"],
        data={"status": "BLOCK"},
        headers = headers,
    )
    assert check_status_distribute(block_response, expected_status_code), f"Expected status code: {expected_status_code}, but received response: {block_response}"


@Step("I check the status for user ([^']*), it should be ([^']*)")
def step_impl(context, uid, expected_status):
    request = context.request
    device_info = ah.get_device_info(context, uid)
    response = request.hugosave_get_request(
        path=ah.verify_mobile_urls["initiate-verification"],
        headers=ah.get_mobile_verification_header(context, device_info),
        params={"user-name": context.data["users"][uid]["initiate_mobile_verification_response"]["userName"]},
    )
    if check_status_distribute(response, 200):
        assert response["data"]["userStatus"] == expected_status


@Step("I authenticate the user ([^']*) from device - ([^']*) and expect a status of ([^']*)")
def device_authentication(context, uid, device, expected_status):
    request = context.request
    request_data = {
        "user_name": context.data["users"][uid]["user_name"],
        "passcode": context.data["users"][uid]["user_details"]["password"],
    }

    device_info = ah.get_device_info(context, uid)
    headers = ah.get_mobile_verification_header(context, device_info)
    headers["x-verification-token"] = context.data["users"][uid]["user_devices"][device]["sign_in_verification_token"]
    authentication_response = request.hugosave_post_request(
        headers= headers,
        path = ah.auth_user_urls["authenticate-user"],
        data = request_data,
    )

    assert authentication_response["data"]["authenticationStatus"] == expected_status
    if not expected_status == "AUTHENTICATION_FAILED":
        context.data["users"][uid]["user_devices"][device]["authentication_token"] = authentication_response["data"]["authenticationToken"]


@Step("I log into the account of user ([^']*) on ([^']*) and the verification status should be ([^ ]+)(?: for user ([^']*) phone_number)?")
def sign_in(context, uid, device, expected_status,number=None):
    request = context.request

    if device != context.data["users"][uid]["current_device"]:
        context.data["users"][uid]["user_devices"][device] = ah.generate_device_details()
        context.data["users"][uid]["current_device"] = device

    customer = context.data["customer"]
    if customer == "HUGOSAVE":
        path = ah.verify_mobile_urls["initiate-mobile-verification"]

    elif customer == "HUGOBANK":
        path = ah.verify_mobile_urls["initiate-mobile-verification"]

    if customer == "CDV":
        path = ah.verify_mobile_urls["initiate-email-verification"]

    device_info = ah.get_device_info(context, uid)
    @retry(AssertionError, tries=10, delay=10, logger=None)
    def retry_update_phone_number():
        if number == None:
            user_name = context.data["users"][uid]["user_name"]
        else:
            user_name = "+373" + ah.get_rand_number(8)
            if "updated_mobile_number" not in context.data["users"][uid]:
                 context.data["users"][uid]["updated_mobile_number"]={}
                 context.data["users"][uid]["updated_mobile_number"] = user_name
        initiate_mobile_verification_response = request.hugosave_get_request(
            path=path,
            headers=ah.get_mobile_verification_header(context, device_info),
            params={"user-name": user_name},
        )
        if check_status_distribute(initiate_mobile_verification_response,"200"):
            assert initiate_mobile_verification_response["data"]["verificationStatus"] == expected_status, "Phone number is not updated"
            context.data["users"][uid]["user_devices"][device]["sign_in_session_id"] = initiate_mobile_verification_response["data"]["sessionId"]

    retry_update_phone_number()


@Step("The user ([^']*) submits OTP to log into the user account from ([^']*) and expects a status ([^ ]+)(?: for user ([^']*) phone_number)?")
def otp_verification(context, uid, device, expected_status,number=None):
    request = context.request
    device_info = ah.get_device_info(context, uid)

    path = ""

    customer = context.data["customer"]
    if customer == "HUGOSAVE":
        path = ah.verify_mobile_urls["initiate-mobile-verification"]

    elif customer == "HUGOBANK":
        path = ah.verify_mobile_urls["initiate-mobile-verification"]

    if customer == "CDV":
        path = ah.verify_mobile_urls["initiate-email-verification"]

    if number == None:
        user_name = context.data["users"][uid]["user_name"]
    else:
        user_name = context.data["users"][uid]["updated_mobile_number"]
    submit_mobile_verification_response = request.hugosave_post_request(
        path=path,
        headers=ah.get_mobile_verification_header(context, device_info),
        data={
            "session_id": context.data["users"][uid]["user_devices"][device]["sign_in_session_id"],
            "user_name": user_name,
            "code": "123456",
        },
    )
    if check_status_distribute(submit_mobile_verification_response, 200):
        assert submit_mobile_verification_response["data"]["verificationStatus"] == expected_status
        context.data["users"][uid]["user_devices"][device]["sign_in_verification_token"] = submit_mobile_verification_response["data"]["verificationToken"]


@Step("I log into the account through ([^']*) of user ([^']*) on ([^']*) and the verification status should be ([^']*)")
def sign_in(context, method, uid, device,expected_status=None):
    request = context.request

    if device != context.data["users"][uid]["current_device"]:
        context.data["users"][uid]["user_devices"][device] = ah.generate_device_details()
        context.data["users"][uid]["current_device"] = device

    device_info = ah.get_device_info(context, uid)
    headers=ah.get_mobile_verification_header(context, device_info)

    @retry(AssertionError, tries=10, delay=10, logger=None)
    def retry_update_email():
        if method == "email":
         user_name = context.data["users"][uid]["user_details"]["email"]
        else:
            user_name = ah.get_rand_number(5) + "@gmail.com"
            context.data["users"][uid]["updated_email"] = user_name
        print(user_name)
        initiate_email_verification_response = request.hugosave_get_request(
            path=ah.verify_email_urls["initiate-verification"],
            headers=headers,
            params={"user-name": user_name}
        )
        if check_status_distribute(initiate_email_verification_response,"200"):
            assert initiate_email_verification_response["data"]["verificationStatus"] == expected_status, "Email is not updated"
            context.data["users"][uid]["user_devices"][device]["sign_in_session_id"] = initiate_email_verification_response["data"]["sessionId"]

    retry_update_email()

@Step("The user ([^']*) submits OTP received to his ([^']*) to log into the user account from ([^']*) and expects a status ([^ ]*)")
def otp_verification(context, uid, method ,device, expected_status):
    request = context.request
    device_info = ah.get_device_info(context, uid)
    user_name=""
    if method == "email":
        user_name = context.data["users"][uid]["user_details"]["email"]
    else:
        user_name = context.data["users"][uid]["updated_email"]
    submit_email_verification_response = request.hugosave_post_request(
        path=ah.verify_email_urls["initiate-verification"],
        headers=ah.get_mobile_verification_header(context, device_info),
        data={
            "session_id": context.data["users"][uid]["user_devices"][device]["sign_in_session_id"],
            "user_name": user_name,
            "code": "123456",
        },
    )

    assert submit_email_verification_response["data"]["verificationStatus"] == expected_status
    context.data["users"][uid]["user_devices"][device]["sign_in_verification_token"] = submit_email_verification_response["data"]["verificationToken"]

