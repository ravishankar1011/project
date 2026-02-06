import time
from appium.webdriver.common.appiumby import AppiumBy
from behave import *
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.ui.hugobank_automation.pages.signuplocators import SignUpLocators
from tests.ui.hugobank_automation.pages.utils import Testing
from behave import use_step_matcher
import os

use_step_matcher("re")

@step("I sign up with bypass number")
def step_onboarding(context):
    wait, driver =  context.wait, context.driver
    for prefix, name, place_of_birth, maiden_name in context.table:
        mobile_number = Testing.generate_random_number(prefix)
        context.valid_mobile_number = mobile_number
        mobile_input = wait.until(EC.element_to_be_clickable(SignUpLocators.MOBILE_INPUT))
        mobile_input.clear()
        mobile_input.send_keys(mobile_number)

        wait.until(EC.element_to_be_clickable(SignUpLocators.GET_OTP_BUTTON)).click()

        wait.until(EC.presence_of_element_located(SignUpLocators.ENTER_OTP_TEXT))

        actions = ActionChains(driver)
        for digit in '123456':
            actions.send_keys(digit)
        actions.perform()

        wait.until(EC.presence_of_element_located(SignUpLocators.CASUAL_NAME_FIELD)).send_keys(name)

        checkbox = wait.until(EC.element_to_be_clickable(SignUpLocators.TERMS_CHECKBOX))
        if not checkbox.is_selected():
            checkbox.click()
        wait.until(EC.element_to_be_clickable(SignUpLocators.CONTINUE_BUTTON)).click()

        for locator in SignUpLocators.USAGE_OPTIONS.values():
            wait.until(EC.element_to_be_clickable(locator)).click()

        wait.until(EC.element_to_be_clickable(SignUpLocators.CONTINUE_BUTTON)).click()

        actions = ActionChains(driver)
        wait.until(EC.presence_of_element_located(SignUpLocators.SET_PASSWORD))

        for digit in '123456':
            actions.send_keys(digit)
        actions.pause(1)
        for digit in '123456':
            actions.send_keys(digit)
        actions.perform()

        wait.until(EC.element_to_be_clickable(SignUpLocators.CONTINUE_BUTTON)).click()
        wait.until(EC.element_to_be_clickable(SignUpLocators.SELECT_COUNTRY_OF_BIRTH_DROPDOWN)).click()
        wait.until(EC.element_to_be_clickable(SignUpLocators.COUNTRY_OF_BIRTH)).click()
        wait.until(EC.element_to_be_clickable(SignUpLocators.PLACE_OF_BIRTH)).send_keys(place_of_birth)
        wait.until(EC.element_to_be_clickable(SignUpLocators.MAIDEN_NAME)).send_keys(maiden_name)
        if driver.is_keyboard_shown():
            driver.hide_keyboard()

        wait.until(EC.element_to_be_clickable(SignUpLocators.CONTINUE_BUTTON)).click()
        WebDriverWait(context.driver, 300).until(
            EC.element_to_be_clickable(SignUpLocators.STAY_ON_HUGOLITE)
        ).click()

        wait.until(EC.presence_of_element_located(SignUpLocators.HOME_PAGE))

@step("I enter the valid mobile number with prefix ([^']*)")
def step_enter_valid_mobile_number(context, mobile_prefix):
    wait, driver = context.wait, context.driver
    mobile_number = Testing.generate_random_number(mobile_prefix)
    mobile_input = wait.until(EC.element_to_be_clickable(SignUpLocators.MOBILE_INPUT))
    mobile_input.clear()
    mobile_input.send_keys(mobile_number)

@Step('I click on the continue button')
def step_click_get_otp_button(context):
    wait, driver = context.wait, context.driver
    wait.until(
        EC.element_to_be_clickable(SignUpLocators.CONTINUE_BUTTON)
    ).click()

