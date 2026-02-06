from typing import List
from behave import *
import tests.api.portal.uims.uims_hepler as uh
from tests.api.portal.dms.field_steps import update_input_config_and_verify_step
from tests.api.portal.uims.uims_dataclass import CreateOperator
from tests.ui.hugosave_automation.features.steps.data_class_parser import DataClassParser
from tests.util.common_util import check_status_portal

use_step_matcher("re")

@when("I create an operator ([^']*) with role ([^']*) and group ([^']*)")
def create_operator(context, uid, rid, gid):
    request = context.request
    context.data["users"] = (
        {} if context.data.get("users", None) is None else context.data["users"]
    )
    context.data["users"][uid] = {}
    operators : List[CreateOperator] = DataClassParser.parse_rows(
        context.table.rows, data_class=CreateOperator
    )
    operator = operators[0]
    if operator.email == "random":
        generated_email = "abc" + uh.get_rand_number(6) + ".kumar@gmail.com"
        operator.email = generated_email

    if rid != "none":
        operator.role_id = context.data["roles"][rid]["roleId"]
    if gid != "none":
        operator.group_id = context.data["groups"][gid]["groupId"]

    operator.customer_profile_id = context.data["customer_profile_id"]
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    response = request.hugoportal_post_request(
        path = uh.admin_user_urls["create_operator"],
        headers = headers,
        data = operator.get_dict()
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"
    context.data["users"][uid] = response["data"]

@then("I verify the operator with email ([^']*) is present in DB or not")
def verify_operator(context, email):
    request = context.request

    user_id = context.data.get("userId")
    new_user_id = context.data.get("newCreatedUserId")
    assert user_id and new_user_id, "Missing userId or newUserId in context.data"
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    response = request.hugoportal_get_request(
        path=uh.user_urls["get_user"] + "/" + new_user_id,
        headers=headers
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"

@when("I Update role of user ([^']*) to ([^']*)")
def update_user_role(context, uid, rid):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    body = {
        "role_id": context.data["roles"][rid]["roleId"]
    }
    response = request.hugoportal_put_request(
        path = uh.user_urls["update_user"] + "/" + context.data["logged_in_user_id"] + "/role",
        headers = headers,
        data = body
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"

@when("I add 123 user ([^']*) to group ([^']*)")
def add_user_to_group(context, uid, gid):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    body = {
        "group_id": context.data["groups"][gid]["groupId"]
    }
    response = request.hugoportal_put_request(
        path = uh.user_urls["update_user"] + "/" + context.data["logged_in_user_id"] + "/group",
        headers = headers,
        data = body
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"

@Then("I fetch user ([^']*) and verified the details")
def fetch_user_and_verify(context, uid):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    response = request.hugoportal_get_request(
        path = uh.admin_user_urls["get_user"] + "/" + context.data["users"][uid]["userId"],
        headers = headers
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"
    user = context.data["users"][uid]
    get_user = response["data"]
    assert user["userId"] == get_user["userId"]
    assert user["userName"] == get_user["userName"]
    assert user["customerProfileId"] == get_user["customerProfileId"]
    assert user["firstName"] == get_user["firstName"]
    assert user["lastName"] == get_user["lastName"]
    assert user["email"] == get_user["email"]
    assert user["phoneNumber"] == get_user["phoneNumber"]
    assert user["role"]["roleId"] == get_user["role"]["roleId"]
    assert user["group"]["groupId"] == get_user["group"]["groupId"]

@Then("I update group of user ([^']*) to ([^']*)")
def update_user_group(context, uid, gid):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    payload = {
        "group_id": context.data["groups"][gid]["groupId"]
    }
    user_id = context.data["users"][uid]["userId"]
    response = request.hugoportal_put_request(
        path = uh.admin_user_urls["add_group"] + "/" + user_id + "/group",
        headers = headers,
        data = payload
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"


@Then("I update role of user ([^']*) to ([^']*)")
def update_user_group(context, uid, rid):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    payload = {
        "role_id": context.data["roles"][rid]["roleId"]
    }
    user_id = context.data["users"][uid]["userId"]
    response = request.hugoportal_put_request(
        path = uh.admin_user_urls["add_role"] + "/" + user_id + "/role",
        headers = headers,
        data = payload
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"

@Then("I fetch user ([^']*) and verified ([^']*) and ([^']*) is present or not")
def fetch_and_verify_details(context, uid, gid, rid):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    user_id = context.data["users"][uid]["userId"]
    response = request.hugoportal_get_request(
        path = uh.admin_user_urls["get_user"] + "/" + user_id,
        headers = headers
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"
    assert context.data["roles"][rid]["roleId"] == response["data"]["role"]["roleId"]
    assert context.data["groups"][gid]["groupId"] == response["data"]["group"]["groupId"]
