from behave import *
import tests.api.portal.uims.uims_hepler as uh
import os
import requests
from tests.util.common_util import check_status_portal

use_step_matcher("re")

@Step("I list all the users using widget ([^']*) for which we can upload file")
def list_users_for_file_upload(context, widget_code):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    response = request.hugoportal_get_request(
        path = uh.data_urls["read"] + f"/{widget_code}/read"
             + "?user-profile-search-filter-name=NAME"
             + "&user-profile-search-filter-value=a"
             + "&user-profile-search-profile-status=PROFILE_ACTIVE"
             + "&user-profile-search-limit=10",
        headers = headers
    )
    if not check_status_portal(response, 200):
        assert False, f"The received response is: {response}"
    if len(response["data"]["paginatedData"]["rows"]) == 0:
        raise Exception("No users found for the specified filter values.")
    context.data["users"] = response["data"]["paginatedData"]["rows"]

@Step("I try to upload a file using resource ([^']*) of widget ([^']*) and page ([^']*) and I verify expected status code as ([^']*)")
def upload_file(context, resource_code, widget_code, page_code, expected_status_code):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    response = request.hugoportal_get_request(
        path = uh.data_urls["get_component_data"] + "/file" + f"/{page_code}/{resource_code}/component-data",
        headers=headers
    )
    if not check_status_portal(response, expected_status_code):
        assert False, f"The received response is: {response}"

    pre_signed_url = response["data"]["url"]
    file_key = response["data"]["fileKey"]
    file_path = os.path.expanduser("~/Downloads/sample_file_for_draft_integration_test.pdf")
    try:
        headers = {"Content-Type": "application/pdf"}
        with open(file_path, 'rb') as f:
            upload_resp = requests.put(pre_signed_url, data=f, headers=headers)
    except FileNotFoundError:
        print(f"Error: The file '{os.path.abspath(file_path)}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    assert upload_resp.status_code == 200, f"Upload failed: {upload_resp.status_code}, {upload_resp.text}"
    context.data["file_key"] = file_key
    context.data["uploaded_file_url"] = pre_signed_url


@Step("I try to process the file that uses resource ([^']*) of widget ([^']*) and page ([^']*)")
def process_file(context, resource_code, widget_code, page_code):
    request = context.request
    headers = {
        "x-logged-in-user-id": context.data["logged_in_user_id"],
        "Authorization": "Bearer " + context.data["token"]
    }
    user_profile_id = context.data["users"][0]["user-profile-search-user-profile-id"]
    file_key = context.data["file_key"]
    body = {
        "input_data": {
            "upload-user-documents-document-type": "ABC",
            "upload-user-documents-document-upload": file_key,
            "upload-user-documents-user-profile-id": user_profile_id
        }
    }
    response = request.hugoportal_post_request(
        path = uh.data_urls["create"] + f"/{page_code}/{widget_code}/create",
        headers = headers,
        data = body
    )
    context.data["draft_id"] = response["data"]["draftId"]