@step('After 20sec Resend OTP button should appear')
def step_resend_otp_button(context):
    wait, driver = context.wait, context.driver
    wait.until(
        EC.visibility_of_element_located(SignUpLocators.RESEND_OTP_BUTTON)
    )

@step('I click on Resend OTP')
def step_click_resend_otp(context):
    wait, driver = context.wait, context.driver
    wait.until(
        EC.element_to_be_clickable(SignUpLocators.RESEND_OTP_BUTTON)
    ).click()

@step('OTP sent SMS should appear')
def step_otp_sent_sms(context):
    wait, driver = context.wait, context.driver
    wait.until(
        EC.visibility_of_element_located(SignUpLocators.OTP_SENT_SNACKBAR)
    )

@Step("I enter casual name ([^']*)")
def step_enter_casual_name(context, name: str):
    wait, driver = context.wait, context.driver
    wait.until(EC.presence_of_element_located(SignUpLocators.CASUAL_NAME_FIELD)).send_keys(name)

@Step('I tick the terms checkbox')
def step_tick_terms_checkbox(context):
    wait, driver = context.wait, context.driver
    wait.until(
        EC.element_to_be_clickable(SignUpLocators.TERMS_CHECKBOX)
    ).click()

@step('I click Continue')
def step_click_continue(context):
    wait, driver = context.wait, context.driver
    wait.until(
        EC.element_to_be_clickable(SignUpLocators.CONTINUE_BUTTON)
    ).click()

@step('I select usage options')
def step_select_usage_options(context):
    wait, driver = context.wait, context.driver
    for locator in SignUpLocators.USAGE_OPTIONS.values():
        wait.until(EC.element_to_be_clickable(locator)).click()

@step('I enter passcodes in both fields')
def step_enter_passcode(context):
    wait, driver = context.wait, context.driver
    actions = ActionChains(driver)
    wait.until(EC.element_to_be_clickable(SignUpLocators.SET_PASSWORD))
    row = context.table[0]
    for digit in row['passcode1']:
        actions.send_keys(digit)
    actions.pause(1)
    for digit in row['passcode2']:
        actions.send_keys(digit)
    actions.perform()

@step("I enter place of birth ([^']*)")
def step_enter_place_birth(context, place_of_birth):
    wait, driver = context.wait, context.driver
    wait.until(EC.element_to_be_clickable(SignUpLocators.PLACE_OF_BIRTH)).send_keys(place_of_birth)

@step("I enter Maiden name ([^']*)")
def step_enter_maiden_name(context, maiden_name):
    wait, driver = context.wait, context.driver
    wait.until(EC.element_to_be_clickable(SignUpLocators.MAIDEN_NAME)).send_keys(maiden_name)

@step("I enter the personal details")
def step_enter_personal_details(context):
    wait, driver = context.wait, context.driver
    row = context.table[0]
    place_of_birth, maiden_name = row['place_of_birth'], row['mother_maiden_name']
    wait.until(EC.element_to_be_clickable(SignUpLocators.PLACE_OF_BIRTH)).send_keys(place_of_birth)
    wait.until(EC.element_to_be_clickable(SignUpLocators.MAIDEN_NAME)).send_keys(maiden_name)
    if driver.is_keyboard_shown():
        driver.hide_keyboard()

@step("I clear mobile number input field")
def step_clear_mobile_number(context):
    wait, driver = context.wait, context.driver
    wait.until(
        EC.element_to_be_clickable(SignUpLocators.MOBILE_INPUT)
    ).clear()

@step("An error text should appear")
def step_error_text(context):
    wait, driver = context.wait, context.driver
    wait.until(
        EC.visibility_of_element_located(SignUpLocators.MOBILE_INPUT_ERROR_TEXT)
    )

@step("I enter mobile number containing more than 10 digits with prefix ([^']*)")
def step_enter_mobile_number(context, mobile_prefix):
    wait, driver = context.wait, context.driver
    mobile_number = Testing.generate_random_number(mobile_prefix, digits_count=10)
    mobile_input = wait.until(EC.element_to_be_clickable(SignUpLocators.MOBILE_INPUT))
    mobile_input.clear()
    mobile_input.send_keys(mobile_number)

