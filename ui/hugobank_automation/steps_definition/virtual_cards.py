import time
from appium.webdriver.common.appiumby import AppiumBy
from behave import *
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.ui.hugobank_automation.pages.virtual_cards_locators import VirtualCards
from tests.ui.hugobank_automation.pages.non_prod_option_locators import NonProd
from tests.ui.hugobank_automation.pages.utils import Testing, pull_to_refresh_from_middle, pull_to_refresh
from appium.webdriver.extensions.android.nativekey import AndroidKey
from behave import use_step_matcher
use_step_matcher("re")

@step(u"I move to the order visa virtual debit card screen")
def move_to_order_virtual_cards_dashboard(context):

    wait, driver =  context.wait, context.driver

    wait.until(EC.element_to_be_clickable(VirtualCards.CARDS_TAB_ON_HOMESCREEN)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.CARDS_DASHBOARD_ON_LEARNING_SCREEN)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.NEW_CARD_BUTTON_ON_CARDS_DASHBOARD)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.VIRTUAL_TAB)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.ORDER_VIRTUAL_CARD_BUTTON)).click()

@step(u"I tap on the each pre defined card name labels")
def tap_on_each_card_name_label(context):

    wait, driver =  context.wait, context.driver

    context.selected_tabs = [row["toggle"] for row in context.table]

@step(u"I select each pre defined tab and validate the reflection in the card name field")
def tap_on_each_card_name_label(context):

    wait, driver =  context.wait, context.driver

    toggle_locators = {

        "Shopping": VirtualCards.SHOPPING_LABEL,
        "Grocery": VirtualCards.GROCERY_LABEL,
        "Subscription": VirtualCards.SUBSCRIPTION_LABEL,
        "Education": VirtualCards.EDUCATION_LABEL

    }

    field_locator = VirtualCards.CARD_NAME_INPUT_FIELD

    for toggle in context.selected_tabs:
        locator = toggle_locators.get(toggle)

        wait.until(EC.element_to_be_clickable(locator)).click()

        field_value = wait.until(
            EC.visibility_of_element_located(field_locator)
        ).text

        assert toggle in field_value

@step(r"I enter card name as ([^']*) in the field")
def input_card_name(context, card_name):

    wait, driver =  context.wait, context.driver

    wait.until(EC.element_to_be_clickable(VirtualCards.CARD_NAME_INPUT_FIELD)).clear().send_keys(card_name)

@step(u"I click on the place order button")
def input_card_name(context):

    wait, driver =  context.wait, context.driver

    wait.until(EC.element_to_be_clickable(VirtualCards.PLACE_ORDER_BUTTON)).click()


@step(r"I input valid passcode ([^']*)")
def input_card_name(context, passcode):

    wait, driver =  context.wait, context.driver

    forgot_btn = wait.until(EC.presence_of_element_located(VirtualCards.FORGOT_BUTTON))

    if forgot_btn:
        actions = ActionChains(driver)
        for digit in passcode:
            actions.send_keys(digit).perform()

@step(u"I order a virtual card with the below name and passcode")
def order_virtual_card(context):

    wait, driver =  context.wait, context.driver

    for card_name, passcode in context.table:

        wait.until(EC.element_to_be_clickable(VirtualCards.CARD_NAME_INPUT_FIELD)).send_keys(card_name)

        wait.until(EC.element_to_be_clickable(VirtualCards.CONTINUE_BUTTON)).click()

        wait.until(EC.element_to_be_clickable(VirtualCards.PLACE_ORDER_BUTTON)).click()

        continue_btn = wait.until(EC.visibility_of_element_located(VirtualCards.FORGOT_BUTTON))

        if continue_btn:
            actions = ActionChains(driver)
            for digit in passcode:
                actions.send_keys(digit).perform()

@step(u"I click on the unhide icon and validate full card number expiry and cvv text")
def click_on_unhide(context):

    wait, driver =  context.wait, context.driver

    wait.until(EC.element_to_be_clickable(VirtualCards.BACK_BUTTON_VIRTUAL_CARD_DASHBOARD)).click()

    while True:

        pull_to_refresh_from_middle(driver, n_times=1)

        elems = driver.find_elements(*VirtualCards.FIRST_VIRTUAL_CARD_ON_CARDS_DASHBOARD)
        if elems and elems[0].is_displayed():
            break

    wait.until(EC.element_to_be_clickable(VirtualCards.FIRST_VIRTUAL_CARD_ON_CARDS_DASHBOARD)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.UNHIDE_ICON)).click()

    wait.until(EC.visibility_of_element_located(VirtualCards.CARD_NUMBER_TEXT))

    wait.until(EC.visibility_of_element_located(VirtualCards.EXP_TEXT))

    wait.until(EC.visibility_of_element_located(VirtualCards.CVV_TEXT))

