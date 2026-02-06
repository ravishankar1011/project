from behave import *
import tests.api.distribute.app_helper as ah
from tests.util.common_util import check_status_distribute

use_step_matcher("re")


@Step("I get user details for user ([^']*) and the user profile status should be ([^']*)")
def step_impl(context, uid, expected_status):
    request = context.request

    headers = ah.get_device_authorisation_header(context, uid)
    response = request.hugosave_get_request(
        path=ah.user_profile_urls["details"], headers=headers, params={"is-full-info": True}
    )
    if uid not in context.data["users"]:
        context.data["users"][uid] = {}

    if check_status_distribute(response, "200"):
        assert response["data"]["userStatus"] == expected_status
        context.data["users"][uid]["user_details_response"] = response["data"]
