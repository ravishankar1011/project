from behave import *
from retry import retry

use_step_matcher("re")
import tests.api.distribute.app_helper as ah
from tests.util.common_util import check_status_distribute


@Step("I authorise the ([^']*) for the user ([^']*) and expect the device authorisation status of ([^']*)")
def device_authorisation_status(context, device, uid, expected_status):
    request = context.request
    if device != context.data["users"][uid]["current_device"]:
        context.data["users"][uid]["user_devices"][device] = ah.generate_device_details()
    headers = ah.get_device_authorisation_header(context, uid)
    headers["x-authentication-token"] =  context.data["users"][uid]["user_devices"][device]["authentication_token"]
    initiate_device_authorisation_response = request.hugosave_post_request(
        path= ah.device_authorisation_urls["initiate"],
        headers=headers
    )
    ah.store_journey_id(context, initiate_device_authorisation_response)
    if check_status_distribute(initiate_device_authorisation_response,200):
        assert initiate_device_authorisation_response["data"]["deviceAuthorisationStatus"] == expected_status, f"Expected device authorisation status: {expected_status}, but received response: {initiate_device_authorisation_response}"
        context.data["users"][uid]["initiate_device_authorisation_response"] = initiate_device_authorisation_response["data"]


@Step("I initiate the ([^']*) journey within the ([^']*) for user ([^']*) to authorise the device - ([^']*) and expect a status ([^']*)")
def step_impl(context, journey_type, step_code, uid, device, expected_status):
    request = context.request
    headers = ah.get_user_header(context, uid)
    headers["x-authentication-token"] = ah.get_device_authentication_token(context, uid, device)
    journey_id = ah.get_journey_id(context, uid, journey_type, step_code)
    response = request.hugosave_post_request(
        path=ah.device_authorisation_urls["initiate-journey"].replace(
            "{journey-id}", journey_id
        ),
        headers=headers,
        data={},
    )
    context.data["users"][uid]["journey_initiate_response"] = (
        response["data"]
    )
    if check_status_distribute(response, "200"):
        assert response["data"]["journeyStatus"] == expected_status, f"Expected journey status: {expected_status}, but received response: {response}"


@Step("I submit the ([^']*) journey within the ([^']*) for user ([^']*) to authorise the device - ([^']*) and expect a status ([^']*)")
def step_impl(context, journey_type, step_code, uid, device, expected_status):
    request = context.request
    journey_id = ah.get_journey_id(context, uid, journey_type, step_code)
    data_builder = ah.JOURNEY_DATA_BUILDERS.get(journey_type, ah.get_default_data)
    data = data_builder(context, uid)
    headers = ah.get_device_authorisation_header(context, uid)
    headers["x-authentication-token"] = ah.get_device_authentication_token(context, uid, device)
    response = request.hugosave_post_request(
        path = ah.device_authorisation_urls["submit-journey"].replace("{journey-id}", journey_id),
        headers = headers,
        data = data
    )
    if check_status_distribute(response, 200):
        assert response["data"]["journeyStatus"] == expected_status or response["data"]["journeyStatus"] == "JOURNEY_SUCCESSFUL", f"Expected journey status: {expected_status}, but received response: {response}"


@Step("I process the ([^']*) journey within the ([^']*) for user ([^']*) to authorise the device - ([^']*) and expect a status ([^']*)")
def step_impl(context, journey_type, step_code, uid, device, expected_status):
    request = context.request
    journey_id = ah.get_journey_id(context, uid, journey_type, step_code)
    headers = ah.get_user_header(context, uid)
    headers["x-authentication-token"] = ah.get_device_authentication_token(context, uid, device)
    data_builder = ah.JOURNEY_DATA_BUILDERS.get(journey_type, ah.get_default_data)
    data = data_builder(context, uid)

    @retry(AssertionError, tries=30, delay=5, logger=None)
    def retry_user_details():
        response = request.hugosave_post_request(
            path = ah.device_authorisation_urls["process-journey"].replace("{journey-id}", journey_id),
            headers = headers,
            data = data
        )
        if check_status_distribute(response, 200):
            assert response["data"]["journeyStatus"] == expected_status, f"Expected journey status: {expected_status}, but received response: {response}"

    retry_user_details()


