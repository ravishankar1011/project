from behave import *
import tests.api.portal.uims.uims_hepler as uh
from tests.util.common_util import check_status_portal

use_step_matcher("re")

@Step("I fetch all the permissions the logged-in user has")
def fetch_permission_for_role_creation(context):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    response = request.hugoportal_get_request(
        path = uh.permission_urls["fetch_permission_for_role_creation"],
        headers = headers
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"
    context.data["permission"] = response["data"]
