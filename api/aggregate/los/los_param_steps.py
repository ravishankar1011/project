import uuid

from tests.api.aggregate.los import los_helper
from behave import *

use_step_matcher("re")

@Then("I create following LOS Params and verify status")
def create_los_param(context):
    request = context.request
    customer_profile_id = context.data["config_data"]["customer_profile_id"]

    if not hasattr(context, "param_map"):
        context.param_map = {}

    for row in context.table:
        param_code = str(uuid.uuid4())
        condition_config_case = row['condition_config_case']
        is_active = row['is_active'].lower() == 'true'
        description = row['description']
        condition_config = los_helper.get_condition_config(condition_config_case, param_code)
        request_payload = {
            "param_code" : param_code,
            "condition_config": condition_config,
            "is_active" : is_active,
            "description": description,
        }
        headers = los_helper.get_headers(customer_profile_id)
        response = request.hugoserve_post_request(
            los_helper.los_param_urls["create"],
            data= request_payload,
            headers=headers
        )
        expected_status_code = row["status_code"]
        assert response.get('headers').get('status_code') == expected_status_code
        param_identifier = row["param_identifier"]
        context.param_map[param_identifier] = param_code