@step(u"I click on the copy button and validate copied text")
def copy_card_num(context):

    wait, driver =  context.wait, context.driver

    wait.until(EC.element_to_be_clickable(VirtualCards.COPY_BUTTON)).click()

    wait.until(EC.visibility_of_element_located(VirtualCards.COPIED_TEXT))

@step(u"I wait for the virtual card to be appeared on the card dashboard")
def wait_till_card_appear(context):

    wait, driver =  context.wait, context.driver

    wait.until(EC.element_to_be_clickable(VirtualCards.BACK_BUTTON_VIRTUAL_CARD_DASHBOARD)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.HOME_TAB)).click()

    pull_to_refresh(driver, n_times=2)

    wait.until(EC.element_to_be_clickable(VirtualCards.CARDS_TAB_ON_HOMESCREEN)).click()

    while True:
        pull_to_refresh_from_middle(driver, n_times=1)

        elems = driver.find_elements(*VirtualCards.FIRST_VIRTUAL_CARD_ON_CARDS_DASHBOARD)
        if elems and elems[0].is_displayed():
            break

@step(u"I click on the home tab")
def copy_card_num(context):

    wait, driver =  context.wait, context.driver

    wait.until(EC.element_to_be_clickable(VirtualCards.HOME_TAB)).click()

@step(u"I click on the card dashboard")
def copy_card_num(context):

    wait, driver =  context.wait, context.driver

    wait.until(EC.element_to_be_clickable(VirtualCards.CARD_DASHBOARD_BUTTON)).click()

@step(u"I click on the Save button")
def copy_card_num(context):

    wait, driver =  context.wait, context.driver

    wait.until(EC.visibility_of_element_located(VirtualCards.SAVE_BUTTON))

@step(u"I click on the back button on the virtual card dashboard")
def clicks_back_btn(context):

    wait, driver =  context.wait, context.driver

    wait.until(EC.element_to_be_clickable(VirtualCards.BACK_BUTTON_VIRTUAL_CARD_DASHBOARD)).click()

@step(u"I click on the back button on the cards dashboard")
def clicks_back_btn(context):

    wait, driver =  context.wait, context.driver
    pull_to_refresh_from_middle(driver, n_times=2)

    wait.until(EC.element_to_be_clickable(VirtualCards.BACK_BUTTON_ON_CARDS_DASHBOARD)).click()

@step(u"I click on the back button on the transaction record")
def clicks_back_btn(context):

    wait, driver =  context.wait, context.driver

    wait.until(EC.element_to_be_clickable(VirtualCards.BACK_BUTTON_ON_TRNX_RECORD)).click()

