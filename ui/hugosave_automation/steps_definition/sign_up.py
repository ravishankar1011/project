from behave import use_step_matcher, given, then
use_step_matcher("re")
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from appium.webdriver.common.appiumby import AppiumBy
from tests.ui.hugosave_automation.pages.util import Util
from tests.ui.hugosave_automation.pages.home_screen_locators import HomeScreen
from tests.ui.hugosave_automation.pages.signuplocators import SignUpLocators
from tests.ui.hugosave_automation.features.steps.data_class_parser import DataClassParser
from tests.ui.hugosave_automation.steps_definition.data_class import UserDetails, Passcode

@given('I verify that I have entered the signup screen')
def step_verify_signup_screen(context):
    welcome_element_response = WebDriverWait(context.driver, 40).until(EC.presence_of_element_located(SignUpLocators.WELCOME_HUGO_HERO_TEXT))
    assert welcome_element_response.text == 'Welcome #Hugohero', "unexpected welcome text"


@given("I enter the mobile number ([^']*)")
def step_enter_mobile_number(context, phone_number: str):
    if not hasattr(context, 'numbers'):
        context.numbers = {}
    if re.search(r'[A-Za-z]', phone_number):
        generated_number = Util.generate_phone_number()
        context.numbers[phone_number] = generated_number
        phone_number = generated_number

    mobile_input = context.wait.until(EC.element_to_be_clickable(SignUpLocators.MOBILE_NUMBER_INPUT_FIELD))
    print(phone_number); mobile_input.clear(); mobile_input.send_keys(phone_number)


@then("I verify that the Get OTP button is ([^']*)")
def verify_continue_button_state(context, enabled_or_disabled: str):
    continue_button = context.wait.until(EC.presence_of_element_located(SignUpLocators.get_otp_button))

    if enabled_or_disabled == 'enabled':
        assert continue_button.is_enabled()

    elif enabled_or_disabled == 'disabled':
        assert not continue_button.is_enabled()

    else:
        assert False,"Invalid input, required 'enabled/disabled'"


@then("I tap on the Get OTP button")
def step_tap_get_otp_button(context):
    context.wait.until(EC.element_to_be_clickable(SignUpLocators.get_otp_button)).click()


@then("I verify that I have entered the Create Account screen")
def step_check_create_account_screen(context):
    assert context.wait.until(EC.presence_of_element_located(SignUpLocators.CASUAL_NAME_TEXT)), "CASUAL NAME text not found"


@then("I verify that I have entered the OTP screen")
def step_check_create_account_screen(context):
    assert context.wait.until(EC.presence_of_element_located(SignUpLocators.ENTER_OTP_TEXT)).is_displayed(), "ENTER_OTP text not found"


@then(r"I enter the OTP ([^']*)")
def step_enter_otp(context, otp):
    actions = ActionChains(context.driver)
    for i in otp:
        actions.pause(0.3)
        actions.send_keys(str(i)).perform()


@then(r'I verify that an error message is displayed for an incorrect OTP')
def step_verify_error_message(context):
    error_message = context.wait.until(EC.presence_of_element_located(SignUpLocators.ERROR_MESSAGE_OTP))
    assert error_message.is_displayed, "error message text not found"
    assert error_message.text == 'Incorrect OTP', "unexpected error message text"


