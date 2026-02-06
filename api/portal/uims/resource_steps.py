from typing import Dict, Any
from behave import *
import tests.api.portal.uims.uims_hepler as uh
from tests.util.common_util import check_status_portal
import json

use_step_matcher("re")

@Step(r"I create a resource ([^']*) for portal with resource_code ([^']*), widget ([^']*) and parent_resource as ([^']*)")
def create_resource(context, rid, resource_code, wid, parent_resource_identifier):
    request = context.request
    context.data["resources"] = (
        {} if context.data.get("resources", None) is None else context.data["resources"]
    )
    context.data["resources"][rid] = {}
    resource_request_dto = uh.resource_request_dto
    if resource_code == "random":
        resource_code = "it-resource-" + uh.generate_random_string(8)
    resource_request_dto["resource_code"] = resource_code
    resource_request_dto["widget_code"]   = context.data["widgets"][wid]["widgetCode"]
    if parent_resource_identifier != "none":
        resource_request_dto["parent_resource_code"]  = context.data["resources"][parent_resource_identifier]["resourceCode"]
        resource_request_dto["dependent_on_resources"] = [context.data["resources"][parent_resource_identifier]["resourceCode"]]
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    response = request.hugoportal_post_request(
        path = uh.resource_urls["create_resource"],
        headers = headers,
        data = resource_request_dto
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"
    context.data["resources"][rid] = response["data"]

@Then("I updated display_name, resource_description, parent_resource_code, param_type, dependent_on_resources, resource_order, is_mandatory, is_pinned of resource ([^']*) and parent_resource as ([^']*) and verified the updated details")
def step_update_resource_subset_and_verify(context, rid, parent_resource_identifier):
    request = context.request
    row = context.table.rows[0]
    parent_resource_code = context.data["resources"][parent_resource_identifier]["resourceCode"]
    payload: Dict[str, Any] = {
        "display_name":             row["display_name"],
        "resource_description":     row["resource_description"],
        "parent_resource_code":     parent_resource_code,
        "dependent_on_resources":   [parent_resource_code],
        "resource_order":           int(row["resource_order"]),
        "is_mandatory":             uh.parse_bool(row["is_mandatory"]),
        "is_pinned":                uh.parse_bool(row["is_pinned"]),
    }

    resource_code = context.data["resources"][rid]["resourceCode"]
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    update_response = request.hugoportal_put_request(
        path    = uh.resource_urls["create_resource"] + f"/{resource_code}",
        headers = headers,
        data    = payload
    )
    if not check_status_portal(update_response, 200):
        assert False, f"The received response is: {update_response}"
    get_response = context.request.hugoportal_get_request(
        path = uh.resource_urls["create_resource"] + f"/{resource_code}",
        headers = headers
    )
    if not check_status_portal(get_response, 200):
        assert False, f"The received response is: {get_response}"
    data = get_response["data"]
    assert data["displayName"]          == row["display_name"]
    assert data["resourceDescription"]  == row["resource_description"]
    assert data.get("parentResourceCode") == parent_resource_code
    assert data["dependentOnResources"] == payload["dependent_on_resources"]
    assert data["resourceOrder"]        == int(row["resource_order"])
    assert data["isMandatory"]          == uh.parse_bool(row["is_mandatory"])
    assert data["isPinned"]             == uh.parse_bool(row["is_pinned"])

@Then("I updated input_config of resource ([^']*) and verified the updated details")
def update_input_config(context, rid):
    row = context.table.rows[0]
    validation = {
        "rules": [
            {
                "rule_type": row["rule_type"],
                "string_rule": {
                    "min_length": row["min_length"],
                    "max_length": row["max_length"]
                }
            }
        ]
    }
    payload: Dict[str, Any] = {
        "is_hidden": row["is_hidden"],
        "is_edit_only": row["is_edit_only"],
        "param_type": row["param_type"],
        "input_config": {
            "sub_component_type": row["sub_component_type"],
            "is_immutable": row["is_immutable"],
            "validation": validation,
            "text_config": {
                "placeholder": row["placeholder"],
                "default_value": row["default_value"]
            }
        }
    }
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    resource_code = context.data["resources"][rid]["resourceCode"]
    response = context.request.hugoportal_put_request(
        headers = headers,
        path = uh.resource_urls["create_resource"] + "/" + resource_code,
        data = payload
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"
    get_response = context.request.hugoportal_get_request(
        path    = uh.resource_urls["create_resource"] + f"/{resource_code}",
        headers = headers
    )
    if not check_status_portal(get_response, 200):
        assert False, f"The received response is: {get_response}"
    data = get_response["data"]
    param_cfg = data["resourceConfig"]["paramConfig"]
    input_cfg = param_cfg["inputConfig"]

    assert data["resourceCode"] == resource_code
    assert param_cfg["paramType"] == row["param_type"]
    assert input_cfg["componentType"] == row["sub_component_type"]
    assert input_cfg["isImmutable"]      == uh.parse_bool(row["is_immutable"])

    rules = input_cfg["validation"]["rules"]
    assert len(rules) == 1
    rule = rules[0]
    assert rule["ruleType"] == row["rule_type"]
    assert rule["stringRule"]["minLength"] == int(row["min_length"])
    assert rule["stringRule"]["maxLength"] == int(row["max_length"])

    text_cfg = input_cfg["textConfig"]
    assert text_cfg["placeholder"]   == row["placeholder"]
    assert text_cfg["defaultValue"]  == row["default_value"]

@Then("I updated output_config of resource ([^']*) and verified the updated details")
def update_output_config(context, rid):
    request = context.request
    row = context.table.rows[0]
    payload: Dict[str, Any] = {
        "output_config": {
            "sub_component_type": row["sub_component_type"],
            "file_config": {
                "display_name": row["display_name"],
                "action_type": row["action_type"],
                "modal_position": row["modal_position"],
                "is_absolute_url": row["is_absolute_url"] == "true"
            },
            "is_concatenated": row["is_concatenated"] == "true",
            "concatenated_pattern": row["concatenated_pattern"],
            "paginated_config": {
                "show_in_table": row["show_in_table"] == "true"
            }
        }
    }

    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    resource_code = context.data["resources"][rid]["resourceCode"]

    # Update the resource
    response = request.hugoportal_put_request(
        headers=headers,
        path=uh.resource_urls["create_resource"] + "/" + resource_code,
        data=payload
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"
    get_response = context.request.hugoportal_get_request(
        path=uh.resource_urls["create_resource"] + f"/{resource_code}",
        headers=headers
    )
    if not check_status_portal(get_response, 200):
        assert False, f"The received response is: {get_response}"
    data = get_response["data"]
    param_cfg = data["resourceConfig"]["paramConfig"]
    output_cfg = param_cfg["outputConfig"]

    assert data["resourceCode"] == resource_code
    assert output_cfg["componentType"] == row["sub_component_type"]
    assert output_cfg["isConcatenated"] == uh.parse_bool(row["is_concatenated"])
    assert output_cfg["concatenatedPattern"] == row["concatenated_pattern"]

    file_cfg = output_cfg["fileConfig"]
    assert file_cfg["displayName"] == row["display_name"]
    assert file_cfg["actionType"] == row["action_type"]
    assert file_cfg["modalPosition"] == row["modal_position"]
    assert file_cfg["isAbsoluteUrl"] == uh.parse_bool(row["is_absolute_url"])

    paginated_cfg = output_cfg["paginatedConfig"]
    assert paginated_cfg["showInTable"] == uh.parse_bool(row["show_in_table"])

@Then("I updated effects of resource ([^']*) where effects depends on resource ([^']*) and value is ([^']*) and verified the updated details")
def update_effects(context, rid, dependent_resource_identifier, value):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }

    payload: Dict[str, Any] = {
        "effects": {
            "visibility_condition": {
                "conditions": [
                    {
                        "resource_code": context.data["resources"][dependent_resource_identifier]["resourceCode"],
                        "value": value
                    }
                ]
            }
        }
    }
    resource_code = context.data["resources"][rid]["resourceCode"]
    response = request.hugoportal_put_request(
        headers = headers,
        path = uh.resource_urls["create_resource"] + "/" + resource_code,
        data = payload
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"

    get_response = context.request.hugoportal_get_request(
        path=uh.resource_urls["create_resource"] + f"/{resource_code}",
        headers=headers
    )
    if not check_status_portal(get_response, 200):
        assert False, f"The received response is: {get_response}"
    data = get_response["data"]

    effects = data["effects"]
    assert effects is not None, "effects should be present in response"

    visibility_condition = effects.get("visibilityCondition")
    assert visibility_condition is not None, "visibilityCondition should be present"

    conditions = visibility_condition.get("conditions", [])
    assert len(conditions) > 0, "conditions list should not be empty"

    condition = conditions[0]
    assert condition["resourceCode"] == context.data["resources"][dependent_resource_identifier]["resourceCode"]
    assert condition.get("value") == value

@Then("I updated resource_layout_properties of resource ([^']*) and verified the updated details")
def update_resource_layout_properties(context, rid):
    row = context.table.rows[0]
    resource_code = context.data["resources"][rid]["resourceCode"]
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    key_layout_properties = json.loads(row["key_layout_properties"])
    value_layout_properties = json.loads(row["value_layout_properties"])

    payload: Dict[str, Any] = {
        "resource_layout_properties": {
            "key_layout_properties": key_layout_properties,
            "value_layout_properties": value_layout_properties
        }
    }

    response = context.request.hugoportal_put_request(
        headers=headers,
        path=uh.resource_urls["create_resource"] + "/" + resource_code,
        data=payload
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"
    get_response = context.request.hugoportal_get_request(
        path=uh.resource_urls["create_resource"] + f"/{resource_code}",
        headers=headers
    )
    if not check_status_portal(get_response, 200):
        assert False, f"The received response is: {get_response}"
    data = get_response["data"]

    layout_props = data["resourceLayoutProperties"]
    assert layout_props is not None, "resourceLayoutProperties should be present"

    actual_key_layout_properties = layout_props.get("keyLayoutProperties", {})
    actual_value_layout_properties = layout_props.get("valueLayoutProperties", {})

    assert actual_key_layout_properties == key_layout_properties
    assert actual_value_layout_properties == value_layout_properties
