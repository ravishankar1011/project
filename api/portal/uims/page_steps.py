import json
from behave import *
from typing import Dict, Any
from tests.api.portal.uims.uims_dataclass import CreatePageWidgetConfig
from tests.util.common_util import check_status_portal
import tests.api.portal.uims.uims_hepler as uh
from tests.ui.hugosave_automation.features.steps.data_class_parser import DataClassParser

use_step_matcher("re")

@when("I create a page ([^']*)")
def create_page_step(context, pid):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    row = context.table.rows[0]
    context.data["pages"] = (
        {} if context.data.get("pages", None) is None else context.data["pages"]
    )
    context.data["pages"][pid] = {}
    page_code = row["page_code"]
    if page_code == "random":
        page_code = "it-page-" + uh.generate_random_string(10)
    payload: Dict[str, Any] = {
        "page_code": page_code,
        "page_name": row["page_name"],
        "page_description": row["page_description"],
        "show_in_menu": row["show_in_menu"] == "true",
        "metadata": json.loads(row["metadata"])
    }
    if row.get("menu_category"):
        payload["menu_category"] = row["menu_category"]
    if row.get("menu_order"):
        payload["menu_order"] = int(row["menu_order"])
    context.data["page_code"] = row["page_code"]
    response = request.hugoportal_post_request(
        path = uh.admin_page_urls["create_page"],
        headers = headers,
        data = payload
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"
    context.data["pages"][pid] = response["data"]

@Step("I create a page_widget_config ([^']*)")
def create_page_widget_config(context, pwcid):
    request = context.request
    context.data["page_widget_configs"] = (
        {} if context.data.get("page_widget_configs", None) is None else context.data["page_widget_configs"]
    )
    context.data["page_widget_configs"][pwcid] = {}
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    page_config_dto_list = DataClassParser.parse_rows(
        context.table.rows, data_class = CreatePageWidgetConfig
    )
    page_config_dto = page_config_dto_list[0]
    response  = request.hugoportal_post_request(
        headers = headers,
        data = page_config_dto.get_dict(),
        path = uh.admin_page_urls["create_page_widget_config"]
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"
    context.data["page_widget_configs"][pwcid] = response["data"]

@Step("I added widget ([^']*) to page ([^']*) with page_widget_config ([^']*)")
def add_page_widget(context, wid, pid, pwcid):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    payload = {
        "widgets": [
            {
                "widget_code": context.data["widgets"][wid]["widgetCode"],
                "page_widget_config_code": context.data["page_widget_configs"][pwcid]["pageWidgetConfigCode"]
            }
        ]
    }
    page_code = context.data["pages"][pid]["pageCode"]
    response = request.hugoportal_post_request(
        path = uh.admin_page_urls["add_page_widget"] + "/" + page_code + "/widget",
        headers = headers,
        data = payload
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"

@then("I update the page and verified updated details")
def update_page_step(context):
    request = context.request
    row = context.table.rows[0]
    page_code = context.data["page_code"]
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }

    payload: Dict[str, Any] = {
        "page_code": page_code,
        "page_name": row["page_name"],
        "page_description": row["page_description"],
        "show_in_menu": row["show_in_menu"] == "true",
        "menu_category": row["menu_category"],
        "menu_order": row["menu_order"],
        "metadata": json.loads(row["metadata"])
    }
    response = request.hugoportal_post_request(
        headers=headers,
        path=uh.admin_page_urls["create_page"],
        data=payload
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"

    get_response = context.request.hugoportal_get_request(
        path=uh.page_urls["get_page"] + f"/{page_code}" + "/structure",
        headers=headers
    )
    if not check_status_portal(get_response, 200):
        assert False, f"The received response is: {get_response}"
    data = get_response["data"]
    assert data["pageCode"] == page_code
    assert data["pageName"] == row["page_name"]
    assert data["pageDescription"] == row["page_description"]

@Then("I try to fetch page structure of page ([^']*) with expected status code ([^']*)")
def get_page_structure(context, pid, expected_status_code):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    page_code = context.data["pages"][pid]["pageCode"]
    response = request.hugoportal_get_request(
        headers = headers,
        path = uh.page_urls["get_page"] + "/" + page_code + "/structure"
    )
    if not check_status_portal(response, expected_status_code):
        assert False, f"The received response is: {response}"
    if expected_status_code == "200":
        print("user is able to fetch page structure of page: " + page_code)
    else:
        print("user is unable to fetch page structure of page: " + page_code)