@step(r"I make an auth clear card transaction of PKR ([^']*)")
def make_transaction(context, trnx_amount):

    wait, driver =  context.wait, context.driver

    context.trnx_amount = trnx_amount

    current_account_balance = wait.until(EC.visibility_of_element_located(VirtualCards.CURRENT_ACC_BALANCE)).text

    context.current_account_balance = int(float(current_account_balance))

    wait.until(EC.element_to_be_clickable(NonProd.PROFILE_ICON_HOMESCREEN)).click()

    current_version_elem = driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true))'
        '.scrollIntoView(new UiSelector().descriptionContains("Current Version"))'
    )

    wait.until(EC.element_to_be_clickable(NonProd.NON_PROD_OPTIONS_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(NonProd.CARD_ACTIVITIES)).click()

    wait.until(EC.element_to_be_clickable(NonProd.SELECT_DROPDOWN_1)).click()

    wait.until(EC.element_to_be_clickable(NonProd.CURRENT_ACC_TEXT)).click()

    wait.until(EC.element_to_be_clickable(NonProd.SELECT_DROPDOWN_2)).click()

    wait.until(EC.element_to_be_clickable(NonProd.FIRST_VIRTUAL_CARD)).click()

    wait.until(EC.element_to_be_clickable(NonProd.ENTER_AMOUNT_FIELD)).send_keys(trnx_amount)

    wait.until(EC.element_to_be_clickable(NonProd.SELECT_DROPDOWN_3)).click()

    wait.until(EC.element_to_be_clickable(NonProd.AUTH_CLEAR)).click()

    wait.until(EC.element_to_be_clickable(NonProd.CHANNEL_DROPDOWN)).click()

    wait.until(EC.element_to_be_clickable(NonProd.E_COMMERCE)).click()

    wait.until(EC.element_to_be_clickable(NonProd.MAKE_CARD_TRANSACTION)).click()

    wait.until(EC.element_to_be_clickable(NonProd.NON_PROD_BACK_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(NonProd.TRANSACTIONS_TEXT_ON_HOMESCREEN)).click()

@step(u"I validate the current balance and transaction record on the virtual card dashboard")
def validation(context):

    wait, driver =  context.wait, context.driver

    pull_to_refresh(driver, n_times=3)

    transaction_amount = int(float(context.trnx_amount))

    current_balance_before_trnx = int(float(context.current_account_balance))

    current_balance_after_trnx= int(float(wait.until(EC.element_to_be_clickable(VirtualCards.CURRENT_ACC_BALANCE)).text))

    expected_balance = current_balance_before_trnx - transaction_amount

    assert expected_balance == current_balance_after_trnx

    pull_to_refresh(driver, n_times=3)

    wait.until(EC.element_to_be_clickable(VirtualCards.CARDS_TAB_ON_HOMESCREEN)).click()

    pull_to_refresh_from_middle(driver, n_times=4)

    wait.until(EC.element_to_be_clickable(VirtualCards.FIRST_VIRTUAL_CARD_ON_CARDS_DASHBOARD)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.FIRST_TRNX_RECORD_OF_VIRTUAL_CARD)).click()

    while True:
        actual_text = wait.until(EC.visibility_of_element_located(VirtualCards.CLOSED_TEXT_ON_TRNX_RECORD)).text
        if actual_text in ['Closed', 'Processing', 'Failed']:
            wait.until(EC.element_to_be_clickable(VirtualCards.BACK_BUTTON_ON_TRNX_RECORD)).click()
            time.sleep(2)
            wait.until(EC.element_to_be_clickable(VirtualCards.FIRST_TRNX_RECORD_OF_VIRTUAL_CARD)).click()
        else:
            break

    settled_text = wait.until(EC.visibility_of_element_located(VirtualCards.CLOSED_TEXT_ON_TRNX_RECORD)).text
    assert 'Settled' in settled_text

@step(r"I lock the virtual card with valid passcode ([^']*)")
def lock_card(context, passcode):

    wait, driver =  context.wait, context.driver

    wait.until(EC.element_to_be_clickable(VirtualCards.FIRST_VIRTUAL_CARD_ON_CARDS_DASHBOARD)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.LOCK_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.YES_BUTTON)).click()

    forgot_btn = wait.until(EC.visibility_of_element_located(VirtualCards.FORGOT_BUTTON))

    if forgot_btn:
        actions = ActionChains(driver)
        for digit in passcode:
            actions.send_keys(digit).perform()
        actions.pause(1)

    wait.until(EC.visibility_of_element_located(VirtualCards.CARD_IS_LOCKED_TEXT))

@step(u"I validate failed transaction record on the virtual card dashboard")
def validation(context):

    wait, driver =  context.wait, context.driver

    pull_to_refresh(driver, n_times=1)

    wait.until(EC.element_to_be_clickable(VirtualCards.CARDS_TAB_ON_HOMESCREEN)).click()

    pull_to_refresh_from_middle(driver, n_times=3)

    wait.until(EC.element_to_be_clickable(VirtualCards.FIRST_VIRTUAL_CARD_ON_CARDS_DASHBOARD)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.FIRST_TRNX_RECORD_OF_VIRTUAL_CARD)).click()

    while True:
        actual_text = wait.until(EC.visibility_of_element_located(VirtualCards.CLOSED_TEXT_ON_TRNX_RECORD)).text
        if actual_text in ['Closed', 'Processing']:
            wait.until(EC.element_to_be_clickable(VirtualCards.BACK_BUTTON_ON_TRNX_RECORD)).click()
            time.sleep(2)
            wait.until(EC.element_to_be_clickable(VirtualCards.FIRST_TRNX_RECORD_OF_VIRTUAL_CARD)).click()
        else:
            break

    settled_text = wait.until(EC.visibility_of_element_located(VirtualCards.CLOSED_TEXT_ON_TRNX_RECORD)).text
    assert 'Failed' in settled_text

