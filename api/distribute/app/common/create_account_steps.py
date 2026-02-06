from behave import *
import tests.api.distribute.app_helper as ah
from tests.api.distribute.app.hugosave_sg.app_dataclass import CreateNewAccountDTO
from tests.util.common_util import check_status_distribute
from hugoutils.utilities.dataclass_util import DataClassParser
from retry import retry

use_step_matcher("re")


@Step("I open a new ([^']*) user account and expect the status code ([^']*)")
def create_new_user(context, customer, expected_status_code):
    global user_info
    request = context.request
    open_new_account_dto_list = DataClassParser.parse_rows(
        context.table.rows, data_class=CreateNewAccountDTO
    )
    for open_new_account_dto in open_new_account_dto_list:
        user_info = open_new_account_dto.get_dict()

    account_type = "PERSONAL"
    if user_info["account_type"] is not None:
        account_type = user_info["account_type"]

    context.data["customer"] = customer
    referral_code = user_info["referral_code"]
    if referral_code:
        if referral_code.startswith("UID"):
            referee_user = context.data["users"][referral_code]["user_details_response"]
            referral_code = referee_user["referralCode"]
        else:
            referral_code = "invalid-code"

    uid = user_info["user_profile_identifier"]
    legal_name = user_info["legal_name"]
    email = context.data["users"][uid]["user_name"]
    name = user_info["name"]
    phone_number = context.data["users"][uid]["user_name"]
    user_name_type = context.data["users"][uid]["mode_of_verification"]

    if customer == "HUGOSAVE":
        security_answers = {}
        non_security_answers = {}
        account_usage_selected_options = []
        if context.data["users"][uid]["mode_of_verification"] == "PHONE_NUMBER":
            email = ah.get_rand_email()

    elif customer == "HUGOBANK":
        security_answers = {"placeOfBirth": "Kabul", "mothersMaidenName": "Ammi"}
        non_security_answers = {"accountUsageSelectedOptions": "OPT_TRANSACTIONS,OPT_CARDS,OPT_SAVINGS" }
        account_usage_selected_options  = ["TRANSACTIONS","CARDS"]
        if context.data["users"][uid]["mode_of_verification"] == "PHONE_NUMBER":
            email = ah.get_rand_email()

    elif customer == "CDV":
        security_answers = {}
        non_security_answers = {}
        account_usage_selected_options = []
        if context.data["users"][uid]["mode_of_verification"] == "EMAIL_ADDRESS":
            phone_number = ah.get_rand_number(7)
        else:
            email = ah.get_rand_email()


    create_user = ah.get_create_user_details(context, uid, user_name_type, legal_name, email, account_type, name, phone_number, referral_code,security_answers, non_security_answers, account_usage_selected_options)

    context.data["users"][user_info["user_profile_identifier"]][
        "user_details"
    ] = create_user

    @retry(AssertionError, tries=30, delay=15, logger=None)
    def retry_new_user():
        create_new_user_response = request.hugosave_post_request(
            path=ah.auth_user_urls["create"],
            headers=ah.get_create_account_header(
                context, user_info["user_profile_identifier"]
            ),
            data=create_user,
        )
        assert check_status_distribute(create_new_user_response, expected_status_code)
        if "userProfileId" in create_new_user_response["data"]:
            context.data["users"][user_info["user_profile_identifier"]][
                "create_new_user_response"
            ] = create_new_user_response["data"]

    retry_new_user()


@Step("I check the current account status")
def check_account_status(context):
    request = context.request
    user_profile_id = context.data["users"]["create_new_user_response"]["userProfileId"]
    account_status_response = request.hugosave_get_request(
        path=ah.user_profile_urls["status"],
        headers=ah.get_user_header(context, user_profile_id),
    )
    assert check_status_distribute(account_status_response, "200"), f"account is not created yet the response received is:{account_status_response}"


@Step("I initiate the initial onboarding of the user ([^']*) and expect a status ([^']*)")
def initiate_initial_onboarding(context, uid, expected_status):
    request = context.request
    initiate_initial_onboarding_response = request.hugosave_post_request(
        path=ah.initial_onboarding_urls["initiate-initial-onboarding"],
        headers=ah.get_initial_onboarding_headers(context, uid),
    )
    ah.store_journey_id(context, initiate_initial_onboarding_response)
    if check_status_distribute(initiate_initial_onboarding_response, "200"):
        assert initiate_initial_onboarding_response["data"]["onboardingStatus"] == expected_status
        context.data["users"][uid]["initiate_initial_onboarding_response"] = (
            initiate_initial_onboarding_response["data"]
        )


@Step("I check the status of initial onboarding for ([^']*) and expect a onboarding status of ([^']*)")
def check_initial_onboarding_status(context, uid, expected_status):
    request = context.request

    @retry(AssertionError, tries=20, delay=5, logger=None)
    def retry_initial_onboarding_status():
        initial_onboarding_status_response = request.hugosave_get_request(
            path=ah.initial_onboarding_urls["initial-onboarding-status"],
            headers=ah.get_initial_onboarding_headers(context, uid),
        )
        if check_status_distribute(initial_onboarding_status_response, "200"):
            if (initial_onboarding_status_response["data"]["onboardingStatus"] == "COMPLETED"):
                assert True, "Successful"

            elif (initial_onboarding_status_response["data"]["operatorActionStatus"] == "OPERATOR_ACTION_REQUIRED"):
                @retry(AssertionError, tries=30, delay=5, logger=None)
                def retry_user_details():
                    response = request.hugosave_put_request(
                        path=ah.dev_urls["update_status"],
                        headers=ah.get_device_authorisation_header(context, uid),
                        data={"update_name_screening": True, "status": "pass"},
                    )
                    if check_status_distribute(response, "200"):
                        assert response["data"]["onboardingStatus"] == expected_status, f"Expected onboarding status: {expected_status}, received response: {response}"

                retry_user_details()


    retry_initial_onboarding_status()


