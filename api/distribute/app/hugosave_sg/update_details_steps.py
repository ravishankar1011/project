from behave import *
import tests.api.distribute.app_helper as ah
from tests.util.common_util import check_status_distribute
from retry import retry

use_step_matcher("re")


@Step("I update ([^']*) of user ([^']*) and check if updated correctly")
def update_user_details(context, fields: str, uid: str):
    request = context.request

    field_list = fields.split(",")
    data = ah.get_dummy_user_data(field_list)

    url = ah.dev_urls["update"]
    if "client_flags" in fields:
        url = ah.user_profile_urls["client_flags"]

    headers = ah.get_user_header(context, uid)
    headers['x-enforce-auth'] = "False"

    response = request.hugosave_put_request(
        path = url,
        data = data,
        headers = headers
    )

    assert check_status_distribute(response, "200"), f"Expected: 200 received: {response['data']['status']}"
    updated_data = request.hugosave_get_request(
        ah.user_profile_urls["details"],
        headers=ah.get_user_header(context, uid),
    )["data"]

    for field in field_list:
        updated_data[field] = data[field]

    context.data["users"][uid][
        "user_details_response"
    ] = updated_data


@Step("I update ([^']*) of user ([^']*) and check if it is updated correctly")
def update_user_details(context, field: str, uid: str):
    request = context.request

    data = ""
    if field == "phone_number":
        data = { "phone_number" : context.data["users"][uid]["updated_mobile_number"]}
    elif field == "email":
        data = { "email" : context.data["users"][uid]["updated_email"]}
    elif field == "mailing_address":
        data = { "user_address_id" : context.data["users"][uid]["WORK_ADDRESS"]["address_id"]}
    elif field == "next_of_kin":
        data = { "name": "John" , "relationship": "PARENT"}
    else:
        data = ah.get_dummy_user_data(field)

    headers = ah.get_user_header(context, uid)
    headers["x-final-user-authorisation-token"] = context.data["users"][
        uid
    ]["user_authorisation_token"]

    url=""
    response=""
    if (field == "name"):
        url = ah.account_management_urls["update_name"]
        response = request.hugosave_put_request(
            path = url,
            params = data,
            headers = headers
        )
    elif (field == "email"):
        url = ah.account_management_urls["update_email"]
        data["verification_token"] = context.data["users"][uid]["user_devices"]["device_1"]["sign_in_verification_token"]
        response = request.hugosave_put_request(
            path = url,
            data = data,
            headers = headers
        )
    elif (field == "phone_number"):
        url = ah.account_management_urls["update_phone_number"]
        data["verification_token"] = context.data["users"][uid]["user_devices"]["device_1"]["sign_in_verification_token"]
        response = request.hugosave_put_request(
            path = url,
            data = data,
            headers = headers
        )
    elif (field == "mailing_address"):
        url = ah.account_management_urls["update_mailing_address"]
        response = request.hugosave_put_request(
            path = url,
            data = data,
            headers = headers
        )
    elif (field == "next_of_kin"):
        url = ah.account_management_urls["update_next_of_kin"]
        response = request.hugosave_put_request(
            path = url,
            data = data,
            headers = headers
        )

    assert check_status_distribute(response, "200"), f"Expected a status code of 200, but received the response: {response}"
    @retry(AssertionError, tries=10, delay=5, logger=None)
    def retry_check_details():
        updated_data = request.hugosave_get_request(
            path=ah.user_profile_urls["details"],
            headers=ah.get_user_header(context, uid),
            params={"is-full-info": True}
        )["data"]

        field_response= field
        if field == "phone_number":
            field_response = "phoneNumber"
            assert (updated_data[field_response] == data[field]), f"User {field} is not updated."
        elif field == "mailing_address":
            for address in updated_data["addresses"]:
                if (address["addressType"] == "WORK_ADDRESS"):
                    assert (address["isMailingAddress"] == True), f"User {field} is not updated."
        elif field in ("name" , "email"):
            assert (updated_data[field_response] == data[field]), f"User {field} is not updated."
        else:
            field_response = "nextOfKin"
            assert (updated_data[field_response] == data["name"] and updated_data["relationship"] == data["relationship"]), f"User {field} is not updated."
        context.data["users"][uid][
            "user_details_response"
        ] = updated_data

    retry_check_details()