@step(r"I unlock the virtual card with valid passcode ([^']*)")
def unlock_card(context, passcode):

    wait, driver =  context.wait, context.driver

    wait.until(EC.element_to_be_clickable(VirtualCards.UNLOCK_ICON)).click()

    forget_btn = wait.until(EC.visibility_of_element_located(VirtualCards.FORGOT_BUTTON))

    if forget_btn:
        actions = ActionChains(driver)
        for digit in passcode:
            actions.send_keys(digit).perform()
        time.sleep(10)

@step(u"I click on the back button on the emulator")
def back_button(context):

    wait, driver =  context.wait, context.driver

    unhide = wait.until(EC.visibility_of_element_located(VirtualCards.UNHIDE_ICON))

    if unhide:
        driver.press_keycode(AndroidKey.BACK)

@step(u"I reach to the cards dashboard")
def back_button(context):

    wait, driver =  context.wait, context.driver

    view_history_text = wait.until(EC.visibility_of_element_located(VirtualCards.VIEW_EDIT_HISTORY_BUTTON))

    if view_history_text:
        wait.until(EC.element_to_be_clickable(VirtualCards.BACK_BUTTON_ON_E_COMMERCE_SCREEN)).click()
        edit_card_label_text = wait.until(EC.visibility_of_element_located(VirtualCards.EDIT_CARD_LABEL_TEXT))
        if edit_card_label_text:
            wait.until(EC.element_to_be_clickable(VirtualCards.BACK_BUTTON_ON_MANAGE_CARD_SCREEN)).click()
            roundups_text = wait.until(EC.visibility_of_element_located(VirtualCards.ROUNDUPS_TEXT_ON_CARDS_DASHBOARD))
            if roundups_text:
                wait.until(EC.element_to_be_clickable(VirtualCards.BACK_BUTTON_VIRTUAL_CARD_DASHBOARD)).click()

@step(u"I move to the cards dashboard")
def back_button(context):

    wait, driver =  context.wait, context.driver

    wait.until(EC.element_to_be_clickable(VirtualCards.BACK_BUTTON_ON_TRNX_RECORD)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.BACK_BUTTON_VIRTUAL_CARD_DASHBOARD)).click()

@step(r"I update the virtual card default limit to ([^']*)")
def update_card_limits(context, amount):

    wait, driver =  context.wait, context.driver

    wait.until(EC.element_to_be_clickable(VirtualCards.FIRST_VIRTUAL_CARD_ON_CARDS_DASHBOARD)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.MANAGE_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.E_COMMERCE_BUTTON_ON_MANAGE_CARD_SCREEN)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.LIMIT_EDIT_ICON)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.LIMIT_AMOUNT_FIELD)).clear().send_keys(amount)

    wait.until(EC.element_to_be_clickable(VirtualCards.SAVE_BUTTON)).click()

@step(u"I validate daily limit reaching soon text on the virtual card dashboard")
def alert_text_validation(context):

    wait, driver =  context.wait, context.driver

    wait.until(EC.element_to_be_clickable(VirtualCards.CARDS_TAB_ON_HOMESCREEN)).click()

    pull_to_refresh_from_middle(driver, n_times=2)

    text = wait.until(EC.visibility_of_element_located(VirtualCards.LIMIT_ALERT_TEXT)).text.strip()

    actual_text = "Limit alert"

    assert actual_text == text

    wait.until(EC.element_to_be_clickable(VirtualCards.FIRST_VIRTUAL_CARD_ON_CARDS_DASHBOARD)).click()

    limit_reaching_soon_text = wait.until(EC.visibility_of_element_located(VirtualCards.E_COMMERCE_DAILY_LIMIT_REACHING_SOON_TEXT)).text.strip()

    expected_text = "E-commerce Daily Spend Limit reaching soon!"

    assert limit_reaching_soon_text == expected_text

    wait.until(EC.element_to_be_clickable(VirtualCards.MANAGE_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.E_COMMERCE_BUTTON_ON_MANAGE_CARD_SCREEN)).click()

    daily_limit_reaching_soon_text = wait.until(EC.visibility_of_element_located(VirtualCards.DAILY_LIMIT_REACHING_SOON_TEXT)).text.strip()

    expected_text2 = "Daily limit reaching soon!"

    assert daily_limit_reaching_soon_text == expected_text2


