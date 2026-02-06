from behave import *
import tests.api.portal.uims.uims_hepler as uh
from tests.util.common_util import check_status_portal

use_step_matcher("re")

@Step("I logged in with credentials")
def login(context):
    request = context.request
    row = context.table[0]
    login_payload = {
        "user_name": row["username"],
        "password": row["password"]
    }
    response = request.hugoportal_post_request(
        path = uh.auth_urls["login_user"],
        data = login_payload
    )
    if not check_status_portal(response, 200):
        assert False, f"Login failed: {response}"
    context.data["logged_in_user_id"] = response["data"]["user"]["userId"]
    context.data["customer_profile_id"] = response["data"]["user"]["customerProfileId"]
    context.data["logged_in_user_role_id"] = response["data"]["user"]["role"]["roleId"]
    context.data["token"] = response["data"]["AuthenticationResponse"]["idToken"]
    context.data["access_token"] = response["data"]["AuthenticationResponse"]["accessToken"]
    context.data["refresh_token"] = response["data"]["AuthenticationResponse"]["refreshToken"]

@Step("I refresh access token for my account and I verify status code as ([^']*)")
def refresh_access_token(context, expected_status):
    request = context.request
    body = {
        "id_token": context.data["token"],
        "refresh_token": context.data["refresh_token"],
        "access_token": context.data["access_token"]
    }
    response = request.hugoportal_post_request(
        path = uh.auth_urls["refresh_token"],
        data = body
    )
    if not check_status_portal(response, expected_status):
        assert False, f"Received response: {response}"

