import copy
import time

from behave import *
from retry import retry
import tests.api.distribute.app_helper as ah
import json
import requests
from tests.util.common_util import check_status_distribute

use_step_matcher("re")


@Step(
    "I initiate progress onboarding for the user ([^']*) to upgrade the account to ([^']*) and expect an onboarding status of ([^']*)"
)
def initiate_onboarding(context, uid, account_level, expected_status):
    request = context.request
    initiate_onboarding_response = request.hugosave_post_request(
        path=ah.progress_onboarding_urls["initiate-progress-onboarding"],
        headers=ah.get_user_header(context, uid),
        data={"accountLevel": account_level},
    )
    ah.store_journey_id(context, initiate_onboarding_response)
    if check_status_distribute(initiate_onboarding_response, "200"):
        assert initiate_onboarding_response["data"]["onboardingStatus"] ==  expected_status, f"Expected onboarding status: {expected_status}, but received response: {initiate_onboarding_response}"
        context.data["users"][uid]["initiate_onboarding_response"] = (
            initiate_onboarding_response["data"]
        )


@Step("I initiate the progress onboarding journey ([^']*) within the ([^']*) for the user ([^']*) and expect a status of ([^']*)")
def initiate_journey(context, journey_type, step_code, uid, expected_status):
    request = context.request
    journey_id = ah.get_journey_id(context, uid, journey_type, step_code)
    url = ah.progress_onboarding_urls["initiate-onboarding-journey"].replace("{journey-id}", journey_id)
    initiate_journey_response = request.hugosave_post_request(
        path=url, headers=ah.get_user_header(context, uid), data={}
    )
    if check_status_distribute(initiate_journey_response, "200"):
        assert initiate_journey_response["data"]["journeyStatus"] == expected_status, f"Expected journey status: {expected_status}, but received response: {initiate_journey_response}"
        context.data["users"][uid]["initiate_journey_response"] = initiate_journey_response["data"]


@Step("I submit the progress onboarding journey ([^']*) within the ([^']*) for the user ([^']*) and expect the journey status to be ([^']*)")
def submit_journey(context, journey_type, step_code, uid, expected_status):
    request = context.request
    journey_id = ah.get_journey_id(context, uid, journey_type, step_code)
    url = ah.progress_onboarding_urls["submit-onboarding-journey"].replace("{journey-id}", journey_id)

    data_builder = ah.JOURNEY_DATA_BUILDERS.get(journey_type, ah.get_default_data)
    data = data_builder(context, uid)
    response = request.hugosave_post_request(
        path=url,
        headers=ah.get_device_authorisation_header(context, uid),
        data=data
    )
    if check_status_distribute(response, 200):
        assert response["data"]["journeyStatus"] == expected_status, f"Expected journey status: {expected_status}, but received response: {response}"


@Step("I process the progress onboarding journey ([^']*) within the ([^']*) for the user ([^']*) and expect a status code of ([^']*)")
def process_journey(context, journey_type, step_code, uid, expected_status):
    request = context.request
    jid = ah.get_journey_id(context, uid, journey_type, step_code)
    journey_id = jid[0]
    url = ah.progress_onboarding_urls["process-onboarding-journey"].replace("{journey-id}", journey_id)
    context.data["users"][uid]["submit_journey_body"] = copy.deepcopy(
        context.data["users"][uid]["initiate_journey_response"]["data"])
    agreements = context.data["users"][uid]["submit_journey_body"]["agreements"]
    for agreement in agreements:
        agreement["accepted"] = True
    context.data["users"][uid]["submit_journey_body"]["agreements"] = agreements
    context.data["users"][uid]["submit_journey_body"]["videoSeen"] = True
    json_string = json.dumps(context.data["users"][uid]["submit_journey_body"])

    request_body = {
        "data": json_string
    }
    journey_submit_response = request.hugosave_post_request(
        path=url, headers=ah.get_user_header(context, uid), data=request_body
    )
    assert check_status_distribute(journey_submit_response, expected_status), f"unable to submit {journey_type} journey:\t {journey_submit_response}"


