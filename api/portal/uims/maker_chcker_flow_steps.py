from behave import *
import tests.api.portal.uims.uims_hepler as uh
from tests.util.common_util import check_status_portal

use_step_matcher("re")

@Step("I create a role ([^']*) with all the permissions that the logged-in user has and add the checker group as ([^']*)")
def create_role_with_permission(context, rid, gid):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    context.data["roles"] = (
        {} if context.data.get("roles", None) is None else context.data["roles"]
    )
    context.data["roles"][gid] = {}
    permission_data = context.data["permission"]
    pages = permission_data["permissions"]["pages"]
    page_permissions = []
    for page in pages:
        widget_permissions = []
        for widget in page["widgets"]:
            resource_permissions = []
            for resource in widget["resources"]:
                actions = resource.get("action", [])
                if "WRITE" in actions:
                    resolved_action = "WRITE"
                elif "READ" in actions:
                    resolved_action = "READ"
                else:
                    resolved_action = "NO_ACCESS"

                resource_permissions.append({
                    "resource_code": resource["resourceCode"],
                    "action": resolved_action
                })
            widget_permission = {
                "widget_code": widget["widgetCode"],
                "checker_group_id": context.data["groups"][gid]["groupId"],
                "resources": resource_permissions
            }
            widget_permissions.append(widget_permission)
        page_permissions.append({
            "page_code": page["pageCode"],
            "widgets": widget_permissions
        })
    customer_profile_id = context.data["customer_profile_id"]
    payload = {
        "role": {
            "role_name": "integration test maker-checker role",
            "description": "creating a role for integration test",
            "customer_profile_id": customer_profile_id
        },
        "pages": page_permissions
    }

    response = request.hugoportal_post_request(
        path = uh.role_urls["create_role_with_permission"],
        headers = headers,
        data = payload
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"
    context.data["roles"][rid] = response["data"]

@Then("I update user role of user with user_id ([^']*) to ([^']*)")
def update_user_role(context, user_id, rid):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    payload = {
        "role_id": context.data["roles"][rid]["roleId"]
    }
    response = request.hugoportal_put_request(
        path = uh.admin_user_urls["update_user"] + "/" + user_id + "/role",
        headers = headers,
        data = payload
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"

@Step("I add user with user_id ([^']*) to group ([^']*)")
def add_user_to_group(context, user_id, gid):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    payload = {
        "group_id": context.data["groups"][gid]["groupId"]
    }
    response = request.hugoportal_put_request(
        path = uh.admin_user_urls["update_user"] + "/" + user_id + "/group",
        headers = headers,
        data = payload
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"

@Step("I try to approve draft with expected status code ([^']*)")
def approve_draft(context, expected_status_code):
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    path = uh.data_urls["create"] + "/draft" + "/" + context.data["draft_id"] + "/approve-draft"
    response = context.request.hugoportal_post_request(
        path = path,
        headers = headers
    )
    if not check_status_portal(response, expected_status_code):
        assert False, f"The received response is: {response}"
