from behave import *
import tests.api.portal.uims.uims_hepler as uh
from tests.util.common_util import check_status_portal

use_step_matcher("re")

@When("I fetch my details")
def fetch_logged_in_user_details(context):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    response = request.hugoportal_get_request(
        path = uh.data_urls["read"] + "/view-logged-in-operator-profile" + "/read",
        headers = headers
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"
    context.data["widget_data_snapshot_id"] = response["data"]["widgetDataSnapshotId"]

@Step("I try to update my details")
def update_user_details(context):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    pay_load = {
        "input_data": {
            "view-logged-in-operator-profile-first-name": uh.generate_random_string() + "Updated first name",
            "view-logged-in-operator-profile-last-name": uh.generate_random_string() + "Updated last name",
            "view-logged-in-operator-profile-phone-number": "+92" + uh.get_rand_number(6)
        },
        "widget_data_snapshot_id": context.data["widget_data_snapshot_id"]
    }

    response = request.hugoportal_post_request(
        path = uh.data_urls["update"] + "/view-logged-in-operator-profile" + "/view-logged-in-operator-profile" + "/update",
        headers = headers,
        data = pay_load
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"

    if (response["data"]["draftId"]):
        context.data["draft_id"] = response["data"]["draftId"]
    else:
        raise ValueError("Operation failed: Response did not contain a valid draft ID.")
