import uuid
from copy import deepcopy

los_base_url = "/los/v1"

admin_urls = {
    "onboard_customer_profile" : los_base_url + "/admin/customer-profile",
}

customer_profile_urls = {
    "get_customer_profile_journeys" : los_base_url + "/customer-profile/los-journeys",
}

end_customer_profile_urls = {
    "onboard" : los_base_url + '/end-customer-profile'
}

los_param_urls = {
    "create" : los_base_url + '/los-param',
}

los_journey_urls = {
    "create" : los_base_url + '/los-journey',
    "get_journey_params" : los_base_url + '/los-journey/$journey_code$/journey-params',
    "get_journey_applications" : los_base_url + '/los-journey/$journey_code$/applications',
}

los_application_urls = {
    "create" : los_base_url + '/application',
    "evaluate": los_base_url + "/application/$application_id$/evaluate",

}

LOS_PARAM_CONDITION_CONFIG = {
    "valid_region_case": {
        "left_operand": "REGION",
        "supported_operators": ["EQUALS"],
        "right_operand_config": {
            "data_type": "STRING",
            "possible_values": ["Urban", "Rural", "Metro"]
        }
    },
    "valid_age_case": {
        "left_operand" : "AGE",
        "supported_operators": ["LESS_THAN", "GREATER_THAN"],
        "right_operand_config": {
            "data_type": "INTEGER"
        }
    }
}

LOS_RULE_GROUPS = {
        'valid_case': {
            "rules": [{
                "when": {
                    "condition_group": {
                        "logical_operator": "OR",
                        "conditions": [
                            {
                                "condition_key": "KEY_001",
                                "value": "Urban",
                                "operator": "EQUALS"
                            },
                            {
                                "condition_key": "KEY_001",
                                "value": "Metro",
                                "operator": "EQUALS"
                            }
                        ],
                        "condition_groups": []
                    }
                },
                "then": {
                    "unary_return": {
                        "number_value": 20
                    }
                },
                "order": 1
            }],
            "execute_match": "EXECUTE_FIRST_MATCH",
            "aggregate_function": "NOOP"
        },
        'unsupported_operator_used': {
            "rules": [{
                "when": {
                    "condition_group": {
                        "logical_operator": "AND",
                        "conditions": [
                            {
                                "condition_key": "KEY_001",
                                "value": "Rural",
                                "operator": "GREATER_THAN"
                            }
                        ],
                        "condition_groups": []
                    }
                },
                "then": {
                    "unary_return": {
                        "number_value": 20
                    }
                },
                "order": 1
            }],
            "execute_match": "EXECUTE_FIRST_MATCH",
            "aggregate_function": "NOOP"
        },
    "invalid_type_used" : {
        "rules": [{
            "when": {
                "condition_group": {
                    "logical_operator": "AND",
                    "conditions": [
                        {
                            "condition_key": "KEY_001",
                            "value": 20,
                            "operator": "EQUALS"
                        }
                    ],
                    "condition_groups": []
                }
            },
            "then": {
                "unary_return": {
                    "number_value": 20
                }
            },
            "order": 1
        }],
        "execute_match": "EXECUTE_FIRST_MATCH",
        "aggregate_function": "NOOP"
    }
}

def get_journey_rule_config(rule_case, param_code):
    if rule_case == 'empty_journey_rule':
        return []
    rule_case_to_pass = rule_case

    if (rule_case != 'valid_case' and rule_case != 'unsupported_operator_used'
            and rule_case != 'invalid_type_used'):
        rule_case_to_pass = 'valid_case'

    journey_rules = [
        {
            "param_code": param_code,
            "weightage": 100,
            "rule_group": update_condition_key_in_rule_group(
                LOS_RULE_GROUPS[rule_case_to_pass],
                param_code
            )
        }
    ]
    if rule_case == 'duplicate_param_code':
      journey_rules.append({
            "param_code": param_code,
            "weightage": 100,
            "rule_group": update_condition_key_in_rule_group(
                LOS_RULE_GROUPS[rule_case_to_pass],
                param_code
            )
        })

    if rule_case == "total_weightage_under_100" :
        journey_rules[0]["weightage"] = 60

    return journey_rules

# function to update param_code correctly
def update_condition_key_in_rule_group(rule_group, param_code):
    updated_group = deepcopy(rule_group)
    if "rules" in updated_group:
        for rule in updated_group["rules"]:
            if "when" in rule and "condition_group" in rule["when"]:
                condition_group = rule["when"]["condition_group"]
                if "conditions" in condition_group:
                    for condition in condition_group["conditions"]:
                        if "condition_key" in condition:
                            condition["condition_key"] = param_code

    return updated_group

# for los param creation
def get_condition_config(condition_config_type, param_code):
    config = LOS_PARAM_CONDITION_CONFIG.get(condition_config_type)
    config_copy = config.copy()
    config_copy["param_code"] = param_code
    config_copy["left_operand"] = param_code
    return config_copy

def get_application_input_data(case_name, context=None, param_identifier=None):
    if case_name == "UNKNOWN_PARAM_IN_INPUT_DATA":
        return {
            str(uuid.uuid4()): "Urban"
        }
    elif case_name == "UNDEFINED_JOURNEY_PARAM_IN_INPUT_DATA":
        param_code = context.param_map['PARAM_2']
        return {
            param_code: "Urban"
        }
    elif case_name == "VALID_CASE" or case_name == "UNKNOWN_CUSTOMER" or case_name == "WRONG_INPUT_VALUE":
        param_code = "REGION"
        if context and param_identifier in context.param_map:
            param_code = context.param_map[param_identifier]   # e.g. PARAM_1
        if case_name == "WRONG_INPUT_VALUE":
            return {
                param_code: 1249
            }
        return {
                param_code: "Urban"
        }
    elif case_name == "EMPTY_INPUT_DATA":
        return {}
    return None


def get_headers(customer_profile_id):
    headers = {
        "x-customer-profile-id": customer_profile_id,
    }
    return headers
