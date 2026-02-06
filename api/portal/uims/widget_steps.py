import json
import tests.api.portal.uims.uims_hepler as uh
from behave import *
from tests.util.common_util import check_status_portal

use_step_matcher("re")

@Step("I create a widget ([^']*) with redirect_page ([^']*)")
def create_widget(context, wid, redirect_page_identifier):
    request = context.request
    context.data["widgets"] = (
        {} if context.data.get("widgets", None) is None else context.data["widgets"]
    )
    row = context.table.rows[0]
    widget_code = row["widget_code"]
    redirect_page_code = ""
    if widget_code == "random":
        widget_code = "it-widget" + uh.generate_random_string(10)
    if redirect_page_identifier != "none":
        redirect_page_code = context.data["pages"][redirect_page_identifier]["pageCode"]
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    payload = {
        "widget_code": widget_code,
        "widget_name": row["widget_name"],
        "widget_description": row["widget_description"],
        "widget_type": row["widget_type"],
        "widget_sub_type": row["widget_sub_type"],
        "redirect_page_code": redirect_page_code,
        "widget_layout_properties": {
            "no_of_columns": int(row["no_of_columns"])
        },
        "widget_config": json.loads(row["widget_config"])

    }
    response = request.hugoportal_post_request(
        path = uh.admin_widget_urls["create_widget"],
        headers = headers,
        data = payload
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"
    context.data["widgets"][wid] = response["data"]

@then("I update the widget_name, widget_description, widget_type, widget_sub_type, no_of_columns, widget_config of widget ([^']*) and verified updated details")
def update_widget_step(context, wid):
    request = context.request
    row = context.table.rows[0]
    config = json.loads(row["widget_config"])
    widget_code = context.data["widgets"][wid]["widgetCode"]
    payload = {
        "widget_name": row["widget_name"],
        "widget_description": row["widget_description"],
        "widget_type": row["widget_type"],
        "widget_sub_type": row["widget_sub_type"],
        "widget_layout_properties": {
            "no_of_columns": int(row["no_of_columns"])
        },
        "widget_config": config
    }

    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }

    response = request.hugoportal_put_request(
        path = uh.admin_widget_urls["update_widget"] + "/" + widget_code,
        headers = headers,
        data = payload,
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"

    get_response = context.request.hugoportal_get_request(
        path=uh.admin_widget_urls["get_widget"] + "/" + widget_code,
        headers= headers
    )
    if not check_status_portal(get_response, 200):
        assert False, f"The received response is: {get_response}"

    data = get_response["data"]
    assert data["widgetCode"] == widget_code
    assert data["widgetName"] == row["widget_name"]
    assert data["widgetDescription"] == row["widget_description"]
    assert data["widgetType"] == row["widget_type"]
    assert data["widgetSubType"] == row["widget_sub_type"]
    assert data["widgetLayoutProperties"]["noOfColumns"] == int(row["no_of_columns"])
    "Widget config missing expected values.\nExpected at least: {config}\nActual: {data['widgetConfig']}"
    assert all(k in data["widgetConfig"] and data["widgetConfig"][k] == v for k, v in config.items()), \
        f"Expected at least: {config}, Actual: {data['widgetConfig']}"

@Step("I add data_source_id of api ([^']*) to widget ([^']*)")
def add_widget_datasource(context, aid, wid):
    row = context.table.rows[0]
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    widget_code = context.data["widgets"][wid]["widgetCode"]
    data_source_id = context.data["apis"][aid]["dataSourceId"]
    body = {
        "data_source_id": data_source_id,
        "operation_type": row["operation_type"]
    }
    response = request.hugoportal_post_request(
        path = uh.admin_widget_urls["add_data_source"] + "/" + widget_code + "/data-source",
        headers = headers,
        data = body
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"