@step(u"I validate daily limit exhausted text on the virtual card dashboard")
def validate_limit_exhausted_text(context):

    wait, driver =  context.wait, context.driver

    wait.until(EC.element_to_be_clickable(VirtualCards.CARDS_TAB_ON_HOMESCREEN)).click()

    pull_to_refresh_from_middle(driver, n_times=2)

    text = wait.until(EC.visibility_of_element_located(VirtualCards.LIMIT_ALERT_TEXT)).text.strip()

    actual_text = "Limit alert"

    assert actual_text == text

    wait.until(EC.element_to_be_clickable(VirtualCards.FIRST_VIRTUAL_CARD_ON_CARDS_DASHBOARD)).click()

    limit_exhausted_text = wait.until(EC.visibility_of_element_located(VirtualCards.E_COMMERCE_DAILY_LIMIT_EXHAUSTED_TEXT)).text.strip()

    expected_text = "E-commerce Daily Spend Limit exhausted!"

    assert limit_exhausted_text == expected_text

    wait.until(EC.element_to_be_clickable(VirtualCards.MANAGE_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.E_COMMERCE_BUTTON_ON_MANAGE_CARD_SCREEN)).click()

    daily_limit_reaching_soon_text = wait.until(EC.visibility_of_element_located(VirtualCards.DAILY_LIMIT_EXHAUSTED_TEXT)).text.strip()

    expected_text2 = "Daily limit exhausted!"

    assert daily_limit_reaching_soon_text == expected_text2

@step(u"I turn off the 'E-commerce' toggle")
def turn_off_toggle(context):

    wait, driver =  context.wait, context.driver

    wait.until(EC.element_to_be_clickable(VirtualCards.FIRST_VIRTUAL_CARD_ON_CARDS_DASHBOARD)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.MANAGE_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.E_COMMERCE_BUTTON_ON_MANAGE_CARD_SCREEN)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.LIMIT_EDIT_ICON)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.LOCAL_TOGGLE_ICON)).click()

@step(u"I move to the homescreen")
def reach_homescreen_from_e_commerce_screen(context):

    wait, driver =  context.wait, context.driver

    status = wait.until(EC.visibility_of_element_located(VirtualCards.OFF_TEXT))

    if status:
        wait.until(EC.element_to_be_clickable(VirtualCards.BACK_BUTTON_ON_E_COMMERCE_SCREEN)).click()

        wait.until(EC.element_to_be_clickable(VirtualCards.BACK_BUTTON_ON_MANAGE_CARD_SCREEN)).click()

        wait.until(EC.element_to_be_clickable(VirtualCards.BACK_BUTTON_VIRTUAL_CARD_DASHBOARD)).click()

        wait.until(EC.element_to_be_clickable(VirtualCards.HOME_TAB)).click()

@step(u"I cancel the virtual card")
def cancel_virtual_card(context):

    wait, driver =  context.wait, context.driver

    wait.until(EC.element_to_be_clickable(VirtualCards.FIRST_VIRTUAL_CARD_ON_CARDS_DASHBOARD)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.MANAGE_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.CANCEL_CARD_TAB_ON_THE_MANAGE_CARD)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.CANCEL_CARD_BUTTON)).click()

@step(u"I validate the cancelled text on the screen")
def cancel_virtual_card(context):

    wait, driver =  context.wait, context.driver

    wait.until(EC.visibility_of_element_located(VirtualCards.ORDER_NEW_VIRTUAL_CARD_TEXT))

    wait.until(EC.element_to_be_clickable(VirtualCards.SKIP_BUTTON)).click()

    wait.until(EC.visibility_of_element_located(VirtualCards.CARD_IS_CANCELLED_TEXT))


@step(u"I move to the order visa virtual debit card screen from the cards dashboard")
def move_to_order_virtual_cards_dashboard(context):

    wait, driver =  context.wait, context.driver

    wait.until(EC.element_to_be_clickable(VirtualCards.NEW_CARD_BUTTON_ON_CARDS_DASHBOARD)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.VIRTUAL_TAB)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.ORDER_VIRTUAL_CARD_BUTTON)).click()

@step(u"I validate order virtual card button should be in disable state")
def validate_order_virtual_card_btn(context):

    wait, driver =  context.wait, context.driver

    wait.until(EC.element_to_be_clickable(VirtualCards.NEW_CARD_BUTTON_ON_CARDS_DASHBOARD)).click()

    wait.until(EC.element_to_be_clickable(VirtualCards.VIRTUAL_TAB)).click()

    order_virtual_card_btn = wait.until(EC.visibility_of_element_located(VirtualCards.ORDER_VIRTUAL_CARD_BUTTON))

    assert not order_virtual_card_btn.is_enabled()
