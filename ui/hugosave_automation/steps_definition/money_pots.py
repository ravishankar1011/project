from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from behave import then, when, given
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
import time
from tests.ui.hugosave_automation.pages.metals_locators import GoldPage
from tests.ui.hugosave_automation.pages.util import Util
from tests.ui.hugosave_automation.pages.non_prod_options_locators import NonProd
from tests.ui.hugosave_automation.pages.money_pots import Pots
from behave import *
import re
from tests.ui.hugosave_automation.pages import metals_locators
from tests.ui.hugosave_automation.pages.etfs_locators import ETFs
use_step_matcher("re")

@when(u'I click on the new pot icon')
def step_impl(context):
    driver = context.driver
    wait = context.wait
    element = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("newPotText")')))
    location = element.location
    size = element.size
    x = location['x'] + size['width'] // 2
    y = location['y'] - 60
    Util.perform_touch_action(context.driver, int(x), int(y))

@when(u'I move to the pot dashboard from the homescreen')
def step_impl(context):
    driver = context.driver
    wait = context.wait
    driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true).instance(0))'
        '.setAsVerticalList()'
        '.scrollIntoView(new UiSelector().description("Get Started"));'
    )
    wait.until(EC.element_to_be_clickable(Pots.GET_STARTED_BUTTON_ON_HOMESCREEN)).click()
    wait.until(EC.element_to_be_clickable(Pots.GET_STARTED_BUTTON_ON_LEARNING_SCREEN)).click()

@when(r"I input pot name as ([^']*)")
def step_impl(context,name):
    driver = context.driver
    wait = context.wait
    wait.until(EC.element_to_be_clickable(Pots.POT_NAME_FIELD)).send_keys(name)

@when(r"I enter goal amount as ([^']*)")
def step_impl(context,amount):
    driver = context.driver
    wait = context.wait
    amount  = int (amount)
    wait.until(EC.element_to_be_clickable(Pots.GOAL_AMOUNT_FIELD)).send_keys(amount)

@when(u'I select goal date')
def step_impl(context):
    driver = context.driver
    wait = context.wait
    wait.until(EC.element_to_be_clickable(Pots.CALENDER_ICON)).click()
    wait.until(EC.element_to_be_clickable(Pots.OK_BUTTON_ON_CALENDER)).click()

@when(u'I click on the next button')
def step_impl(context):
    driver = context.driver
    wait = context.wait
    wait.until(EC.element_to_be_clickable(Pots.NEXT_BUTTON)).click()

@when(u'I click on the create pot button')
def step_impl(context):
    driver = context.driver
    wait = context.wait
    wait.until(EC.element_to_be_clickable(Pots.CREATE_POT_BUTTON)).click()

@then(u'I validate successfully created text on the screen')
def step_impl(context):
    driver = context.driver
    wait = context.wait
    wait.until(EC.visibility_of_element_located(Pots.SUCCESS_TEXT))

@when(u'I click on the add one dollar to the pot button after creation')
def step_impl(context):
    driver = context.driver
    wait = context.wait
    wait.until(EC.element_to_be_clickable(Pots.ADD_ONE_DOLLAR_BUTTON)).click()

@when(u'I click on the add button on the preview screen')
def step_impl(context):
    driver = context.driver
    wait = context.wait
    wait.until(EC.element_to_be_clickable(Pots.ADD_BUTTON)).click()

@then(r"I validate current value of the pot ([^']*)")
def step_impl(context, value):
    driver = context.driver
    wait = context.wait
    record = wait.until(EC.element_to_be_clickable(Pots.TRNX_RECORD)).click()
    time.sleep(3)
    wait.until(EC.element_to_be_clickable(Pots.BACK_BUTTON)).click()
    if record:
        element = wait.until(EC.visibility_of_element_located(Pots.CURRENT_VALUE_ON_POT_DASHBOARD))
        value_text = element.text.strip()
        actual_value = int(float(value_text))
        expected_value = int(float(value))
        assert actual_value == expected_value, f"Expected value to be 1.00 but got {value_text}"

@when(u'I click on the i will do it later button')
def step_impl(context):
    driver = context.driver
    wait = context.wait
    wait.until(EC.element_to_be_clickable(Pots.I_WILL_DO_IT_LATER_BUTTON)).click()

@when(u'I click on the add to pot button on the pot dashboard')
def step_impl(context):
    driver = context.driver
    wait = context.wait
    wait.until(EC.element_to_be_clickable(Pots.ADD_TO_POT_BUTTON)).click()

@then(u'I validate amount added successfully text on the screen')
def step_impl(context):
    driver = context.driver
    wait = context.wait
    wait.until(EC.visibility_of_element_located(Pots.AMOUNT_ADDED_SUCCESSFULLY_TEXT))

@when(u'I click on the withdraw button')
def step_impl(context):
    driver = context.driver
    wait = context.wait
    wait.until(EC.element_to_be_clickable(Pots.WITHDRAW_BUTTON)).click()

@when(u'I click on the withdraw button on the preview screen')
def step_impl(context):
    driver = context.driver
    wait = context.wait
    wait.until(EC.element_to_be_clickable(Pots.WITHDRAW_BUTTON_ON_PREVIEW)).click()

@then(u'I validate withdrawn successfully text')
def step_impl(context):
    driver = context.driver
    wait = context.wait
    wait.until(EC.element_to_be_clickable(Pots.WITHDRAWN_SUCCESSFULLY_TEXT)).click()