@Step("I check status of ([^']*) journey within the ([^']*) for the user ([^']*), the status should be ([^']*)")
def check_journey_status(context, journey_type, step_code, uid, journey_status):
    request = context.request
    journey_id = ah.get_journey_id(context, uid, journey_type, step_code)
    url = ah.progress_onboarding_urls["onboarding-journey-status"].replace("{journey-id}", journey_id)

    @retry(AssertionError, tries=30, delay=15, logger=None)
    def retry_journey_status():
        journey_status_response = request.hugosave_get_request(
            path=url,
            headers=ah.get_device_authorisation_header(context, uid)
        )
        assert journey_status_response["data"]["journeyStatus"] == journey_status, f"unable to get status for {journey_type} journey:\t {journey_status_response}"

    retry_journey_status()


@Step("I upload ([^']*) for ([^']*) for the ([^']*) journey for user ([^ ]+)(?: as the ([^']*))?")
def upload_documents(context, document_type, detail_type, journey_type, uid, proof_type = None):
    customer = context.data["customer"]
    presigned_url = ah.get_presigned_url(
        context,
        uid,
        document_type,
        detail_type,
        proof_type,
        customer
    )

    with open(presigned_url["file_path"], "rb") as file:
        response = requests.put(
            url = presigned_url["upload_url"],
            data = file,
            headers = {"Content-Type": "image/jpg"}
        )
        assert response.status_code == 200


@Step("I upgrade the user ([^']*) account level to L3")
def status_update(context, uid):
    request = context.request
    time.sleep(5)
    user_profile_id = ah.get_user_profile_id(uid, context)
    status_update_response = request.hugosave_put_request(
        path=ah.dev_urls["compliance_update"],
        headers=ah.get_user_header(context, uid),
        params={"level": "L3"},
    )


@Step("I submit the progress onboarding for user ([^']*), the onboarding status should be ([^']*) and the account level should be ([^']*)")
def submit_progress_onboarding(context, uid, expected_onboarding_status, expected_account_level):
    request = context.request
    onboarding_id = ah.get_progress_onboarding_id(context, uid)
    submit_onboarding_response = request.hugosave_post_request(
        path=ah.progress_onboarding_urls["submit-progress-onboarding"],
        headers=ah.get_user_header(context, uid),
        data={"onboarding_id": onboarding_id},
    )
    if check_status_distribute(submit_onboarding_response, "200"):
        if submit_onboarding_response["data"]["onboardingStatus"] == expected_onboarding_status:
            assert submit_onboarding_response["data"]["accountLevel"] == expected_account_level


@Step("I check progress onboarding status for the user ([^']*), the ([^']*) status should be ([^']*)")
def check_progress_onboarding_status(context, uid, parameter, status):
    request = context.request

    @retry(AssertionError, tries=40, delay=20, logger=None)
    def retry_initial_onboarding_status():
        initial_onboarding_status_response = request.hugosave_get_request(
            path=ah.progress_onboarding_urls["progress-onboarding-status"],
            headers=ah.get_user_header(context, uid)
        )
        if check_status_distribute(initial_onboarding_status_response, 200):
            assert initial_onboarding_status_response["data"][parameter] == status, f"Failed to fetch initial onboarding status. \nReceived{initial_onboarding_status_response}"

    retry_initial_onboarding_status()


@Step("I check the user details to confirm if user ([^']*) is ([^']*) and the user profile status should be ([^']*)")
def check_user_details(context, uid, account_level, expected_status):
    request = context.request

    @retry(AssertionError, tries=30, delay=15, logger=None)
    def retry_user_details():
        user_details_response = request.hugosave_get_request(
            path=ah.user_profile_urls["details"],
            headers=ah.get_user_header(context, uid),
            params={"is-full-info": True},
        )
        if check_status_distribute(user_details_response, "200"):
            assert user_details_response["data"]["userState"]["accountLevel"] == account_level and user_details_response["data"]["userStatus"] == expected_status
            context.data["users"][uid]["user_details_response"] = user_details_response["data"]

    retry_user_details()


