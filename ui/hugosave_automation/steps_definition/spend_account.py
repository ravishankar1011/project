import time
from behave import given, when, then, use_step_matcher
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.ui.hugosave_automation.pages.util import Util
from tests.ui.hugosave_automation.pages.spend_account_locators import SpendAccountLocators
use_step_matcher("re")

@given("I tap on the spend account banner on the home screen")
def step_tap_spend_account_banner(context):
    Util.pull_to_refresh(context.driver, n_times=1)
    context.wait.until(EC.element_to_be_clickable(SpendAccountLocators.SPEND_ACCOUNT_TEXT)).click()

@when ("I tap on the Spend Account Dashboard Button and Close Announcement Modals")
def step_tap_spend_account_button(context):
    wait = context.wait
    wait.until(EC.element_to_be_clickable(SpendAccountLocators.SPEND_ACCOUNT_DASHBOARD_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(SpendAccountLocators.NEXT_BUTTON_ANNOUNCEMENT_MODAL)).click()

    wait.until(EC.element_to_be_clickable(SpendAccountLocators.DONE_BUTTON_ANNOUNCEMENT_MODAL)).click()

    context.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiScrollable(new UiSelector().scrollable(true)).scrollToBeginning(10)')


@when("I top up the Spend Account with ([^']*)")
def step_top_up_spend_account(context,amount):
    wait = context.wait
    Util.pull_to_refresh(context.driver, n_times=2)

    element = wait.until(EC.element_to_be_clickable(SpendAccountLocators.TOP_UP_FROM_SAVE_ACCOUNT_TEXT))
    location = element.location
    size = element.size
    x = location['x'] + size['width'] // 2
    y = location['y'] - 60
    Util.perform_touch_action(context.driver, int(x), int(y))

    Util.perform_touch_action(context.driver, int(x), int(y))

    wait.until(EC.element_to_be_clickable(SpendAccountLocators.TOP_UP_INPUT_FIELD)).send_keys(amount)

    wait.until(EC.element_to_be_clickable(SpendAccountLocators.TOP_UP_PREVIEW_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(SpendAccountLocators.PREVIEW_TOP_UP_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(SpendAccountLocators.GO_TO_DASHBOARD_BUTTON)).click()
    
    time.sleep(2)


@then("The Spend Account balance should reflect the ([^']*)")
def step_check_spend_account_balance(context,amount):
    Util.pull_to_refresh(context.driver, n_times=3)

    spend_account_balance_path = f'new UiSelector().text("{amount}")'

    balance = WebDriverWait(context.driver, 60).until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,spend_account_balance_path)))

    assert balance.text.strip()==amount, f"expected spend account balance is {amount} but got {balance.text.strip()}"

@then("I withdraw ([^']*) from the spend account")
def step_withdraw_from_spend_account(context,amount):
    wait = context.wait

    wait.until(EC.element_to_be_clickable(SpendAccountLocators.WITHDRAW_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(SpendAccountLocators.TOP_UP_INPUT_FIELD)).send_keys(amount)

    wait.until(EC.element_to_be_clickable(SpendAccountLocators.TOP_UP_PREVIEW_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(SpendAccountLocators.PREVIEW_WITHDRAW_BUTTON)).click()

@when("I lock the Spend Account")
def step_impl(context):
    element = context.wait.until(EC.element_to_be_clickable(SpendAccountLocators.LOCK_ACC_TEXT))

    location = element.location
    size = element.size
    x = location['x'] + size['width'] // 2
    y = location['y'] - 60
    Util.perform_touch_action(context.driver, int(x), int(y))

    context.wait.until(EC.element_to_be_clickable(SpendAccountLocators.LOCK_SPEND_ACCOUNT_BUTTON)).click()
