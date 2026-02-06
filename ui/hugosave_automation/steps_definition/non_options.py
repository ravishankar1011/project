from behave import use_step_matcher
use_step_matcher("re")
from behave import given, then
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait  # Use WebDriverWait from selenium
from selenium.webdriver.support import expected_conditions as EC
from tests.ui.hugosave_automation.pages.util import Util
import time
from tests.ui.hugosave_automation.pages.non_prod_options_locators import *

@then("I scroll down the menu screen")
def step_scroll_down_and_up(context):
    # Perform scrolling action until element found downwards
    down = context.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Enjoying our app?"))')
    assert down.is_displayed(), f'{down} is not displayed'
    print(down.text)

@then(r"I tap on the Deposit to your account button")
def step_tap_transaction_activities_option(context):

    deposit_button = '//android.view.ViewGroup[@content-desc="Deposit to your account"]'
    deposit = WebDriverWait(context.driver, 30).until(EC.presence_of_element_located((AppiumBy.XPATH, deposit_button)))
    if deposit:
        print("Deposit to your account button tapped.")
        deposit.click()

@then("I wait for ([^']*) sec")
def wait_for(context, sec):
    time.sleep(int(sec))


@then("I go to non_prod options and make a ([^']*) card transaction of ([^']*)")
def step_impl(context,type,amount):
    wait = WebDriverWait(context.driver, 40)
    wait.until(EC.element_to_be_clickable(NonProd.PROFILE_ICON_HOMESCREEN)).click()

    Util.step_scroll_up(context.driver, 250)

    current_version = wait.until(EC.element_to_be_clickable(NonProd.CURRENT_VERSION_BUTTON))
    if current_version:
        for _ in range(13):
            current_version.click()


        wait.until(EC.element_to_be_clickable(NonProd.NON_PROD_OPTIONS_BUTTON)).click()

        wait.until(EC.element_to_be_clickable(NonProd.CARD_ACTIVITIES)).click()
        time.sleep(3)

        wait.until(EC.element_to_be_clickable(NonProd.SELECT_AN_ACCOUNT)).click()

        wait.until(EC.element_to_be_clickable(NonProd.SPEND_ACCOUNT_BUTTON)).click()

        wait.until(EC.element_to_be_clickable(NonProd.SELECT_YOUR_CARD)).click()
        time.sleep(2)

        wait.until(EC.element_to_be_clickable(NonProd.CARD_TO_SELECT)).click()
        time.sleep(2)

        wait.until(EC.element_to_be_clickable(NonProd.AMOUNT_FIELD)).send_keys("10")

        wait.until(EC.element_to_be_clickable(NonProd.SELECT_TYPE)).click()
        time.sleep(2)

        wait.until(EC.element_to_be_clickable(NonProd.AUTH_CLEAR)).click()
        time.sleep(2)

        wait.until(EC.element_to_be_clickable(NonProd.CHANNEL)).click()
        time.sleep(2)

        wait.until(EC.element_to_be_clickable(NonProd.AUTH_CLEAR)).click()
        time.sleep(2)

        wait.until(EC.element_to_be_clickable(NonProd.MAKE_CARD_TRANSACTION)).click()
        time.sleep(2)

        wait.until(EC.element_to_be_clickable(NonProd.BACK_BUTTON_ON_NONPROD)).click()

        wait.until(EC.element_to_be_clickable(NonProd.SHOW_ME_AROUND)).click()
