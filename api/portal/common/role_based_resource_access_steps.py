from behave import *
import tests.api.portal.uims.uims_hepler as uh
from tests.util.common_util import check_status_portal

use_step_matcher("re")

@Step("I fetched the page structure of page ([^']*) and verified that resource ([^']*) is present, while ([^']*) is not")
def fetch_page_and_verify(context, pid, rid1, rid2):
    request = context.request
    page_code = context.data["pages"][pid]["pageCode"]

    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    get_response = request.hugoportal_get_request(
        path=uh.page_urls["get_page"] + f"/{page_code}" + "/structure",
        headers=headers
    )
    check_status_portal(get_response, 200)
    resource_code_one = context.data["resources"][rid1]["resourceCode"]
    resource_code_two = context.data["resources"][rid2]["resourceCode"]

    page = get_response["data"]
    pageWidgetConfig = page["pageWidgetConfigs"][0]
    widget = pageWidgetConfig["widgets"][0]
    resources = widget["sections"][0]["children"]
    resource_codes = [r["resourceCode"] for r in resources]
    assert resource_code_one in resource_codes, f"{resource_code_one} not found in widget resources"
    assert resource_code_two not in resource_codes, f"{resource_code_two} should not be present in widget resources"
