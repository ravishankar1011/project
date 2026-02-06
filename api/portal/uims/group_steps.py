from typing import List
from behave import *
import tests.api.portal.uims.uims_hepler as uh
from tests.api.portal.uims.uims_dataclass import CreateGroup
from tests.ui.hugosave_automation.features.steps.data_class_parser import DataClassParser
from tests.util.common_util import check_status_portal

use_step_matcher("re")

@Step("I create a group ([^']*) with role ([^']*)")
def create_group(context, gid, rid):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "x-customer-profile-id": context.data["customer_profile_id"]
    }
    context.data["groups"] = (
        {} if context.data.get("groups", None) is None else context.data["groups"]
    )
    context.data["groups"][gid] = {}
    groups: List[CreateGroup] = DataClassParser.parse_rows(
        context.table.rows, data_class=CreateGroup
    )
    group = groups[0]
    if rid != "none":
        group.role_id = context.data["roles"][rid]["roleId"]
    else:
        group.role_id = ""
    group.customer_profile_id = context.data["customer_profile_id"]

    response = request.hugoportal_post_request(
        path = uh.group_urls["create_group"],
        headers = headers,
        data = group.get_dict()
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"
    context.data["groups"][gid] = response["data"]

@Then("I update group_name, group_description of group ([^']*) and verified the updated details")
def update_and_verify_group(context, gid):
    request = context.request
    row = context.table.rows[0]
    group_id = context.data["groups"][gid]["groupId"]
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "x-customer-profile-id": context.data["customer_profile_id"]
    }
    payload = {
        "group_name": row["group_name"],
        "description": row["group_description"]
    }
    response = request.hugoportal_put_request(
        path = uh.group_urls["update_group"] + "/" + group_id,
        headers = headers,
        data = payload
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"

    updated_group_details = request.hugoportal_get_request(
        path=uh.group_urls["get_group"] + "/" + group_id,
        headers=headers
    )
    if not check_status_portal(updated_group_details, 200):
        assert False, f"The received response is: {updated_group_details}"
    assert updated_group_details["data"]["groupName"] == row["group_name"], "Updated group name does not match."
    assert updated_group_details["data"]["description"] == row["group_description"], "Updated group description does not match."
    print(f"Successfully updated and verified details for group ID: {group_id}")

@Then("I update role as ([^']*) of group ([^']*) and verified the updated details")
def update_group_role_and_verify_group(context, rid, gid):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "x-customer-profile-id": context.data["customer_profile_id"]
    }
    payload = {
        "role_id": context.data["roles"][rid]["roleId"]
    }
    group_id = context.data["groups"][gid]["groupId"]
    response = request.hugoportal_put_request(
        path = uh.group_urls["update_group"] + "/" + group_id,
        headers = headers,
        data = payload
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"

    updated_group_details = request.hugoportal_get_request(
        path=uh.group_urls["get_group"] + "/" + group_id,
        headers=headers
    )
    if not check_status_portal(updated_group_details, 200):
        assert False, f"The received response is: {updated_group_details}"
    assert updated_group_details["data"]["roleId"] == context.data["roles"][rid]["roleId"], "Updated group role does not match."