@then( "I verify that I have entered the Create Account screen and ensure that all text elements and input fields are present")
def step_check_text_elements(context):
    Util.close_keyboard_if_shown(context.driver)
    wait = WebDriverWait(context.driver, timeout=15)

    casual_name_text = wait.until(EC.presence_of_element_located(SignUpLocators.CASUAL_NAME_TEXT))
    legal_name_text = wait.until(EC.presence_of_element_located(SignUpLocators.LEGAL_NAME_TEXT))
    email_text = wait.until(EC.presence_of_element_located(SignUpLocators.EMAIL_TEXT))
    tick_box_text = wait.until(EC.presence_of_element_located(SignUpLocators.TICK_THIS_BOX_TEXT))
    casual_name_input_field = wait.until(EC.element_to_be_clickable(SignUpLocators.CASUAL_NAME_INPUT_FIELD))
    legal_name_input_field = wait.until(EC.element_to_be_clickable(SignUpLocators.LEGAL_NAME_INPUT_FIELD))
    email_input_field = wait.until(EC.element_to_be_clickable(SignUpLocators.EMAIL_INPUT_FIELD))
    checkbox = wait.until(EC.element_to_be_clickable(SignUpLocators.CHECK_BOX))
    continue_button = wait.until(EC.element_to_be_clickable(SignUpLocators.CONTINUE_BUTTON))

    assert casual_name_text.is_displayed, "casual name text not found"
    assert casual_name_text.text == 'Casual Name (e.g. Jimmy, Jo, Ray)', "unexpected Casual Name (e.g. Jimmy, Jo, Ray) text"
    assert legal_name_text.is_displayed, "legal name text not found"
    assert legal_name_text.text == 'Full Legal Name as per your ID *', "unexpected  text Full Legal Name as per your ID *"
    assert email_text.is_displayed, "email text not found"
    assert email_text.text == "Email Address *", "unexpected Email Address text"
    assert tick_box_text.is_displayed, "tick box text not found"
    assert tick_box_text.text == "Tick this box to confirm you are at least 18 years old and agree to our Terms & Conditions and Privacy Policy", f"unexpected tick box text"
    assert checkbox.is_displayed, "check box not displayed"
    assert continue_button.is_displayed, "continue button not displayed"
    assert casual_name_input_field.is_displayed, "casual name field not displayed"
    assert legal_name_input_field.is_displayed, "legal name field not displayed"
    assert email_input_field.is_displayed, "email field not displayed"


@given(r'I enter a casual name, a legal name, an email, and tick the checkbox')
def step_enter_user_details(context):
    driver, wait = context.driver, context.wait
    test_object_list = DataClassParser.parse_rows(context.table.rows, data_class=UserDetails)

    for object in test_object_list:
        casual_name, legal_name, email, tick_check_box = object.casual_name, object.legal_name, object.email, object.tick_check_box

        if not hasattr(context, 'user_details'):
            context.user_details = {}  # Initialize the dictionary
        if not hasattr(context, 'co_ordinates'):
            pass

        # enter casual_name:
        if casual_name:
            assert (field := wait.until(EC.element_to_be_clickable(SignUpLocators.CASUAL_NAME_INPUT_FIELD))), "casual name field not found";field.clear();field.send_keys(casual_name)
            context.user_details["casual_name"] = casual_name
        else:
            context.user_details["casual_name"] = None

        # enter legal_name:
        if legal_name:
            assert (field := wait.until(EC.element_to_be_clickable(SignUpLocators.LEGAL_NAME_INPUT_FIELD))), "legal name field not found";field.clear();field.send_keys(legal_name)
            context.user_details["legal_name"] = legal_name
        else:
            context.user_details["legal_name"] = None

        # enter email:
        if email:
            Util.close_keyboard_if_shown(driver)
            assert (field := wait.until(EC.element_to_be_clickable(SignUpLocators.EMAIL_INPUT_FIELD))), "legal name field not found";field.clear();field.send_keys(email)
            context.user_details["email"] = email
        else:
            context.user_details["email"] = None

        # tap on the checkbox
        if tick_check_box:
            Util.close_keyboard_if_shown(driver)
            assert (field := wait.until(EC.element_to_be_clickable(SignUpLocators.CHECK_BOX))), "check box not found";field.click()
            context.user_details["tick_check_box"] = tick_check_box