@step("I enter an invalid mobile number ([^']*)")
def step_enter_invalid_mobile_number(context, mobile_number):
    wait, driver = context.wait, context.driver
    mobile_input = wait.until(
        EC.element_to_be_clickable(SignUpLocators.MOBILE_INPUT)
    )
    mobile_input.clear()
    mobile_input.send_keys(mobile_number)

@step('The continue button should be disabled')
def step_check_get_otp_disabled(context):
    wait, driver = context.wait, context.driver
    wait.until(
        EC.presence_of_element_located(SignUpLocators.CONTINUE_BUTTON)
    )

@step(r"I enter OTP ([^']*)")
def step_enter_otp(context, otp):
    wait, driver = context.wait, context.driver
    Testing.enter_otp(driver, wait, otp)

@step("I enter Invalid OTP ([^']*) for four times")
def step_enter_invalid_otp(context, otp):
    wait, driver = context.wait, context.driver
    for i in range(4):
        time.sleep(1)
        Testing.enter_otp(driver, wait, otp)
        if i<3:
            wait.until(
                EC.visibility_of_element_located(SignUpLocators.INVALID_OTP_ERROR_TEXT)
            )

@step('An error message Incorrect OTP should display')
def step_incorrect_otp_error(context):
    wait, driver = context.wait, context.driver
    wait.until(
        EC.visibility_of_element_located(SignUpLocators.INVALID_OTP_ERROR_TEXT)
    )

@step('maximum attempts reached text should appear')
def step_max_attempts_error(context):
    wait, driver = context.wait, context.driver
    error = wait.until(
        EC.visibility_of_element_located(SignUpLocators.MAX_ATTEMPTS_ERROR_TEXT)
    )
    assert error.text == 'Incorrect OTP. You have reached the maximum attempts. Please retry in 30 mins.', 'WRONG ERROR MESSAGE'

@step('An error message should be displayed')
def step_incorrect_otp_error(context):
    wait, driver = context.wait, context.driver
    wait.until(
        EC.visibility_of_element_located(SignUpLocators.CASUAL_NAME_ERROR_TEXT)
    )

@step('The continue button is disabled')
def step_continue_button_disabled(context):
    wait, driver = context.wait, context.driver
    button = wait.until(
        EC.presence_of_element_located(SignUpLocators.CONTINUE_BUTTON)
    )
    assert button.get_attribute("enabled") == 'false', "Continue button is not disabled"

@step('The continue button is disabled in security questions screen')
def step_continue_button_disabled(context):
    wait, driver = context.wait, context.driver
    wait.until(
        EC.presence_of_element_located(SignUpLocators.PLACE_OF_BIRTH)
    )
    button = wait.until(
        EC.presence_of_element_located(SignUpLocators.CONTINUE_BUTTON)
    )
    assert button.get_attribute("enabled") == 'false', "Continue button is not disabled"

@step('The continue button is disabled in account usage options screen')
def step_continue_button_disabled(context):
    wait, driver = context.wait, context.driver
    wait.until(
        EC.presence_of_element_located(SignUpLocators.ACCOUNT_OPTIONS_TEXT)
    )
    button = wait.until(
        EC.presence_of_element_located(SignUpLocators.CONTINUE_BUTTON)
    )
    assert button.get_attribute("enabled") == 'false', "Continue button is not disabled"

@step('Passcode error text should display')
def step_passcode_error_text(context):
    wait, driver = context.wait, context.driver
    wait.until(
        EC.visibility_of_element_located(SignUpLocators.PASSCODE_ERROR_TEXT)
    )

@step("I validate that error message appear for invalid Mother's maiden name")
def step_maiden_error_text(context):
    wait, driver = context.wait, context.driver
    wait.until(
        EC.visibility_of_element_located(SignUpLocators.SECURITY_QUE_ERROR_TEXT)
    )
