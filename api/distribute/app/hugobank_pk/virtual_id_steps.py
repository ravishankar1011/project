from behave import *

import tests.api.distribute.app_helper as ah
from tests.util.common_util import check_status_distribute

use_step_matcher("re")

@Step("I link the raast ID for the user ([^']*)")
def step_impl(context, user_profile_identifier):
    request = context.request
    data = {
        "virtual_id_details": {
            "virtual_id_type": "MOBILE",
            "virtual_id_value": context.data["users"][user_profile_identifier]["user_name"]
        },
        "account_id": ah.get_cash_wallet_id(context, user_profile_identifier),
    }
    headers = ah.get_user_header(context, user_profile_identifier)
    headers["x-final-user-authorisation-token"] = context.data["users"][
        user_profile_identifier
    ]["user_authorisation_token"]
    response = request.hugosave_post_request(
        path=ah.virtual_id_urls["link"],
        data=data,
        headers=headers
    )
    check_status_distribute(response, expected_status=200)


@Step("I verify the raast ID is linked successfully for the user ([^']*)")
def step_impl(context, user_profile_identifier):
    user_data = context.data["users"][user_profile_identifier]
    mobile_number = user_data["mobile_number"]

    params = {
        "virtual-id-type": "MOBILE",
        "virtual-id-value": mobile_number
    }

    response = context.request.hugosave_get_request(
        path=ah.virtual_id_urls["link"],
        headers=ah.get_user_header(context, user_profile_identifier),
        params=params,
    )

    if response.status_code == 200:
        status_in_response = response.data.get("status")
        expected_status = "VIRTUAL_ID_LINKED"
        assert status_in_response == expected_status, f"Expected status '{expected_status}', but got '{status_in_response}'"
        context.data["users"][user_profile_identifier]["raast_id"] = mobile_number
        mobile_number_str = str(mobile_number)
        raast_id = mobile_number_str[2:]
        context.data["users"][user_profile_identifier]["raast_id"] = raast_id


@Step("I add the user ([^']*) as Payee ([^']*) to the user ([^']*) using raast ID")
def step_impl(context, payee_profile_identifier, payee_identifier, user_profile_identifier):
    request = context.request
    mobile_number = context.data["users"][payee_profile_identifier]["user_name"]
    raast_id = mobile_number[4:]
    name = context.data["users"][payee_profile_identifier]["user_details_response"]["name"]
    data = ah.get_payee_with_raast(context, name, raast_id)
    headers = ah.get_user_header(context, user_profile_identifier)
    headers["x-final-user-authorisation-token"] = context.data["users"][user_profile_identifier]["user_authorisation_token"]
    response = request.hugosave_post_request(
        path=ah.payee_urls["root"],
        data=data,
        headers=headers
    )
    assert check_status_distribute(response,"200")
    context.data["users"][user_profile_identifier][payee_identifier] = response["data"]


@Step("I create a virtual ID for the user ([^']*)")
def step_impl(context, user_profile_identifier):
    request = context.request
    data = {
        "virtual_id_details": {
            "virtual_id_type": "MOBILE",
            "virtual_id_value": context.data["users"][user_profile_identifier]["user_name"]
        }
    }
    headers = ah.get_user_header(context, user_profile_identifier)
    headers["x-final-user-authorisation-token"] = context.data["users"][
        user_profile_identifier
    ]["user_authorisation_token"]
    response = request.hugosave_post_request(
        path=ah.virtual_id_urls["create"],
        data=data,
        headers=headers
    )
    assert check_status_distribute(response, "200")


@Step("I check if the virtual ID is linked successfully for the user ([^']*)")
def step_impl(context, user_profile_identifier):
    user_data = context.data["users"][user_profile_identifier]
    mobile_number = user_data["mobile_number"]

    params = {
        "virtual-id-type": "MOBILE",
        "virtual-id-value": mobile_number
    }

    response = context.request.hugosave_get_request(
        path=context.ah.virtual_id_urls["link"],
        headers=context.ah.get_user_header(context, user_profile_identifier),
        params=params,
    )
    assert check_status_distribute(response, "200"), f"Expected status code 200, but got {response.status_code}"


@Step("I check if the raast ID of user ([^']*) is added as payee ([^']*) to user ([^']*)")
def step_impl(context, payee_profile_identifier, payee_identifier, user_profile_identifier):

    request = context.request

    response = request.hugosave_get_request(
        ah.user_profile_urls["payees-list"],
        headers=ah.get_user_header(context, user_profile_identifier),
    )
    payee_list = response["data"]
    payee_id = context.data["users"][user_profile_identifier][payee_identifier]["payeeId"]
    if check_status_distribute(response, "200") and len(payee_list['payees']) == 1:
        context.data["users"][user_profile_identifier]["payees"] = (
            {}
            if context.data["users"][user_profile_identifier].get("payees", None)
               is None
            else context.data["users"][user_profile_identifier]["payees"]
        )
        context.data["users"][user_profile_identifier]["payees"][payee_profile_identifier] = {
            "id": payee_id,
            "updated_data": {},
        }
