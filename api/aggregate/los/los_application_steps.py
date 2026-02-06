import uuid

from tests.api.aggregate.los import los_helper
from behave import *

use_step_matcher("re")

@Then("I create following LOS Application and verify status as ([^']*)")
def create_los_application(context, status):
    request = context.request
    for row in context.table:

        if row["journey_code"] in context.data :
            journey_code = context.data[row["journey_code"]]
        else:
            journey_code = str(uuid.uuid4())

        if row["end_customer_profile_id"] in context.data :
            end_customer_profile_id = context.data[row["end_customer_profile_id"]].end_customer_profile_id
        else:
            end_customer_profile_id = str(uuid.uuid4())

        if row["input_data_case"] == 'UNKNOWN_CUSTOMER':
            customer_profile_id = str(uuid.uuid4())
        else :
            customer_profile_id = context.data["config_data"]["customer_profile_id"]

        if row["input_data_case"] == 'MISSING_INPUT_DATA':
            request_body = {
                "journey_code": journey_code,
                "end_customer_profile_id": end_customer_profile_id
            }
        else:
            input_data =  los_helper.get_application_input_data(row["input_data_case"], context, "PARAM_1")
            request_body = {
                "journey_code": journey_code,
                "end_customer_profile_id": end_customer_profile_id,
                "input_data": input_data
            }

        response = request.hugoserve_post_request(
            los_helper.los_application_urls['create'],
            data=request_body,
            headers=los_helper.get_headers(customer_profile_id),
        )
        assert response.get('headers').get('status_code') == status
        application_id = response.get("data", {}).get("application_id")
        if application_id:
            context.data[row["application_identifier"]] = application_id

@Then("I Evaluate Application ([^']*) and verify status as ([^']*)")
def evaluate_application(context,application_identifier, status):
    request = context.request
    customer_profile_id = context.data["config_data"]["customer_profile_id"]
    if application_identifier not in context.data :
        application_id = str(uuid.uuid4())
    else:
        application_id = context.data.get(application_identifier)

    response = request.hugoserve_put_request(
        los_helper.los_application_urls["evaluate"].replace("$application_id$", application_id),
        headers=los_helper.get_headers(customer_profile_id),
    )
    assert response.get('headers').get('status_code') == status
