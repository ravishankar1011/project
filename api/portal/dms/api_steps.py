from behave import *
import tests.api.portal.dms.dms_helper as dh
from tests.util.common_util import check_status_portal

use_step_matcher("re")

@Step("I create an api ([^']*) with api_code ([^']*) and data_provider_id ([^']*) with field ([^']*) with field_code ([^']*)")
def add_api(context, aid, api_code, data_provider_id, fid, field_code):
    request = context.request
    context.data["apis"] = (
        {} if context.data.get("apis", None) is None else context.data["apis"]
    )
    context.data["fields"] = (
        {} if context.data.get("fields", None) is None else context.data["fields"]
    )
    context.data["apis"][aid] = {}
    context.data["fields"][fid] = {}
    api_request_dto = dh.api_request_dto
    if api_code == "random":
        api_code = "it-api-" + dh.generate_random_string(10)
    if field_code == "random":
        field_code = "it-field-" + dh.generate_random_string(10)
    api_request_dto["api_details"]["api_code"] = api_code
    api_request_dto["api_details"]["data_provider_id"] = data_provider_id
    api_request_dto["fields"][0]["field_code"] = field_code
    api_response = request.hugoportal_post_request(
        path = dh.api_urls["add_api"],
        headers = dh.get_principal_id_and_access_key(),
        data = api_request_dto
    )
    if not check_status_portal(api_response, 200):
        assert (
            False
        ), f"the received response is {api_response}"
    context.data["apis"][aid] = api_response["data"]
    context.data["fields"][fid] = api_response["data"]["fields"][0]

@Step("I add a new field ([^']*) with field_code ([^']*) to api ([^']*) and dependent_field as ([^']*)")
def add_fields_to_an_existing_api(context, fid, field_code, aid, dependent_field_identifier):
    request = context.request
    field_request_dto = dh.field_request_dto
    if dependent_field_identifier != "none":
        dependent_field_code = context.data["fields"][dependent_field_identifier]["fieldCode"]
        field_request_dto["dependent_field_codes"] = [dependent_field_code]
    if field_code == "random":
        field_code = "it-field-" + dh.generate_random_string(10)
    field_request_dto["field_code"] = field_code
    field_request_dto = {
        "fields": [field_request_dto]
    }
    api_response = request.hugoportal_put_request(
        path = f'{dh.api_urls["add_fields"]}/{context.data["apis"][aid]["api"]["apiId"]}/add-fields',
        headers = dh.get_principal_id_and_access_key(),
        data = field_request_dto
    )
    if not check_status_portal(api_response, 200):
        assert (
            False
        ), f"the received response is {api_response}"
    added_fields = api_response["data"].get("fields", [])
    matched_field = next((f for f in added_fields if f.get("fieldCode") == field_code), None)
    assert matched_field is not None, f"Field with code '{field_code}' not found in response: {added_fields}"
    context.data["fields"][fid] = matched_field

@Step("I fetch API ([^']*) and verify that field ([^']*) is present, and that field ([^']*) is a dependent field of FID2")
def verify_added_fields(context, aid, fid2, fid1):
    request = context.request
    api_id = context.data["apis"][aid]["api"]["apiId"]
    response = request.hugoportal_get_request(
        path=f'{dh.api_urls["get_api"]}/{api_id}',
        headers=dh.get_principal_id_and_access_key()
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"

    fields = response["data"].get("fields", [])
    fid2_code = context.data["fields"][fid2]["fieldCode"]
    fid2_entry = next((f for f in fields if f["fieldCode"] == fid2_code), None)
    fid1_id = context.data["fields"][fid1]["fieldId"]
    fid1_code = context.data["fields"][fid1]["fieldCode"]
    assert fid2_entry is not None, f"Field {fid2_code} not found in API {aid}"

    fid1_entry = next((f for f in fields if f["fieldCode"] == fid1_code), None)
    assert fid1_entry is not None, f"Field {fid1_code} not found in API {aid}"
    dependent_codes = fid2_entry.get("dependentFieldIds", [])
    assert fid1_id in dependent_codes, (
        f"Field {fid2_code} does not list {fid1_code} as a dependent field. "
        f"Found dependencies: {dependent_codes}"
    )