@then(r"I verify the user details and validate error messages for invalid inputs")
def step_validate_user_details(context):
    driver, wait = context.driver, context.wait
    Util.close_keyboard_if_shown(driver)

    casual_name, legal_name, email, tick_check_box = context.user_details["casual_name"], context.user_details["legal_name"], context.user_details["email"], context.user_details["tick_check_box"]

    is_valid_legal = Util.is_valid_casual_or_legal_name(legal_name)
    is_valid_email_ = Util.is_valid_email(email)
    is_valid_casual = Util.is_valid_casual_or_legal_name(casual_name) if casual_name else True

    # check the error message
    if is_valid_legal and is_valid_email_ and is_valid_casual and tick_check_box:
        assert True
    else:
        if not is_valid_casual:
            if casual_name:
                casual_name_error = wait.until(EC.presence_of_element_located(SignUpLocators.CASUAL_NAME_ERROR_TEXT))
                assert casual_name_error, f"Expected casual name error message but not found"

        if not is_valid_legal:
            if legal_name:
                legal_name_error = wait.until(EC.presence_of_element_located(SignUpLocators.LEGAL_NAME_ERROR_TEXT))

                assert legal_name_error, f"Expected legal name error message but not found"

        if not is_valid_email_:
            if email:
                email_error = wait.until(EC.presence_of_element_located(SignUpLocators.EMAIL_ERROR_TEXT))
                assert email_error, f"Expected email error message but not found"


@then(r"I verify the continue button is ([^']*)")
def step_continue_button_status(context, enabled_or_disabled):
    Util.close_keyboard_if_shown(context.driver)

    continue_button_state = context.wait.until(EC.presence_of_element_located(SignUpLocators.CONTINUE_BUTTON))

    if enabled_or_disabled == "enabled":
        assert continue_button_state.is_enabled(), f"Expected continue button state to be enabled but got {continue_button_state}"

    elif enabled_or_disabled == "disabled":
        assert not continue_button_state.is_enabled(), f"Expected continue button state to be disabled but got {continue_button_state}"

    else:
        assert False,"Invalid input, required 'enabled/disabled'"


@then(r"I clear the fields")
def step_clear_fields(context):
    driver, wait = context.driverwait, context.wait

    assert (field := wait.until(EC.element_to_be_clickable(SignUpLocators.CASUAL_NAME_INPUT_FIELD))), "casual name field not found"; field.clear()

    assert (field := wait.until(EC.element_to_be_clickable(SignUpLocators.LEGAL_NAME_INPUT_FIELD))), "legal name field not found"; field.clear()

    Util.close_keyboard_if_shown(driver)
    assert (field := wait.until(EC.element_to_be_clickable(SignUpLocators.EMAIL_INPUT_FIELD))), "email field not found"; field.clear()

    if context.user_details["tick_check_box"]:
        Util.close_keyboard_if_shown(driver)
        assert (field := wait.until(EC.element_to_be_clickable(SignUpLocators.CHECK_BOX))), "check box not found";
        field.click()


@then(r'I click on the continue button')
def step_click_continue_button(context):
    context.wait.until(EC.presence_of_element_located(SignUpLocators.CONTINUE_BUTTON)).click()


@then(r'I check whether I have reached the Set Passcode screen')
def step_check_set_passcode_screen(context):
    set_passcode_text =  WebDriverWait(context.driver, 30).until(EC.presence_of_element_located(SignUpLocators.SET_PASSCODE_TEXT))
    assert set_passcode_text.is_displayed(), f"Set passcode text not displayed"


@given(r'I enter passcodes in both fields')
def step_enter_passcode(context):
    test_object_list = DataClassParser.parse_rows(context.table.rows, data_class=Passcode)
    for object in test_object_list:
        passcode2 = list(object.passcode_field2)
        passcode_number1 = list(object.passcode_field1)
        actions = ActionChains(context.driver)
        for i in passcode_number1:  # Python range is exclusive of the end value.
            actions.send_keys(str(i)).perform()
        for i in passcode2:  # Python range is exclusive of the end value.
            actions.send_keys(str(i)).perform()


@then(r"I verify that the create account button is ([^']*)")
def step_verify_button(context,enabled_or_disabled):
    create_account_button = context.wait.until(EC.presence_of_element_located(SignUpLocators.CREATE_ACCOUNT_BUTTON))
    if enabled_or_disabled=="enabled":
        assert create_account_button.is_enabled(), f' create account button should be enabled but the button status is create_account_button["enabled"]:{create_account_button.is_enabled()}'
    elif enabled_or_disabled == "disabled":
        assert not create_account_button.is_enabled(), f' create account button should be disabled but the button status is create_account_button["enabled"]: {create_account_button.is_enabled()}'
    else:
        assert False, "Invalid input, required 'enabled/disabled'"


