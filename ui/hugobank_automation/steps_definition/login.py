from behave import *
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from tests.ui.hugobank_automation.pages.login_locators import LoginLocators
from behave import use_step_matcher
use_step_matcher("re")

@step("I enter mobile number")
def i_enter_valid_mobile_number(context):
   wait, driver = context.wait, context.driver
   wait.until(EC.presence_of_element_located(LoginLocators.MOBILE_INPUT))
   mobile_number = context.valid_mobile_number
   mobile_input = wait.until(EC.element_to_be_clickable(LoginLocators.MOBILE_INPUT))
   mobile_input.clear()
   mobile_input.send_keys(mobile_number)

@step("I enter the OTP")
def step_enter_otp(context):
   wait, driver = context.wait, context.driver
   wait.until(EC.presence_of_element_located(LoginLocators.ENTER_OTP_TEXT))
   actions = ActionChains(driver)
   for digit in '123456':
       actions.send_keys(digit)
   actions.perform()

@step("I enter passcode ([^']*)")
def step_enter_passcode(context, passcode):
   wait, driver = context.wait, context.driver
   wait.until(EC.presence_of_element_located(LoginLocators.ENTER_PASSCODE))
   wait.until(EC.element_to_be_clickable(LoginLocators.PASSCODE_FIELD)).click()
   actions = ActionChains(driver)
   for digit in passcode:
       actions.send_keys(digit)
   actions.perform()

@step('I click Allow notifications button')
def step_click_allow_notifications(context):
   wait, driver = context.wait, context.driver
   wait.until(
       EC.element_to_be_clickable(LoginLocators.ALLOW_NOTIFICATIONS_BUTTON)
   ).click()

@step('I should be navigated to Home page')
def step_home_page(context):
   wait, driver = context.wait, context.driver
   wait.until(
       EC.visibility_of_element_located(LoginLocators.HOME_PAGE)
   )

@step('I click on profile icon')
def step_profile_icon(context):
   wait, driver = context.wait, context.driver
   wait.until(
       EC.element_to_be_clickable(LoginLocators.PROFILE_ICON)
   ).click()

@step('I click on logout')
def step_logout(context):
   wait, driver = context.wait, context.driver
   wait.until(EC.element_to_be_clickable(LoginLocators.MENU_LOGOUT)).click()

   wait.until(EC.element_to_be_clickable(LoginLocators.MENU_LOGOUT)).click()

@step('Incorrect passcode error text should appear')
def step_incorrect_password_error_text(context):
   wait, driver = context.wait, context.driver
   wait.until(
       EC.visibility_of_element_located(LoginLocators.PASSCODE_ERROR_TEXT)
   )

@step('I click on Forgot Passcode')
def step_click_forgot_passcode(context):
   wait, driver = context.wait, context.driver
   wait.until(
       EC.element_to_be_clickable(LoginLocators.FORGOT_PASSCODE)
   ).click()

@step('App gets opened')
def step_app_opened(context):
   wait, driver = context.wait, context.driver
   driver.background_app(30)

@step("I authenticate with passcode ([^']*)")
def step_authenticate(context, passcode):
   wait, driver = context.wait, context.driver
   wait.until(EC.presence_of_element_located(LoginLocators.AUTHENTICATION)).click()
   actions = ActionChains(driver)
   for digit in passcode:
       actions.send_keys(digit)
   actions.perform()

@step('I provide the reset-passcode OTP')
def step_enter_otp_passcode(context):
    wait, driver = context.wait, context.driver
    wait.until(EC.presence_of_element_located(LoginLocators.OTP_FOR_PASSCODE_RESET))
    actions = ActionChains(driver)
    for digit in '123456':
        actions.send_keys(digit)
    actions.perform()
    wait.until(EC.visibility_of_element_located(LoginLocators.ID_VERIFIED_SNACKBAR))