@Step("I update the onboarding status as ([^']*) if operator action status is ([^']*) for user ([^']*) to upgrade the account to level ([^']*)")
def update_onboard_status_by_operator(context, decision, current_operator_action_status, uid, level):
    request = context.request
    user_profile_id = ah.get_user_profile_id(uid, context)
    @retry(AssertionError, tries = 30, delay = 5, logger = None)
    def retry_user_details():
        initial_onboarding_status_response = request.hugosave_get_request(
            path=ah.progress_onboarding_urls["progress-onboarding-status"],
            headers=ah.get_user_header(context, uid),
            params={"account-level": level}
        )
        if check_status_distribute(initial_onboarding_status_response, "200"):
            if initial_onboarding_status_response["data"]["onboardingStatus"] == "COMPLETED":
                assert True, "Successful"
            elif initial_onboarding_status_response["data"]["operatorActionStatus"] == "OPERATOR_ACTION_REQUIRED":
                onboarding_id = initial_onboarding_status_response["data"]["onboardingId"]

                update_onboarding_operator_status_action_response = request.hugosave_post_request(
                    path=ah.customer_user_urls["operator-action"],
                    headers=ah.get_portal_header(user_profile_id, context),
                    data={
                        "targetId": onboarding_id,
                        "action": "SUBMIT_DECISION",
                        "decision": decision,
                        "scope": "ONBOARDING_LEVEL",
                        "decision_reason": "VERIFIED",
                        "note": "Approved"
                    }
                )

                if not check_status_distribute(update_onboarding_operator_status_action_response, 200):
                    assert (
                        False
                    ), f"Failed to update onboarding operator action. \nReceived{update_onboarding_operator_status_action_response}"

            else:
                raise AssertionError("retrying account details")

        else:
            raise AssertionError("retrying account details")

    retry_user_details()


@Step("Create a binding signature for the user ([^']*) to bind the ([^']*) and the device binding status should be ([^']*)")
def create_binding_signature(context, uid, device_type, expected_status):
    request = context.request
    device_info = ah.get_device_info(context, uid)
    private_key, public_key = ah.generate_keys()
    serialized_public_key = ah.serialize_public_key(public_key)

    # --------------------------Adding changes for test ------------------------------------
    serialized_private_key = ah.serialize_private_key(private_key)
    # # PRINT (for one-time capture only)
    print("PRIVATE KEY (SAVE THIS):", serialized_private_key)
    print("PUBLIC KEY:", serialized_public_key)
    # --------------------------------------------------------------------------------------

    context.data["users"][uid]["public_key"] = public_key
    context.data["users"][uid]["private_key"] = private_key
    headers = {
        "x-device-id" : device_info["x-device-id"],
        "x-device-authorisation-token" : context.data["users"][uid]["initiate_device_authorisation_response"]["deviceAuthorisationToken"],
        "x-org-id": context.data["org_id"]
    }
    device_binding_response = request.hugosave_post_request(
        path=ah.gtw_device_urls["bind"],
        headers=headers,
        data={"public_key": serialized_public_key}
    )
    if check_status_distribute(device_binding_response, 200):
        assert device_binding_response["data"]["deviceBindingStatus"] == expected_status


@Step("I disable cool-off for user ([^']*) and expect a status code of ([^']*)")
def disable_cool_off(context,uid, expected_status_code):
    request = context.request
    reset_cool_off_response = request.hugosave_delete_request(
        path= ah.dev_urls["reset_cool_off"],
        headers=ah.get_device_authorisation_header(context, uid)
    )
    assert check_status_distribute(reset_cool_off_response, expected_status_code), f"Failed to disable device cool-off, the received response is: {reset_cool_off_response}"


