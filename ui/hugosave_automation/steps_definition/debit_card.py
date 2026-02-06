import time
from behave import given, when, then
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.ui.hugosave_automation.pages.util import Util
from tests.ui.hugosave_automation.pages.debit_card_locators import DebitCardLocators
from behave import use_step_matcher
use_step_matcher("re")


@given("I open the Debit Card section from the Spend Account Dashboard")
def step_go_to_debit_card_section(context):
    wait = context.wait
    Util.step_scroll_up(context.driver, 230)

    wait.until(EC.element_to_be_clickable(DebitCardLocators.DEBIT_CARD_ORDER_CARD)).click()

    wait.until(EC.element_to_be_clickable(DebitCardLocators.ORDER_DEBIT_CARD_DASHBOARD_BUTTON)).click()

    order_screen_header = wait.until(EC.presence_of_element_located(DebitCardLocators.ORDER_DEBIT_CARD_HEADER))
    expected_text = 'Order Hugosave Visa\nPlatinum Debit Card'

    assert order_screen_header.text == expected_text, f'Expected: {expected_text}, Got: {order_screen_header.text}'


@then('I tap on the Confirm button to place the Debit Card order')
def step_tap_confirm_button(context):
    context.wait.until(EC.element_to_be_clickable(DebitCardLocators.CONFIRM_BUTTON)).click()


@then('I should be redirected to the Card Dashboard with the ACTIVATE IT button visible')
def step_verify_activate_it_text(context):
    Util.pull_to_refresh(context.driver, 3)

    activate_it_text = context.wait.until(EC.presence_of_element_located(DebitCardLocators.ACTIVATE_IT_TEXT))
    assert activate_it_text.text.strip().lower() == 'activate it', f'Expected "Activate it", but got: "{activate_it_text.text}"'


@when("I tap on the ACTIVATE IT button and enter the token number ([^']*)")
def step_enter_card_token_number(context, token):
    context.wait.until(EC.element_to_be_clickable(DebitCardLocators.ACTIVATE_IT_TEXT)).click()
    Util.pull_to_refresh(context.driver, 2)

    token_input = context.wait.until(EC.presence_of_element_located(DebitCardLocators.CARD_TOKEN_INPUT_FIELD))
    token_input.clear()

    token_input.send_keys(token)


@then('I tap on the Activate Debit Card button to complete activation')
def step_tap_activate_button(context):
    context.wait.until(EC.element_to_be_clickable(DebitCardLocators.ACTIVATE_DEBIT_CARD_BUTTON)).click()


@then('I tap on the GO TO CARD DASHBOARD button and verify the card is visible on the dashboard')
def step_verify_debit_card(context):
    wait = context.wait
    wait.until(EC.element_to_be_clickable(DebitCardLocators.GO_TO_CARD_DASHBOARD_BUTTON)).click()

    Util.pull_to_refresh(context.driver, 2)

    expiry = wait.until(EC.presence_of_element_located(DebitCardLocators.EXPIRY_TEXT))

    cvv = wait.until(EC.presence_of_element_located(DebitCardLocators.CVV_TEXT))

    assert expiry.is_displayed(), "Card expiry text is not visible"
    assert cvv.is_displayed(), "CVV text is not visible"

@then('I go to the home screen')
def step_go_to_home_screen(context):
    wait = context.wait
    wait.until(EC.element_to_be_clickable(DebitCardLocators.BACK_BUTTON_ON_CARD_DASHBOARD)).click()
    time.sleep(2)
    wait.until(EC.element_to_be_clickable(DebitCardLocators.BACK_BUTTON_ON_SPEND_ACCOUNT)).click()
    time.sleep(3)
    wait.until(EC.element_to_be_clickable(DebitCardLocators.BACK_BUTTON_ON_SPEND_ACCOUNT_LEARNING_SCREEN)).click()
