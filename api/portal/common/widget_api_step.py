from behave import *
import tests.api.portal.uims.uims_hepler as uh
from tests.util.common_util import check_status_portal

use_step_matcher("re")

@Step("I list all the the logs ([^']*) using paginated widget ([^']*) that call paginated api access-logs and I verify expected status code as ([^']*)")
def list_all_logs(context, access_logs, widget_code, expected_status_code):
    request = context.request
    context.data["access_logs"] = (
        {} if context.data.get("access_logs", None) is None else context.data["access_logs"]
    )
    context.data["access_logs"][access_logs] = {}
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    response = request.hugoportal_get_request(
        path = uh.data_urls["read"] + f"/{widget_code}" + "/read",
        headers=headers
    )
    if not check_status_portal(response, expected_status_code):
        assert False, f"The received response is: {response}"
    context.data["access_logs"][access_logs] = response["data"]["paginatedData"]["rows"]

@Step("I fetch details of one access log using detailed widget ([^']*) that call detailed read API log-details and I verify expected status code as ([^']*)")
def list_all_logs(context, widget_code, expected_status_code):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    resource_code = "log-details-log-id"
    resource_code_value = context.data["access_logs"]["access_logs"][0]["access-logs-log-id"]
    response = request.hugoportal_get_request(
        path=(
            uh.data_urls["read"]
            + f"/{widget_code}/read"
            + f"?{resource_code}={resource_code_value}"
        ),
        headers=headers
    )
    if not check_status_portal(response, expected_status_code):
        assert False, f"The received response is: {response}"

@Step("I fetch my details ([^']*) using update widget ([^']*), detailed API get-logged-in-user-profile and verify expected status code as ([^']*)")
def fetch_details(context, user_details, widget_code, expected_status_code):
    request = context.request
    context.data["get_details"] = (
        {} if context.data.get("get_details", None) is None else context.data["get_details"]
    )
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }

    response = request.hugoportal_get_request(
        path=(
            uh.data_urls["read"]
            + f"/{widget_code}/read"
        ),
        headers=headers
    )
    if not check_status_portal(response, expected_status_code):
        assert False, f"The received response is: {response}"
    context.data["get_details"][user_details] = response["data"]

@Step("I update my details using update widget ([^']*), update API update-logged-in-user-profile and verify updated details")
def update_details(context, widget_code):
    request = context.request
    row = context.table[0]
    first_name = row["first_name"]
    last_name = row["last_name"]
    phone_number = row["phone_number"]
    if first_name == "random":
        first_name = "mrityunjay" + uh.generate_random_string(5)
    if last_name == "random":
        last_name = "kumar" + uh.generate_random_string(5)
    if phone_number == "random":
        phone_number = "+9244" + uh.get_rand_number(5)

    body = {
        "input_data": {
            widget_code + "-" + "first-name": first_name,
            widget_code + "-" + "last-name": last_name,
            widget_code + "-" + "phone-number": phone_number
        },
        "widget_data_snapshot_id": context.data["get_details"]["user_details"]["widgetDataSnapshotId"]
    }
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    response = request.hugoportal_post_request(
        path=(
            uh.data_urls["update"] + f"/{widget_code}"
            + f"/{widget_code}/update"
        ),
        headers=headers,
        data = body
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"

    get_response = request.hugoportal_get_request(
        path=(
            uh.data_urls["read"]
            + f"/{widget_code}/read"
        ),
        headers=headers
    )
    if not check_status_portal(get_response, 200):
        assert False, f"The received response is: {response}"
    detailed_data = get_response["data"]["detailedData"]
    assert detailed_data[widget_code + "-" + "first-name"] == first_name
    assert detailed_data[widget_code + "-" + "last-name"] == last_name
    assert detailed_data[widget_code + "-" + "phone-number"] == phone_number

@Step("I list my permission using permission widget ([^']*) and I verify expected status code as ([^']*)")
def fetch_details(context, widget_code, expected_status_code):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    resource_code = widget_code + "-" + "role-id"
    resource_data = context.data["logged_in_user_role_id"]
    response = request.hugoportal_get_request(
        path=(
            uh.data_urls["read"]
            + f"/{widget_code}/read"
            + f"?{resource_code}={resource_data}"
        ),
        headers = headers
    )
    if not check_status_portal(response, expected_status_code):
        assert False, f"The received response is: {response}"

@Step("I fetch menu widget ([^']*) and I verify expected status code as ([^']*)")
def fetch_details(context, widget_code, expected_status_code):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    response = request.hugoportal_get_request(
        path= uh.widget_urls["get_menu_widget"] + "/menu",
        headers = headers
    )
    if not check_status_portal(response, expected_status_code):
        assert False, f"The received response is: {response}"
