import uuid

from tests.api.aggregate.los import los_helper
from behave import *

from tests.util.common_util import check_status

use_step_matcher("re")


@Then(
    "I onboard End Customer Profile ([^']*) to LOS and verify onboard status as ([^']*) and status code as ([^']*)"
)
def onboard_end_customer_profile(
        context, end_customer_profile_id, expected_onboard_status, expected_status_code
):
    request = context.request

    customer_profile_id = context.data["config_data"]["customer_profile_id"]
    end_customer_profile_id = str(uuid.uuid4())
    data = {
        "end_customer_profile_id": end_customer_profile_id,
    }
    response = request.hugoserve_post_request(
        los_helper.end_customer_profile_urls["onboard"],
        data=data,
        headers=los_helper.get_headers(customer_profile_id),
    )
    check_status(response, expected_status_code)
    if "data" in response:
        assert (
                response["data"]["onboard_status"] == "ONBOARD_SUCCESS"
                or response["data"]["onboard_status"] == expected_onboard_status
        )