@Step("I update ([^']*) journey within the ([^']*) for user ([^']*) as ([^']*)")
def update_status(context, journey, step_code, uid, status):
    request = context.request
    user_profile_id = ah.get_user_profile_id(uid, context)
    jid = ah.get_journey_id(context, uid, journey, step_code)

    if journey == "HUGOSAVE_SINGPASS" or "HUGOBANK_VERISYS":
        path = ah.dev_urls["update_status"]
        data = {"journey": journey, "status": status}
    else:
        path = ah.progress_onboarding_urls["progress-onboarding-update"].replace("{journey-id}", jid)
        data = {"data": json.dumps({"same_as_registered_address": True})}

    @retry(AssertionError, tries=30, delay=5, logger=None)
    def retry_user_details():
        response = request.hugosave_put_request(
            path=path,
            headers=ah.get_device_authorisation_header(context, uid),
            data=data
        )
        assert check_status_distribute(response, "200"), f"Failed to update status. Response: {response.text if response else 'No response'}"

    retry_user_details()


@Step("I process the progress onboarding journey ([^']*) within the ([^']*) for user ([^']*), and expect a status ([^']*)")
def process_journey(context, journey_type, step_code, uid, status):
    request = context.request
    journey_id = ah.get_journey_id(context, uid, journey_type, step_code)
    url = ah.progress_onboarding_urls["process-onboarding-journey"].replace("{journey-id}", journey_id)

    data_builder = ah.JOURNEY_DATA_BUILDERS.get(journey_type, ah.get_default_data)
    data = data_builder(context, uid)

    @retry(AssertionError, tries=30, delay=5, logger=None)
    def retry_user_details():
        response = request.hugosave_post_request(
            path=url,
            headers=ah.get_user_header(context, uid),
            data=data
        )
        if check_status_distribute(response, 200):
            assert response["data"]["journeyStatus"] == status, f"Expected journey status: {status}, but received response: {response}"

    retry_user_details()


@Step("I update the progress onboarding journey ([^']*) within the ([^']*) for user ([^']*), and expect a status code of ([^']*)")
def update_journey(context, journey_type, step_code, uid, expected_status_code):
    request = context.request
    journey_id = ah.get_journey_id(context, uid, journey_type, step_code)
    url = ah.progress_onboarding_urls["progress-onboarding-update"].replace("{journey-id}", journey_id)

    response = request.hugosave_put_request(
        path=url,
        headers=ah.get_user_header(context, uid),
        data={"data": json.dumps(
            {
                "isFamilyPep": True,
            }
        )}
    )
    assert check_status_distribute(response, expected_status_code)


@Step("I update the ([^']*) journey status within the ([^']*) as ([^']*) if operator action status is ([^']*) for user ([^']*)")
def update_journey_status_by_operator(context, journey_type, step_code, decision, current_operator_action_status, uid):
    request = context.request
    user_profile_id = ah.get_user_profile_id(uid, context)
    journey_id = ah.get_journey_id(context, uid, journey_type, step_code)
    @retry(AssertionError, tries = 40, delay = 10, logger = None)
    def retry_user_details():
        initial_onboarding_status_response = request.hugosave_get_request(
            path=ah.progress_onboarding_urls["onboarding-journey-status"].replace("{journey-id}", journey_id),
            headers=ah.get_initial_onboarding_headers(context, uid)
        )
        if check_status_distribute(initial_onboarding_status_response, "200"):
            if initial_onboarding_status_response["data"]["journeyStatus"] == "JOURNEY_SUCCESSFUL":
                assert True, "Successful"
            elif initial_onboarding_status_response["data"]["journeyStatus"] == "JOURNEY_HOLD":

                update_onboarding_operator_status_action_response = request.hugosave_post_request(
                    path=ah.customer_user_urls["operator-action"],
                    headers=ah.get_portal_header(user_profile_id, context),
                    data={
                        "target_id": journey_id,
                        "action": "SUBMIT_DECISION",
                        "scope": "JOURNEY_LEVEL",
                        "decision": decision,
                        "decision_reason": "VERIFIED",
                        "note": "Test"
                    }
                )

                assert check_status_distribute(update_onboarding_operator_status_action_response, "200"), f"Failed to update onboarding operator action. \nReceived{update_onboarding_operator_status_action_response}"

            else:
                raise AssertionError("retrying account details")

    retry_user_details()
