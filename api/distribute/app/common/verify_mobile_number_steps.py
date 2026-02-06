from behave import *
import tests.api.distribute.app_helper as ah
from tests.util.common_util import check_status_distribute
from hugoutils.utilities.dataclass_util import DataClassParser
from tests.api.distribute.app.hugosave_sg.app_dataclass import VerifyMobileNumberDTO

use_step_matcher("re")


@Step("The user ([^']*) provides a valid mobile number on ([^']*) to initiate onboarding and the expected status is ([^']*)")
def verify_mobile_number(context, uid, device, expected_status):
    global data
    request = context.request
    context.data["users"] = {} if context.data.get("users") is None else context.data["users"]
    context.data["users"][uid] = {} if context.data["users"].get(uid) is None else context.data["users"][uid]
    context.data["users"][uid]["user_devices"] = {} if context.data["users"][uid].get("user_devices") is None else context.data["users"][uid]["user_devices"]
    context.data["users"][uid]["current_device"] = device
    context.data["users"][uid]["user_devices"][device] = ah.generate_device_details()
    verify_mobile_list = DataClassParser.parse_rows(
        context.table.rows, data_class=VerifyMobileNumberDTO
    )
    device_info = ah.get_device_info(context, uid)
    x_initiation_signature = ah.get_initiation_signature(device_info)

    for verify_mobile_dto in verify_mobile_list:
        data = verify_mobile_dto.get_dict()

    user_name = ""
    if data["user_name_type"] == "EMAIL_ADDRESS":
        url = ah.verify_mobile_urls["initiate-email-verification"]
        user_name = ah.get_rand_email()
        context.data["users"][uid]["user_name"] = user_name

    elif data["user_name_type"] == "PHONE_NUMBER":
        url = ah.verify_mobile_urls["initiate-mobile-verification"]
        if data["user_name"] == "random":
            data["user_name"] = ah.get_rand_number(10)

        mobile_prefix = "+65"
        if data["ph_prefix"] is not None:
            mobile_prefix = data["ph_prefix"]

        generated_mobile_number = mobile_prefix + data["user_name"]
        user_name = generated_mobile_number
        context.data["users"][uid]["user_name"] = generated_mobile_number

    context.data["users"][uid]["mode_of_verification"] = data["user_name_type"]
    context.data["users"][uid]["initiation_signature"] = x_initiation_signature

    initiate_mobile_verification_response = request.hugosave_get_request(
        path=url,
        headers=ah.get_mobile_verification_header(context, device_info),
        params={"user-name": user_name},
    )
    if check_status_distribute(initiate_mobile_verification_response, 200):
        assert initiate_mobile_verification_response["data"]["verificationStatus"] == expected_status
        context.data["users"][uid]["initiate_mobile_verification_response"] = (
            initiate_mobile_verification_response["data"]
        )


@Step("The user ([^']*) submits OTP to proceed with verification and expects a status code of ([^ ]+)(?: and a status of ([^']*))?")
def submit_otp(context, uid, expected_status_code, expected_status = None):
    request = context.request
    device_info = ah.get_device_info(context, uid)
    headers = ah.get_mobile_verification_header(context, device_info)

    if context.data["users"][uid]["mode_of_verification"] == "EMAIL_ADDRESS":
        url = ah.verify_mobile_urls["initiate-email-verification"]
    else:
        url = ah.verify_mobile_urls["initiate-mobile-verification"]

    submit_mobile_verification_response = request.hugosave_post_request(
        path = url,
        headers = headers,
        data={
            "session_id": context.data["users"][uid]["initiate_mobile_verification_response"]["sessionId"],
            "user_name": context.data["users"][uid]["initiate_mobile_verification_response"]["userName"],
            "code": "123456",
        },
    )
    if check_status_distribute(submit_mobile_verification_response, expected_status_code):
        if expected_status_code == "200":
            assert submit_mobile_verification_response["data"]["verificationStatus"] == expected_status
            context.data["users"][uid]["submit_mobile_verification_response"] = (
                submit_mobile_verification_response["data"]
            )
