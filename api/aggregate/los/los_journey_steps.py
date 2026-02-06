import uuid

from tests.api.aggregate.los import los_helper
from behave import *

use_step_matcher("re")

@Then("I create following LOS Journey and verify status as ([^']*)")
def create_los_journey(context, status):
  request = context.request
  customer_profile_id = context.data["config_data"]["customer_profile_id"]
  for row in context.table:
    los_journey_code = str(uuid.uuid4())
    journey_name = row["journey_name"]
    description = row["description"]
    rule_case = row["rules_case"]
    if rule_case == 'unknown_customer_profile':
      customer_profile_id = str(uuid.uuid4())
    if rule_case == 'unknown_param_code':
      param_code = str(uuid.uuid4())
    else:
      param_code = row["param_code"]
      param_code = context.param_map.get(param_code)

    request_body = {
        "journey_code": los_journey_code,
        "description": description
      }

    if rule_case != 'empty_journey_rules':
      request_body["journey_rules"] = los_helper.get_journey_rule_config(rule_case, param_code)
    if rule_case != 'missing_mandatory_fields':
      request_body["journey_name"] = journey_name

    response = request.hugoserve_post_request(
      los_helper.los_journey_urls['create'],
      data=request_body,
      headers=los_helper.get_headers(customer_profile_id),
    )
    assert response.get('headers').get('status_code') == status
    if status == '200':
      context.data[row["journey_code"]] = los_journey_code
      journey_id = response.get("data", {}).get("journey_id")
      if journey_id:
        context.data[row["journey_identifier"]] = journey_id

@Then("I get Journey params for a journey code ([^']*) and verify status as ([^']*)")
def get_journey_params(context,journey_code, status_code):
  request = context.request
  customer_profile_id = context.data["config_data"]["customer_profile_id"]

  if  context.data.get(journey_code) is not None:
    los_journey_code = context.data.get(journey_code)
  else:
    los_journey_code = str(uuid.uuid4())

  response = request.hugoserve_get_request(
    los_helper.los_journey_urls['get_journey_params'].replace('$journey_code$', los_journey_code),
    headers=los_helper.get_headers(customer_profile_id),
  )

  assert response.get('headers').get('status_code') == status_code

@Then("I get applications for a journey code ([^']*) and verify journey id ([^']*) and status as ([^']*)")
def get_applications_for_journey(context, journey_code,journey_identifier, status):
  request = context.request
  customer_profile_id = context.data["config_data"]["customer_profile_id"]

  if context.data.get(journey_code) is not None:
    los_journey_code = context.data.get(journey_code)
  else:
    los_journey_code = str(uuid.uuid4())

  response = request.hugoserve_get_request(
    los_helper.los_journey_urls['get_journey_applications'].replace('$journey_code$', los_journey_code),
    headers=los_helper.get_headers(customer_profile_id),
  )

  assert response.get('headers').get('status_code') == status
  if status == '200':
    assert response.get('data').get('applications')[0].get('journey_id') == context.data.get(journey_identifier)
