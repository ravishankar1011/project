from typing import Dict, Any
from behave import *
import tests.api.portal.dms.dms_helper as dh
from tests.util.common_util import check_status_portal

use_step_matcher("re")

def parse_bool(val: str) -> bool:
    return val.strip().lower() == "true"

@Step("I create a field ([^']*) of api ([^']*) with field_code ([^']*) and dependent_field ([^']*)")
def create_field(context, fid, aid, field_code, dependent_field_identifier):
    request = context.request
    headers = dh.get_principal_id_and_access_key()
    field_request_dto = dh.field_request_dto
    if field_code == "random":
        field_code  = "it-field-" + dh.generate_random_string(10)
    field_request_dto["field_code"] = field_code
    field_request_dto["api_id"] = context.data["apis"][aid]["api"]["apiId"]
    if dependent_field_identifier != "none":
        field_request_dto["dependent_field_codes"] = [context.data["fields"][dependent_field_identifier]["fieldCode"]]
    response = request.hugoportal_post_request(
        path = dh.field_urls["create_field"],
        headers = headers,
        data = field_request_dto
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"
    context.data["fields"][fid] = response["data"]

@Then("I updated field_name, field_description, field_type, data_type, group_by, is_edit_only, is_mandatory, field_order, is_paginated_field and dependent_field as ([^']*) of field ([^']*) and verified the updated details")
def step_update_and_verify_field(context, fid, dependent_field):
    request = context.request
    row = context.table.rows[0]
    headers = dh.get_principal_id_and_access_key()
    payload: Dict[str, Any] = {
        "field_name": row["field_name"],
        "field_description": row["field_description"],
        "field_type": row["field_type"],
        "data_type": row["data_type"],
        "group_by": row["group_by"],
        "is_edit_only": parse_bool(row["is_edit_only"]),
        "is_mandatory": parse_bool(row["is_mandatory"]),
        "field_order": int(row["field_order"]),
        "is_paginated_field": parse_bool(row["is_paginated_field"]),
    }
    if dependent_field != "none":
        payload["dependent_field_codes"] = [context.data["fields"][dependent_field]["fieldCode"]]
    field_id = context.data["fields"][fid]["fieldId"]
    update_response = request.hugoportal_put_request(
        path = f'{dh.field_urls["update_field"]}/{field_id}',
        headers = headers,
        data = payload
    )
    if not check_status_portal(update_response, 200):
        assert False, f"The received response is: {update_response}"
    get_response = request.hugoportal_get_request(
        path = dh.field_urls["get_field"] + "/" + field_id,
        headers = headers
    )
    if not check_status_portal(get_response, 200):
        assert False, f"The received response is: {get_response}"

    data = get_response["data"]
    assert data["fieldName"] == row["field_name"]
    assert data["fieldDescription"] == row["field_description"]
    assert data["fieldType"] == row["field_type"]
    assert data["dataType"] == row["data_type"]
    assert data.get("groupBy") == row["group_by"]
    assert data["isEditOnly"] == parse_bool(row["is_edit_only"])
    assert data["isMandatory"] == parse_bool(row["is_mandatory"])
    assert data["fieldOrder"] == int(row["field_order"])
    assert data["isPaginatedField"] == parse_bool(row["is_paginated_field"])
    assert context.data["fields"][dependent_field]["fieldId"] in data["dependentFieldIds"]

@Then("I updated the mapping path of the field ([^']*) and verified whether it was updated or not")
def update_mapping_path_and_verify_step(context, fid):
    request = context.request
    row = context.table.rows[0]
    headers = dh.get_principal_id_and_access_key()
    mapping_path : Dict[str, Any] = {
        "mapping_path": {
            "request_mapping_path": row["request_mapping_path"],
            "request_field_position": row["request_field_position"],
            "response_mapping_path": row["response_mapping_path"]
        }
    }
    field_id = context.data['fields'][fid]["fieldId"]
    response = request.hugoportal_put_request(
        path = dh.field_urls["update_field"] + "/" + field_id,
        headers = headers,
        data = mapping_path
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"

    get_response = request.hugoportal_get_request(
        path = dh.field_urls["create_field"] + "/" + field_id,
        headers = headers
    )
    if not check_status_portal(get_response, 200):
        assert False, f"The received response is: {get_response}"
    updated = get_response["data"]
    mp = updated["mappingPath"]
    assert mp["requestMappingPath"] == row["request_mapping_path"]
    assert mp["responseMappingPath"] == row["response_mapping_path"]
    assert mp["requestFieldPosition"] == row["request_field_position"]

@Then("I updated the input config of the field ([^']*) and verified whether it was updated or not")
def update_input_config_and_verify_step(context, fid):
    request = context.request
    row = context.table.rows[0]
    headers = dh.get_principal_id_and_access_key()
    component_type = row["component_type"]
    text_config = {
        "placeholder": row["placeholder"],
        "default_value": row["default_value"]
    }
    rule_type = row["validation_type"]
    rule: Dict[str, Any] = {}
    if rule_type == "STRING_VALIDATION":
        rule["string_rule"] = {
            "min_length": int(row["min_length"]),
            "max_length": int(row["max_length"])
        }
    validation = {
        "rules": [
            {
                "rule_type": rule_type,
                "string_rule" :{
                    "min_length": int(row["min_length"]),
                    "max_length": int(row["max_length"])
                },
                "error_message": row["error_message"]
            }
        ]
    }
    input_config = {
        "component_type": component_type,
        "is_immutable": row["is_immutable"].lower() == "true",
        "validation": validation,
        "text_config": text_config
    }

    input_config : Dict[str, Any] = {
        "input_config": input_config
    }
    field_id = context.data["fields"][fid]["fieldId"]
    response = request.hugoportal_put_request(
        path = dh.field_urls["update_field"] + "/" + field_id,
        headers = headers,
        data = input_config
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"
    get_response = request.hugoportal_get_request(
        path=dh.field_urls["create_field"] + "/" + field_id,
        headers=headers
    )
    if not check_status_portal(get_response, 200):
        assert False, f"The received response is: {get_response}"
    config = get_response["data"]["inputConfig"]
    assert config["componentType"] == component_type
    assert config["isImmutable"] == (row["is_immutable"].lower() == "true")
    assert config["textConfig"]["placeholder"] == row["placeholder"]
    assert config["textConfig"]["defaultValue"] == row["default_value"]

    rule = config["validation"]["rules"][0]
    assert rule["ruleType"] == rule_type
    assert rule["stringRule"]["minLength"] == int(row["min_length"])
    assert rule["stringRule"]["maxLength"] == int(row["max_length"])
    assert rule["errorMessage"] == row["error_message"]

@Then("I updated the output config of the field ([^']*) and verified whether it was updated or not")
def update_output_config_and_verify_step(context, fid):
    request = context.request
    row = context.table.rows[0]
    headers = dh.get_principal_id_and_access_key()
    component_type = row["component_type"]
    file_config = {
        "display_name": row["display_name"],
        "action_type": row["action_type"],
        "modal_position": row["modal_position"],
        "is_absolute_url": row["is_absolute_url"].lower() == "true"
    }
    output_config = {
        "component_type": component_type,
        "is_clickable": row["is_clickable"].lower() == "true",
        "file_config": file_config
    }

    payload = {
        "output_config": output_config
    }
    field_id = context.data['fields'][fid]["fieldId"]
    response = request.hugoportal_put_request(
        path = dh.field_urls["create_field"] + "/" + field_id,
        headers = headers,
        data = payload
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"
    get_response = request.hugoportal_get_request(
        path = dh.field_urls["create_field"] + "/" + field_id,
        headers = headers
    )
    if not check_status_portal(get_response, 200):
        assert False, f"The received response is: {get_response}"
    config = get_response["data"]["outputConfig"]
    assert config["componentType"] == component_type
    assert config["isClickable"] == (row["is_clickable"].lower() == "true")

    file_config_resp = config["fileConfig"]
    assert file_config_resp["displayName"] == row["display_name"]
    assert file_config_resp["actionType"] == row["action_type"]
    assert file_config_resp["modalPosition"] == row["modal_position"]
    assert file_config_resp["isAbsoluteUrl"] == (row["is_absolute_url"].lower() == "true")

@Then("I updated the effects of field ([^']*) where effects depends upon field ([^']*) and value is ([^']*) and verified whether it was updated or not")
def update_effects_and_verify_step(context, fid, dependent_field, value):
    request = context.request
    headers = dh.get_principal_id_and_access_key()
    field_conditions = []
    condition = {
        "field_code": context.data["fields"][dependent_field]['fieldCode'],
        "value": value
    }
    field_conditions.append(condition)
    payload = {
        "effects": {
            "visibility_condition": {
                "conditions": field_conditions
            }
        }
    }
    field_id = context.data['fields'][fid]["fieldId"]
    response = request.hugoportal_put_request(
        path = dh.field_urls["create_field"] + "/" + field_id,
        headers = headers,
        data = payload
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"

    get_response = request.hugoportal_get_request(
        path = dh.field_urls["create_field"] + "/" + field_id,
        headers = headers
    )
    if not check_status_portal(get_response, 200):
        assert False, f"The received response is: {get_response}"
    actual_conditions = get_response["data"]["effects"]["visibilityCondition"]["conditions"]
    expected_id = context.data["fields"][dependent_field]["fieldId"]
    actual = actual_conditions[0]
    assert actual["fieldId"] == expected_id
    assert str(actual["value"]) == value
