from behave import *
import tests.api.portal.uims.uims_hepler as uh
from tests.util.common_util import check_status_portal

use_step_matcher("re")

@Step("I list all the the roles using dropdown resource ([^']*) of page ([^']*) and widget ([^']*) and I verify expected status code as ([^']*)")
def fetch_dropdown_data(context, resource_code, page_code, widget_code, expected_status_code):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    response = request.hugoportal_get_request(
        path= uh.data_urls["get_component_data"] + "/dropdown" + f"/{page_code}/{resource_code}/component-data" ,
        headers = headers
    )
    if not check_status_portal(response, expected_status_code):
        assert False, f"The received response is: {response}"

@Step("I fetch pre-signed-url using file upload config resource ([^']*) of page ([^']*) and widget ([^']*) and I verify expected status code as ([^']*)")
def fetch_dropdown_data(context, resource_code, page_code, widget_code, expected_status_code):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    response = request.hugoportal_get_request(
        path= uh.data_urls["get_component_data"] + "/file" + f"/{page_code}/{resource_code}/component-data" ,
        headers = headers
    )
    if not check_status_portal(response, expected_status_code):
        assert False, f"The received response is: {response}"

@Step("I list all the conditions using condition config resource ([^']*) of page ([^']*) and widget ([^']*) and I verify expected status code as ([^']*)")
def fetch_dropdown_data(context, resource_code, page_code, widget_code, expected_status_code):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    response = request.hugoportal_get_request(
        path= uh.data_urls["get_component_data"] + "/condition" + f"/{page_code}/{resource_code}/component-data" ,
        headers = headers
    )
    if not check_status_portal(response, expected_status_code):
        assert False, f"The received response is: {response}"