@Step("I submit the initial onboarding for ([^']*), the onboarding status should be ([^']*) and the account level should be ([^']*)")
def submit_initial_onboarding_status(context, uid, expected_onboarding_status, expected_account_level):
    request = context.request
    onboarding_id = ah.get_initial_onboarding_id(uid, context)
    submit_initial_onboarding_response = request.hugosave_post_request(
        path=ah.initial_onboarding_urls["submit-initial-onboarding"],
        headers=ah.get_initial_onboarding_headers(context, uid),
        data={"onboarding_id": onboarding_id},
    )
    if check_status_distribute(submit_initial_onboarding_response, 200):
        if submit_initial_onboarding_response["data"]["onboardingStatus"] == expected_onboarding_status:
            assert submit_initial_onboarding_response["data"]["accountLevel"] == expected_account_level, f"Expected account level: {expected_account_level}, but received response: {submit_initial_onboarding_response}"
            context.data["users"][uid]["submit_initial_onboarding_response"] = (
                submit_initial_onboarding_response["data"]
            )


@Step("I initiate the initial onboarding journey ([^']*) within the ([^']*) for the user ([^']*) and expect a status of ([^']*)")
def initiate_journey(context, journey_type, step_code, uid, expected_status):
    request = context.request
    journey_id = ah.get_journey_id(context, uid, journey_type, step_code)
    url = ah.initial_onboarding_urls["initiate-initial-onboarding-journey"].replace("{journey-id}", journey_id)
    initiate_journey_response = request.hugosave_post_request(
        path=url,
        headers=ah.get_initial_onboarding_headers(context, uid),
        data={}
    )
    if check_status_distribute(initiate_journey_response, "200"):
        assert initiate_journey_response["data"]["journeyStatus"] == expected_status, f"Expected the journey status: {expected_status}, but received response: {initiate_journey_response}"
        context.data["users"][uid]["initiate_journey_response"] = initiate_journey_response["data"]


@Step("I process the initial onboarding journey ([^']*) within the ([^']*) for user ([^']*), and expect a status ([^']*)")
def process_journey(context, journey_type, step_code, uid, expected_status):
    request = context.request
    journey_id = ah.get_journey_id(context, uid, journey_type, step_code)
    url = ah.initial_onboarding_urls["process-initial-onboarding-journey"].replace("{journey-id}", journey_id)

    data_builder = ah.JOURNEY_DATA_BUILDERS.get(journey_type, ah.get_default_data)
    data = data_builder(context, uid)

    @retry(AssertionError, tries=30, delay=5, logger=None)
    def retry_user_details():
        response = request.hugosave_post_request(
            path=url,
            headers=ah.get_initial_onboarding_headers(context, uid),
            data=data
        )
        if check_status_distribute(response, "200"):
            assert response["data"]["journeyStatus"] == expected_status, f"Expected journey status: {expected_status}, but received response: {response}"

    retry_user_details()


@Step("I check status of the initial onboarding journey ([^']*) within the ([^']*) for the user ([^']*), the status should be ([^']*)")
def check_journey_status(context, journey_type, step_code, uid, journey_status):
    request = context.request
    journey_id = ah.get_journey_id(context, uid, journey_type, step_code)
    url = ah.initial_onboarding_urls["initial-onboarding-journey-status"].replace("{journey-id}", journey_id)

    @retry(AssertionError, tries=30, delay=15, logger=None)
    def retry_journey_status():
        journey_status_response = request.hugosave_get_request(
            path=url,
            headers=ah.get_initial_onboarding_headers(context, uid)
        )
        if journey_status_response["data"]["journeyStatus"] == journey_status:
            assert True
        else:
            assert False, f"unable to get status for {journey_type} journey:\t {journey_status_response}"

    retry_journey_status()


@Step("I submit the initial onboarding journey ([^']*) within the ([^']*) for the user ([^']*) and expect the journey status to be ([^']*)")
def submit_journey(context, journey_type, step_code, uid, expected_status):
    request = context.request
    journey_id = ah.get_journey_id(context, uid, journey_type, step_code)
    url = ah.initial_onboarding_urls["submit-initial-onboarding-journey"].replace("{journey-id}", journey_id)

    data_builder = ah.JOURNEY_DATA_BUILDERS.get(journey_type, ah.get_default_data)
    data = data_builder(context, uid)
    response = request.hugosave_post_request(
        path=url,
        headers=ah.get_initial_onboarding_headers(context, uid),
        data=data
    )
    if check_status_distribute(response, "200"):
        assert response["data"]["journeyStatus"] == expected_status or response["data"]["journeyStatus"] == "JOURNEY_SUCCESSFUL", f"Expected journey status: {expected_status}, but received response: {response}"
