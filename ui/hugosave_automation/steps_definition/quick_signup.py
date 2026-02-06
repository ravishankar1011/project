from behave import *
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
import time
from tests.ui.hugosave_automation.pages.signup_locators import Signup
from tests.ui.hugosave_automation.pages.non_prod_options_locators import NonProd
from tests.ui.hugosave_automation.pages.home_screen_locators import HomeScreen
from tests.ui.hugosave_automation.pages.util import Util
from tests.ui.hugosave_automation.steps_definition.data_class import *
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from behave import use_step_matcher
use_step_matcher("re")

@step(u'I signup using bypass number')
def signup(context):
    driver = context.driver
    wait = context.wait

    row = context.table[0]
    data = SignupData(
        casual_name=row["Casual Name"],
        legal_name=row["Legal Name"],
        email=row["Email"],
        passcode=row["Passcode"]
    )

    random_digits = "".join(random.choice("0123456789") for _ in range(10))
    mobile_number = "+378" + random_digits
    wait.until(EC.element_to_be_clickable(Signup.MOBILE_INPUT_FIELD)).clear().send_keys(mobile_number)
    wait.until(EC.element_to_be_clickable(Signup.GET_OTP_BUTTON)).click()

    otp = wait.until(EC.visibility_of_element_located(Signup.ENTER_6_DIGIT_OTP_TEXT))
    if otp:
        actions = ActionChains(driver)
        for i in range(1, 7):
            actions.send_keys(str(i)).perform()
            time.sleep(0.1)

    details_screen = wait.until(EC.visibility_of_element_located(Signup.EMAIL))
    if details_screen:
        wait.until(EC.element_to_be_clickable(Signup.CASUAL_NAME_FIELD)).clear().send_keys(data.casual_name)
        wait.until(EC.element_to_be_clickable(Signup.FULL_NAME_FIELD)).clear().send_keys(data.legal_name)
        wait.until(EC.element_to_be_clickable(Signup.EMAIL_FIELD)).clear().send_keys(data.email)
        wait.until(EC.element_to_be_clickable(Signup.CHECKBOX)).click()
        wait.until(EC.element_to_be_clickable(Signup.CONTINUE_BUTTON)).click()

    passcode_screen = wait.until(EC.visibility_of_element_located(Signup.SET_YOUR_PASSCODE_TEXT))
    if passcode_screen:
        actions = ActionChains(driver)
        for digit in data.passcode:
            actions.send_keys(digit).perform()
            time.sleep(0.1)

        for digit in data.passcode:
            actions.send_keys(digit).perform()
            time.sleep(0.1)
    wait.until(EC.element_to_be_clickable(Signup.CREATE_ACCOUNT_BUTTON)).click()
    wait.until(EC.element_to_be_clickable(Signup.ALLOW_NOTIFICATIONS_BUTTON)).click()
    wait.until(EC.element_to_be_clickable(Signup.CLOSE_SHOW_ME_AROUND)).click()

@when(u'I wait for the premium upgrade to complete')
def upgrade_to_premium(context):
    driver = context.driver
    wait = context.wait

    wait._timeout = 120
    wait._poll = 15

    wait.until(
        lambda d: (
                          Util.pull_to_refresh(d, n_times=1) or True
                  ) and d.find_element(*Signup.LOW_BALANCE_ICON_OF_SPEND_ACCOUNT).is_displayed()
    )


@when(r"I deposit amount using non prod options ([^']*)")
def deposit_amount(context,amount):

    driver = context.driver
    wait = context.wait

    wait.until(EC.element_to_be_clickable(NonProd.PROFILE_ICON_HOMESCREEN)).click()

    for i in range(12):
        wait.until(EC.element_to_be_clickable(NonProd.CURRENT_VERSION_BUTTON)).click()
        time.sleep(1)

    driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Enjoying our app?"))',
    )

    wait.until(EC.element_to_be_clickable(NonProd.NON_PROD_OPTIONS_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(NonProd.TRANSACTION_ACTIVITIES)).click()

    wait.until(EC.element_to_be_clickable(NonProd.INPUT_AMOUNT_FIELD)).send_keys(amount)

    wait.until(EC.element_to_be_clickable(NonProd.DEPOSIT_TO_YOUR_ACCOUNT_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(NonProd.BACK_BUTTON_ON_NONPROD)).click()

    time.sleep(2)

    wait.until(EC.element_to_be_clickable(Signup.LOW_BALANCE_ICON_OF_SPEND_ACCOUNT)).click()