@then(r'I check for the error message')
def step_check_error_message(context):
    set_passcode_text = context.wait.until(EC.presence_of_element_located(SignUpLocators.SET_PASSCODE_TEXT))
    assert set_passcode_text.is_displayed(), f'Not directed to the passcode screen after clicking create account button'

    error_message = context.wait.until(EC.presence_of_element_located(SignUpLocators.ERROR_MESSAGE_PASSCODE))
    assert error_message.is_displayed(), f"error message didn't appear"
    assert error_message.text == "The passcodes don't match", f'incorrect error message: {error_message.text}'


@then('I click on the Create account button')
def step_click_create_account_button(context):
    context.wait.until(EC.presence_of_element_located(SignUpLocators.CREATE_ACCOUNT_BUTTON)).click()


@then(r'I clear the passcode fields')
def clear_passcode_fields(context):
    last_button_field2 = 'new UiSelector().className("android.view.ViewGroup").instance(33)'
    last_button_field1 = 'new UiSelector().className("android.view.ViewGroup").instance(26)'
    context.wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, last_button_field2))).click()
    for i in range(6):
        context.driver.press_keycode(67)
    context.wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, last_button_field1))).click()
    for i in range(6):
        context.driver.press_keycode(67)


@then(r'I verify if I am directed to the Allow Notifications screen')
def step_directed_to_notification_screen(context):
    notification_text = WebDriverWait(context.driver, 30).until(
        EC.presence_of_element_located(SignUpLocators.NOTIFICATION_TEXT))
    assert notification_text.is_displayed(), f'Got exception (not directed to the Allow Notifications screen)'


@then(r'I verify if I am directed to the Allow Notifications screen and check the text elements and button')
def step_verify_notification_screen(context):
    wait = WebDriverWait(context.driver, 150)

    notification_text = wait.until(EC.presence_of_element_located(SignUpLocators.NOTIFICATION_TEXT))
    assert notification_text.is_displayed(), f'Got exception (not directed to the Allow Notifications screen)'

    allow_notifications_button = wait.until(EC.presence_of_element_located(SignUpLocators.ALLOW_NOTIFICATIONS_BUTTON))
    assert allow_notifications_button.is_displayed(), f'Allow notifications button not displayed'

    not_now_button = wait.until(EC.presence_of_element_located(SignUpLocators.NOT_NOW_BUTTON))
    assert not_now_button.is_displayed(), f'Allow notifications button not displayed'


@given(r"I tap on the ([^']*) notification button")
def step_allow_notifications(context, allow_or_cancel: str):
    wait = WebDriverWait(context.driver, 15)

    if allow_or_cancel== "allow":
        allow_notifications_button = wait.until( EC.presence_of_element_located(SignUpLocators.ALLOW_NOTIFICATIONS_BUTTON))
        assert allow_notifications_button.is_enabled(), f'Allow notifications button not displayed'; allow_notifications_button.click()

    elif allow_or_cancel== "not_now":
        not_now_button = wait.until(EC.presence_of_element_located(SignUpLocators.NOT_NOW_BUTTON))
        assert not_now_button.is_enabled(), f'Allow notifications button not displayed'; not_now_button.click()

        not_now_pop_up = wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("RNE__Overlay__Container")')))
        assert not_now_pop_up.is_displayed(), f'Cancel Pop-up not displayed after tapping on the cancel button'
        Util.perform_touch_action(context.driver, 344, 1600)


@then("I verify that i have reached the Home screen")
def step_verify_home_screen(context):
    wait = WebDriverWait(context.driver, 60)

    show_me_around = wait.until(EC.presence_of_element_located(HomeScreen.SHOW_ME_AROUND))
    assert show_me_around.is_displayed(), f'Got exception (not directed to the home screen)'
