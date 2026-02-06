import random
import string

uims_base_url = "/uims/v1"

admin_urls = {
    "onboard_customer": uims_base_url + "/admin/customer-profile/onboard",
    "get_customer": uims_base_url + "/admin/customer-profile"
}

admin_user_urls = {
    "create_operator": uims_base_url + "/admin/user",
    "get_user": uims_base_url + "/admin/user",
    "update_user": uims_base_url + "/admin/user",
    "add_group": uims_base_url + "/admin/user",
    "add_role": uims_base_url + "/admin/user"
}

admin_page_urls = {
    "create_page": uims_base_url + "/admin/page",
    "create_page_widget_config": uims_base_url + "/admin/page/page-widget-config",
    "add_page_widget": uims_base_url + "/admin/page"
}

admin_widget_urls = {
    "create_widget" : uims_base_url + "/admin/widget",
    "get_widget": uims_base_url + "/admin/widget",
    "update_widget" : uims_base_url + "/admin/widget",
    "add_data_source": uims_base_url + "/admin/widget"
}

admin_role_urls = {
    "add_role_page_widget": uims_base_url + "/admin/role",
    "add_role_widget_resource": uims_base_url + "/admin/role",
    "create_role": uims_base_url + "/admin/role",
    "get_role": uims_base_url + "/admin/role",
    "update_role": uims_base_url + "/admin/role",
    "delete_role": uims_base_url + "/admin/role",
}

page_urls = {
    "get_page": uims_base_url + "/page",
}

widget_urls = {
    "get_menu_widget": uims_base_url + "/widget"
}

auth_urls = {
    "login_user" : uims_base_url + "/auth/login",
    "refresh_token": uims_base_url + "/auth/refresh"
}

customer_profile_urls = {
    "list_users": uims_base_url + "/customer-profile/users",
    "list_groups": uims_base_url + "/customer-profile/groups",
    "list_roles": uims_base_url + "/customer-profile/roles"
}

role_urls = {
    "create_role_with_permission": uims_base_url + "/role/permissions"
}

group_urls = {
    "create_group": uims_base_url + "/group",
    "get_group": uims_base_url + "/group",
    "update_group": uims_base_url + "/group"
}

data_urls = {
    "create": uims_base_url + "/data",
    "read": uims_base_url + "/data",
    "update": uims_base_url + "/data",
    "get_component_data": uims_base_url + "/data"
}

permission_urls = {
    "fetch_permission_for_role_creation": uims_base_url + "/permission"
}

resource_urls = {
    "create_resource": uims_base_url + "/resource"
}
resource_request_dto = {
    "resource_code": "",
    "widget_code": "",
    "display_name": "integration test resource",
    "resource_description": "integration test resource",
    "resource_type": "PARAM",
    "parent_resource_code": "",
    "resource_config": {
        "param_config": {
            "field_id": "random",
            "param_type": "INPUT",
            "input_config": {
                "sub_component_type": "TEXT",
                "is_immutable": False,
                "text_config": {
                    "placeholder": "abx",
                    "default_value": "abc"
                }
            }

        }
    },
    "resource_layout_properties": {},
    "effects":{},
    "dependent_on_resources": [],
    "resource_order": 0,
    "is_mandatory": False,
    "is_pinned": True
}

def get_rand_number(n):
    return str(random.randint(pow(10, n - 1), pow(10, n) - 1))

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def parse_bool(val: str) -> bool:
    return val.strip().lower() == "true"
