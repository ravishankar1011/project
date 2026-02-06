from behave import *
from tests.util.common_util import check_status_portal
import tests.api.portal.uims.uims_hepler as uh

use_step_matcher("re")

@When("I create a role ([^']*) with following details")
def create_role_step(context, rid):
    request = context.request
    row = context.table.rows[0]
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"],
        "x-customer-profile-id": context.data["customer_profile_id"]
    }
    context.data["roles"] = (
        {} if context.data.get("roles", None) is None else context.data["roles"]
    )
    context.data["roles"][rid] = {}
    payload = {
        "customer_profile_id": context.data["customer_profile_id"],
        "role_name": row["role_name"],
        "description": row["description"]
    }
    response = request.hugoportal_post_request(
        path = uh.admin_role_urls["create_role"],
        headers = headers,
        data = payload
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"
    context.data["roles"][rid] = response["data"]

@Then("I add page ([^']*) and widget ([^']*) to logged_in_user role")
def add_page_widget_to_role(context, pid, wid):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    payload = {
        "page_widgets": [
            {
                "page_code": context.data["pages"][pid]["pageCode"],
                "widget_code": context.data["widgets"][wid]["widgetCode"]
            }
        ]
    }
    logged_in_user_role_id = context.data["logged_in_user_role_id"]
    response = request.hugoportal_post_request(
        path = uh.admin_role_urls["add_role_page_widget"] + "/" + logged_in_user_role_id + "/page-widget",
        headers = headers,
        data = payload
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"

@Step("I add resource ([^']*) and widget ([^']*) to logged_in_user role")
def add_resource_role(context, rid, wid):

    payload = {
        "widget_resource": [
            {
                "resource_code": context.data["resources"][rid]["resourceCode"],
                "widget_code": context.data["widgets"][wid]["widgetCode"],
                "permitted_action": "WRITE"
            }
        ]
    }
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    role_id = context.data["logged_in_user_role_id"]
    response = context.request.hugoportal_post_request(
        path=uh.admin_role_urls["add_role_widget_resource"] + "/" + role_id + "/widget-resource",
        headers=headers,
        data=payload
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"


@When("I update the role ([^']*) with the following details and verified updated details")
def update_role_step(context, rid):
    row = {heading: context.table.rows[0][i] for i, heading in enumerate(context.table.headings)}
    role_id = context.data["roles"][rid]["roleId"]
    payload = {
        "role_name": row["role_name"],
        "description": row["description"]
    }
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"],
        "x-customer-profile-id": context.data["customer_profile_id"]
    }
    response = context.request.hugoportal_put_request(
        path = uh.admin_role_urls["update_role"] + f"/{role_id}",
        data = payload,
        headers = headers
    )

    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"
    response = context.request.hugoportal_get_request(
        path=uh.admin_role_urls["get_role"] + f"/{role_id}",
        headers=headers
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"
    data = response["data"]
    assert data["roleName"] == row["role_name"]
    assert data["description"] == row["description"]

@then("I delete the created role")
def delete_role_step(context):
    role_id = context.data["role_id"]
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }

    response = context.request.hugoportal_delete_request(
        path=uh.role_urls["delete_role"] + f"/{role_id}",
        headers=headers
    )
    check_status_portal(response, 200)

@Step("I create a role ([^']*) with permission and checker_group as ([^']*)")
def create_role_with_permission(context, rid, gid):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    context.data["roles"] = (
        {} if context.data.get("roles", None) is None else context.data["roles"]
    )
    context.data["roles"][rid] = {}
    page = context.data["permission"] ["permissions"] ["pages"] [0]
    widget = page["widgets"][0]
    resource = widget["resources"][0]
    action = resource["action"]
    permitted_action = ""
    if "WRITE" in action:
        permitted_action = "WRITE"
    elif "READ" in action:
        permitted_action = "READ"
    elif permitted_action == "RESTRICTED_READ":
        permitted_action = "RESTRICTED_READ"
    else:
        permitted_action = "NO_ACCESS"
    body = {
        "role" : {
            "role_name": "integration test",
            "description": "creating a role for integration test",
            "customer_profile_id": context.data["customer_profile_id"]
        },
        "pages": [
            {
                "page_code": page["pageCode"],
                "widgets": [
                    {
                        "widget_code": widget["widgetCode"],
                        "checker_group_id": context.data["groups"][gid]["groupId"],
                        "resources": [
                            {
                                "resource_code": resource["resourceCode"],
                                "action": permitted_action
                            }
                        ]
                    }
                ]
            }
        ]
    }
    response = request.hugoportal_post_request(
        path=uh.role_urls["create_role_with_permission"],
        headers=headers,
        data=body
    )
    context.data["roles"][rid]["permission"] = body
    context.data["roles"][rid]["roleId"] = response["data"]["roleId"]

@Step("I fetched the permission of ([^']*) and verified")
def fetch_permission_and_verify(context, rid):
    """
    Fetches the permission of a given role ID
    """
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    response = request.hugoportal_get_request(
        path = uh.role_urls["get_role"] + "/" + context.data["roles"][rid]["roleId"],
        headers = headers
    )
    expected_data = context.data["roles"][rid]["permission"]
    assert response["data"]["roleName"] == expected_data["role"]["role_name"]
    assert response["data"]["description"] == expected_data["role"]["description"]
    expected_pages = expected_data["pages"]
    actual_pages = response["data"]["permissions"]["pages"]

    assert len(actual_pages) == len(expected_pages), "Number of pages do not match."

    page_to_verify = actual_pages[0]
    expected_page = expected_pages[0]

    assert page_to_verify["pageCode"] == expected_page["page_code"], "Page code does not match."

    expected_widgets = expected_page["widgets"]
    actual_widgets = page_to_verify["widgets"]

    assert len(actual_widgets) == len(expected_widgets), "Number of widgets do not match."

    widget_to_verify = actual_widgets[0]
    expected_widget = expected_widgets[0]

    assert widget_to_verify["widgetCode"] == expected_widget["widget_code"], "Widget code does not match."
    assert widget_to_verify["checkerGroupId"] == expected_widget["checker_group_id"], "Checker Group ID does not match."

    expected_resources = expected_widget["resources"]
    actual_resources = widget_to_verify["resources"]
    expected_resource = expected_resources[0]
    is_found = any(
        resource["resourceCode"] == expected_resource["resource_code"] and
        resource["action"] == expected_resource["action"]
        for resource in actual_resources
    )
    assert is_found, f"Verification failed: The expected resource {expected_resource} was not found."