@Step("I check the authorisation status of the ([^']*) for the user ([^']*) and expect a device authorisation status of ([^']*)")
def device_authorisation_status(context, device_type, uid, expected_status):
    request = context.request
    @retry(AssertionError, tries=40, delay = 10, logger = None)
    def retry_authorisation_status():
        headers = ah.get_device_authorisation_header(context, uid)
        if device_type != "device_1":
            headers["x-authentication-token"] = context.data["users"][uid]["user_devices"][device_type]["authentication_token"]
        else:
            headers["x-authentication-token"] = context.data['users'][uid]['create_new_user_response']['authenticationToken']
        initiate_device_authorisation_response = request.hugosave_get_request(
            path= ah.device_authorisation_urls["status"],
            headers=headers
        )
        if check_status_distribute(initiate_device_authorisation_response,200):
            assert initiate_device_authorisation_response["data"]["deviceAuthorisationStatus"] == expected_status, f"The expected device authorisation status is: {expected_status}, but received response: {initiate_device_authorisation_response}"
            context.data["users"][uid]["initiate_device_authorisation_response"] = initiate_device_authorisation_response["data"]

    retry_authorisation_status()


@Step("I submit the device authorisation of ([^']*) for user ([^']*) and expect a device authorisation status of ([^']*)")
def submit_device_authorisation(context, device, uid, expected_status):
    request = context.request
    body = {
        "authorisation_session_id": context.data["users"][uid]["initiate_device_authorisation_response"]["authorisationSessionId"],
        "authorisation_journey": "HUGOBANK_BIO_VERISYS",
        "authorisation_details": {}
    }
    headers = ah.get_user_header(context, uid)
    headers["x-authentication-token"] = context.data["users"][uid]["user_devices"][device]["authentication_token"]
    submit_device_authorisation_response = request.hugosave_post_request(
        path = ah.device_authorisation_urls["submit"],
        headers = headers,
        data = body
    )
    if check_status_distribute(submit_device_authorisation_response, 200):
        assert submit_device_authorisation_response["data"]["deviceAuthorisationStatus"] == expected_status, f"The expected device authorisation status is: {expected_status}, but received response: {submit_device_authorisation_response}"


@Step("I check status of the ([^']*) journey within the ([^']*) for the user ([^']*) to authorise the device - ([^']*) and expect a status ([^']*)")
def check_journey_status(context, journey_type, step_code, uid, device, journey_status):
    request = context.request
    journey_id = ah.get_journey_id(context, uid, journey_type, step_code)
    url = ah.progress_onboarding_urls["onboarding-journey-status"].replace("{journey-id}", journey_id)

    @retry(AssertionError, tries=30, delay=15, logger=None)
    def retry_journey_status():
        journey_status_response = request.hugosave_get_request(
            path=url,
            headers=ah.get_device_authorisation_header(context, uid)
        )
        if journey_status_response["data"]["journeyStatus"] == journey_status:
            assert True
        else:
            assert False, f"unable to get status for {journey_type} journey:\t {journey_status_response}"

    retry_journey_status()


@Step("I list all user devices for user ([^']*) and the user should have ([^']*)")
def list_user_devices(context, uid, device_type):
    request = context.request
    device_id_list = []
    if device_type != "no_devices":
        device_list = device_type.split(",")
        for device in device_list:
            device_id_list.append(ah.get_device_id(context, uid, device))
    headers = ah.get_user_header(context, uid)
    customer = context.data["customer"]
    if customer == "HUGOSAVE":
        max_devices = "1"
    elif customer == "HUGOBANK":
        max_devices = "3"
    elif customer == "CDV":
        max_devices = "1"
    headers["x-max-devices"] = max_devices
    params = {'include-all': 'true'}
    list_devices_response = request.hugosave_get_request(
        path = ah.device_management_urls["list"],
        headers = headers,
        params = params
    )
    returned_device_dict = list_devices_response["data"]["activeDevices"]
    returned_device_id_list = [device["deviceInfo"]["deviceId"] for device in returned_device_dict]

    if check_status_distribute(list_devices_response, 200):
        for device_id in device_id_list:
            assert device_id in returned_device_id_list


@Step("I initiate the initial user authorisation to ([^']*) for user ([^']*) and expect cool-off")
def get_initial_authentication_token(context, action, uid):
    request = context.request
    response = request.hugosave_post_request(
        path=ah.get_user_authorisation_token_urls["initial-initiate"],
        headers=ah.get_user_header(context, uid),
        params={"action": action},
    )
    assert check_status_distribute(response, "HSA_9904"), f"Expected cool-off, but received response: {response}"
