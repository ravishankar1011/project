from behave import *
import tests.api.portal.uims.uims_hepler as uh
from typing import Dict, Any
from tests.util.common_util import check_status_portal

use_step_matcher("re")

@Step("I onboard a new customer ([^']*) with the following details")
def onboard_customer_step(context, cpid):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    row = context.table.rows[0]
    context.data["customers"] = (
        {} if context.data.get("customers", None) is None else context.data["customers"]
    )
    context.data["customers"][cpid] = {}
    allowed_domains = [d.strip() for d in row["allowed_domains"].split(",")]
    corporate_email = row["corporate_email"]
    admin_email = row["admin_email"]
    if corporate_email == "random":
        corporate_email = "itcustomer" + uh.generate_random_string(10) + "@gmail.com"
    if admin_email == "random":
        admin_email = "itadmin" + uh.generate_random_string(10) + "@gmail.com"
    payload: Dict[str, Any] = {
        "name": row["name"],
        "corporate_email": corporate_email,
        "phone_number": row["phone_number"],
        "theme": row["theme"],
        "logo_url": row["logo_url"],
        "super_admin_details": {
            "first_name": row["admin_first_name"],
            "last_name": row["admin_last_name"],
            "admin_email": admin_email,
            "admin_phone_number": row["admin_phone_number"]
        },
        "security_config": {
            "session_config": {
                "idle_time_threshold_in_minutes": int(row["idle_time_threshold_in_minutes"]),
                "max_failed_attempts": int(row["max_failed_attempts"]),
                "lock_time_duration": int(row["lock_time_duration"])
            },
            "password_config": {
                "regex": row["regex"],
                "length": int(row["length"]),
                "require_special_characters": row["require_special_characters"] == "true",
                "require_numbers": row["require_numbers"] == "true",
                "require_uppercase": row["require_uppercase"] == "true",
                "allowed_special_characters": row["allowed_special_characters"]
            },
            "allowed_domains": allowed_domains
        }
    }
    response = request.hugoportal_post_request(
        path = uh.admin_urls["onboard_customer"],
        headers = headers,
        data = payload
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"
    context.data["customers"][cpid] = response["data"]

@Step("I update the following details of customer ([^']*) and verified updated details")
def update_customer_step(context, cpid):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    row = context.table.rows[0]
    allowed_domains = [d.strip() for d in row["allowed_domains"].split(",")]
    payload: Dict[str, Any] = {
        "name": row["name"],
        "corporate_email": row["corporate_email"],
        "phone_number": row["phone_number"],
        "security_config": {
            "session_config": {
                "idle_time_threshold_in_minutes": int(row["idle_time_threshold_in_minutes"]),
                "max_failed_attempts": int(row["max_failed_attempts"]),
                "lock_time_duration": int(row["lock_time_duration"])
            },
            "password_config": {
                "regex": row["regex"],
                "length": int(row["length"]),
                "require_special_characters": row["require_special_characters"] == "true",
                "require_numbers": row["require_numbers"] == "true",
                "require_uppercase": row["require_uppercase"] == "true",
                "allowed_special_characters": row["allowed_special_characters"]
            },
            "allowed_domains": allowed_domains
        }
    }
    customer_profile_id = context.data["customers"][cpid]["customerProfileId"]
    response = request.hugoportal_put_request(
        path = uh.admin_urls["get_customer"] + f"/{customer_profile_id}",
        data = payload,
        headers = headers
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"

    get_response = context.request.hugoportal_get_request(
        path=uh.admin_urls["get_customer"] + f"/{customer_profile_id}",
        headers=headers
    )
    if not check_status_portal(get_response, 200):
        assert False, f"The received response is: {get_response}"
    customer = get_response["data"]
    assert customer["name"] == row["name"]
    assert customer["corporateEmail"] == row["corporate_email"]
    assert customer["phoneNumber"] == row["phone_number"]

    security_cfg = customer["securityConfig"]
    session_cfg = security_cfg["sessionConfig"]
    password_cfg = security_cfg["passwordConfig"]

    assert session_cfg["idleTimeThresholdInMinutes"] == int(row["idle_time_threshold_in_minutes"])
    assert session_cfg["maxFailedAttempts"] == int(row["max_failed_attempts"])
    assert session_cfg["lockTimeDuration"] == int(row["lock_time_duration"])

    assert password_cfg["regex"] == row["regex"]
    assert password_cfg["length"] == int(row["length"])
    assert password_cfg["requireSpecialCharacters"] == (row["require_special_characters"] == "true")
    assert password_cfg["requireNumbers"] == (row["require_numbers"] == "true")
    assert password_cfg["requireUppercase"] == (row["require_uppercase"] == "true")
    assert password_cfg["allowedSpecialCharacters"] == row["allowed_special_characters"]

    assert sorted(security_cfg["allowedDomains"]) == sorted(allowed_domains)

@When("I fetch all the roles and set a role as ([^']*)")
def list_all_roles(context, rid):
    """
    Fetches a list of all roles, and stores the details of the first role
    found in the context for later use.
    """
    request = context.request
    context.data["roles"] = (
        {} if context.data.get("roles", None) is None else context.data["roles"]
    )
    context.data["roles"][rid] = {}
    headers = {
        "x-customer-profile-id": context.data["customer_profile_id"],
        "x-logged-in-user-id": context.data["logged_in_user_id"]
    }
    get_response = request.hugoportal_get_request(
        path=uh.customer_profile_urls["list_roles"],
        headers=headers,

    )
    if not check_status_portal(get_response, 200):
        assert False, f"The received response is: {get_response}"
    roles_list = get_response.get("data", {}).get("role", [])
    role = {}
    if roles_list:
        role = roles_list[0]
    selected_role = role
    context.data["roles"][rid] = role
    print(
        f"Successfully fetched a list of roles and stored '{selected_role.get('roleName')}' "
        f"with ID '{selected_role.get('roleId')}' as '{rid}' in the context."
    )
