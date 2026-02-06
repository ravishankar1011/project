from tests.api.aggregate.los import los_helper
from behave import *

use_step_matcher("re")

@Then("I onboard Customer Profile ([^']*) to LOS and verify onboard status as ([^']*)")
def onboard_customer_profile(context, customer_identifier, expected_onboard_status):
    request = context.request
    customer_profile_dto = context.data.get(customer_identifier)
    customer_id = customer_profile_dto.customer_id
    customer_profile_id = customer_profile_dto.customer_profile_id

    data = {
        "customer_id": customer_id,
        "customer_profile_id": customer_profile_id,
    }

    response = request.hugoserve_post_request(
        los_helper.admin_urls["onboard_customer_profile"],
        data=data
    )

    assert (
            response["data"]["onboard_status"] == "ONBOARD_SUCCESS"
            or response["data"]["onboard_status"] == expected_onboard_status
    )

@Then("I get LOS Journeys for the customer and verify status as ([^']*)")
def get_los_journeys_for_a_customer(context, expected_status):
    request = context.request
    customer_profile_id = context.data["config_data"]["customer_profile_id"]

    response = request.hugoserve_get_request(
        los_helper.customer_profile_urls['get_customer_profile_journeys'],
        headers=los_helper.get_headers(customer_profile_id)
    )
    assert (response["headers"]["status_code"] == expected_status)
