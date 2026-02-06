from behave import given, when, then, step
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.ui.hugobank_automation.pages.payee_locators import PayeeLocator
from tests.ui.hugobank_automation.pages.utils import Testing
from appium.webdriver.common.appiumby import AppiumBy

from tests.ui.hugobank_automation.pages.utils import *
from appium.webdriver.extensions.android.nativekey import AndroidKey
from datetime import timedelta, datetime, time
import pytz
import time as time_module

from behave import use_step_matcher
use_step_matcher("re")

@step("I tapped on the Fund Transfer button and selected Other Bank Account Details")
def step_tap_other_bank_details(context):
    wait = context.wait
    wait.until(EC.presence_of_element_located(PayeeLocator.FUNDTRANSFER_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.ADD_PAYEE_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.ADD_NEW_PAYEE_TEXT))
    wait.until(EC.element_to_be_clickable(PayeeLocator.OTHERBANK_ACCOUNT_DETAILS_BUTTON)).click()

@step("I enter account details")
def step_enter_account_details(context):
    driver, wait = (context.driver, context.wait)

    for bank_name, account_prefix in context.table:

        if bank_name:
            bank_dropdown = wait.until(EC.element_to_be_clickable(PayeeLocator.BANK_NAME_BOX))
            bank_dropdown.click()
            scrollable_locator = (
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiScrollable(new UiSelector().scrollable(true))'
                f'.scrollIntoView(new UiSelector().text("{bank_name}"))'
            )
            wait.until(EC.presence_of_element_located(scrollable_locator)).click()

        if account_prefix:
            account_number = Testing.generate_random_number(account_prefix, 9)
            acc_field = wait.until(EC.element_to_be_clickable(PayeeLocator.ACCOUNT_INPUT_FIELD))
            acc_field.clear()
            acc_field.send_keys(account_number)

@step('I enter account details with IBAN')
def step_enter_account_details_with_iban(context):
    driver, wait = (context.driver, context.wait)

    for bank_name, IBAN_prefix in context.table:
        if bank_name:
            bank_dropdown = wait.until(EC.element_to_be_clickable(PayeeLocator.BANK_NAME_BOX))
            bank_dropdown.click()
            scrollable_locator = (
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiScrollable(new UiSelector().scrollable(true))'
                f'.scrollIntoView(new UiSelector().text("{bank_name}"))'
            )
            wait.until(EC.presence_of_element_located(scrollable_locator)).click()

        if IBAN_prefix:
            IBAN_number = Testing.generate_random_number(IBAN_prefix, 20)
            acc_field = wait.until(EC.element_to_be_clickable(PayeeLocator.ACCOUNT_INPUT_FIELD))
            acc_field.clear()
            acc_field.send_keys(IBAN_number)

@step("The Submit button should be disabled")
def step_verify_submit_disabled(context):
    driver, wait = (context.driver, context.wait)
    submit_button = wait.until(EC.presence_of_element_located(PayeeLocator.SUBMIT_BUTTON))
    assert not submit_button.is_enabled()

@step("I clear the account number field")
def step_clear_account_number(context):
    context.wait.until(EC.element_to_be_clickable(PayeeLocator.ACCOUNT_INPUT_FIELD)).clear()

@step("I should see an error message No account found")
def step_check_no_account_msg(context):
    wait = context.wait
    wait.until(EC.presence_of_element_located(PayeeLocator.SUBMIT_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.NO_ACCOUNT_FOUND_ERROR))

@step("I click on Submit button")
def step_submit_button(context):
    context.wait.until(EC.presence_of_element_located(PayeeLocator.SUBMIT_BUTTON)).click()

@step("I click on Get OTP button")
def step_tap_get_otp(context):
    context.wait.until(EC.presence_of_element_located(PayeeLocator.GET_OTP_BUTTON)).click()

@step("I enter the OTP ([^']*)")
def step_enter_correct_otp(context, otp):
    driver, wait = (context.driver, context.wait)
    wait.until(EC.presence_of_element_located(PayeeLocator.OTP_SCREEN_TEXT))
    otp_number = list(otp)
    actions = ActionChains(driver)
    for i in otp_number:
        actions.send_keys(str(i)).perform()

@step("I should see an error message Incorrect OTP")
def step_error_incorrect_otp(context):
    context.wait.until(EC.presence_of_element_located(PayeeLocator.INCORRECT_OTP_TEXT))

@step("I enter the passcode ([^']*)")
def step_enter_passcode(context, passcode):
    driver, wait = (context.driver, context.wait)
    wait.until(EC.presence_of_element_located(PayeeLocator.ENTER_PASSCODE_TEXT))
    passcode_number=list(passcode)
    actions = ActionChains(driver)
    for i in passcode_number:
        actions.send_keys(str(i)).perform()

@step("I should see an error message Incorrect Passcode")
def step_error_incorrect_passcode(context):
    context.wait.until(EC.presence_of_element_located(PayeeLocator.INCORRECT_PASSCODE_TEXT))

@step("The payee should be added successfully")
def step_new_payee_screen(context):
    wait = context.wait
    wait.until(EC.presence_of_element_located(PayeeLocator.PAYEENAME_NEW_PAYEESCREEN))
    wait.until(EC.presence_of_element_located(PayeeLocator.BANKDETAIL_NEW_PAYEESCREEN))
    wait.until(EC.presence_of_element_located(PayeeLocator.PAYBUTTON))

@step("I validate the UI of the Account Page")
def step_validate_account_page(context):
    wait = context.wait
    wait.until(EC.presence_of_element_located(PayeeLocator.BANK_NAME_TEXT))
    wait.until(EC.presence_of_element_located(PayeeLocator.TEST_BANK_RAAST_TEXT))
    wait.until(EC.presence_of_element_located(PayeeLocator.BANK_ACCOUNT_TEXT))
    wait.until(EC.presence_of_element_located(PayeeLocator.FAVOURITE_TEXT))
    wait.until(EC.presence_of_element_located(PayeeLocator.CANCEL_BUTTON))
    wait.until(EC.presence_of_element_located(PayeeLocator.GET_OTP_BUTTON))

@step("I go to Home Screen from Payee screen")
def step_tap_back_button(context):
    wait = context.wait
    wait.until(EC.presence_of_element_located(PayeeLocator.PAYBUTTON))
    wait.until(EC.presence_of_element_located(PayeeLocator.BACK_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.ADD_PAYEE_BUTTON))
    wait.until(EC.presence_of_element_located(PayeeLocator.BACK_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.HOMESCREEN_PROFILE_ICON))

@step("I click on Add Payee button")
def step_tap_add_payee_button(context):
    context.wait.until(EC.presence_of_element_located(PayeeLocator.ADD_PAYEE_BUTTON)).click()

@step("I click on Pay button")
def step_tap_pay_button(context):
   context.wait.until(EC.element_to_be_clickable(PayeeLocator.PAYBUTTON)).click()

@step("I enter amount ([^']*) and select purpose of transaction")
def step_enter_amount(context, amount):
   wait = context.wait
   payment_input = wait.until(EC.element_to_be_clickable(PayeeLocator.PAYMENT_INPUT))
   payment_input.send_keys(amount)
   time_module.sleep(4)
   wait.until(EC.presence_of_element_located(PayeeLocator.PURPOSE_OF_TRANSACTION_BUTTON)).click()
   wait.until(EC.presence_of_element_located(PayeeLocator.PURPOSE_OF_TRANSACTION_OPTION)).click()

@step("I click on Proceed and Pay buttons")
def step_tap_proceed_button(context):
   wait = context.wait
   wait.until(EC.presence_of_element_located(PayeeLocator.PROCEED_BUTTON)).click()
   wait.until(EC.presence_of_element_located(PayeeLocator.NEW_PAYMENT_BUTTON)).click()

@step("The transaction should be settled")
def step_check_transaction(context):
   wait = context.wait
   wait.until(EC.presence_of_element_located(PayeeLocator.BACK_TO_DASHBOARD_BUTTON)).click()
   pull_to_refresh(context.driver, 3)
   wait.until(EC.presence_of_element_located(PayeeLocator.OUTGOING_PAYMENT_TEXT)).click()
   settled_text = wait.until(EC.presence_of_element_located(PayeeLocator.SETTLED_TEXT))
   assert "Settled" in settled_text.text
   wait.until(EC.presence_of_element_located(PayeeLocator.AMOUNT_TEXT))
   wait.until(EC.presence_of_element_located(PayeeLocator.TOTAL_TEXT))

@step("I tapped on the Fund Transfer button and selected RAAST ID")
def step_tap_RAAST_ID(context):
    wait = context.wait
    wait.until(EC.presence_of_element_located(PayeeLocator.FUNDTRANSFER_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.ADD_PAYEE_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.RAAST_ID_BUTTON)).click()

@step("I enter the RAAST ID")
def step_enter_RAAST_ID(context):
    wait = context.wait
    wait.until(EC.presence_of_element_located(PayeeLocator.RAAST_ID_INPUT))
    RAAST_ID = Testing.generate_random_number('46', 8)
    input_field = wait.until(EC.element_to_be_clickable(PayeeLocator.RAAST_ID_INPUT))
    input_field.send_keys(RAAST_ID)

@step("I validate Submit button is in disable state")
def step_validate_submit_button(context):
    wait = context.wait
    submit_button = wait.until(EC.presence_of_element_located(PayeeLocator.SUBMIT_BUTTON))
    assert not submit_button.is_enabled()

@step("I enter the incorrect RAAST ID")
def step_enter_incorrect_RAAST_ID(context):
    wait = context.wait
    incorrect_RAAST_ID = Testing.generate_random_number('45', 8)
    input_field = wait.until(EC.element_to_be_clickable(PayeeLocator.RAAST_ID_INPUT))
    input_field.send_keys(incorrect_RAAST_ID)
    wait.until(EC.presence_of_element_located(PayeeLocator.SUBMIT_BUTTON)).click()

@step("I clear the RAAST ID input field")
def step_clear_RAAST_ID_input(context):
    context.wait.until(EC.presence_of_element_located(PayeeLocator.RAAST_ID_INPUT)).clear()

@step("I save the internal account number and IBAN number")
def step_store_internal_account_number(context):
    driver, wait = (context.driver, context.wait)
    wait.until(EC.presence_of_element_located(PayeeLocator.ACCOUNT_CARD_TEXT)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.HUGOBANK_ACCOUNT_DASHBOARD_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.ACCOUNT_DETAILS_TEXT)).click()
    DataStore.internal_account_number = wait.until(EC.presence_of_element_located(PayeeLocator.ACCOUNT_NUMBER_VALUE)).text
    DataStore.internal_IBAN_number = wait.until(EC.presence_of_element_located(PayeeLocator.IBAN_NUMBER_VALUE)).text
    wait.until(EC.presence_of_element_located(PayeeLocator.BACK_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.HUGOBANK_ACCOUNT_TEXT))
    wait.until(EC.presence_of_element_located(PayeeLocator.BACK_BUTTON)).click()

@step("I link the Raast ID to the Hugobank account number")
def step_link_raast_id(context):
    driver, wait = (context.driver, context.wait)
    wait.until(EC.presence_of_element_located(PayeeLocator.FUNDTRANSFER_BUTTON))
    wait.until(EC.presence_of_element_located(PayeeLocator.HOMESCREEN_PROFILE_ICON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.RAAST_MANAGEMENT_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.CREATE_RAASTID_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.SUBMIT_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.LINK_RAASTID_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.SUBMIT_BUTTON)).click()

@step("I save the internal Raast ID")
def step_save_internal_raast_id(context):
    driver, wait = (context.driver, context.wait)
    wait.until(EC.presence_of_element_located(PayeeLocator.RAASTID_TEXT))
    DataStore.internal_raast_id = wait.until(EC.presence_of_element_located(PayeeLocator.RAASTID_VALUE)).text
    wait.until(EC.presence_of_element_located(PayeeLocator.BACK_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.TRANSACTIONS_TEXT)).click()

@step("I enter the internal RAAST ID")
def step_enter_internal_raast_id(context):
    wait = context.wait
    wait.until(EC.presence_of_element_located(PayeeLocator.RAAST_ID_INPUT))
    RAAST_ID = DataStore.internal_raast_id
    input_field = wait.until(EC.element_to_be_clickable(PayeeLocator.RAAST_ID_INPUT))
    input_field.send_keys(RAAST_ID)

@step("I tapped on the Fund Transfer button and selected HugoBank Account Details")
def step_tap_hugobank_account_details(context):
    wait = context.wait
    wait.until(EC.presence_of_element_located(PayeeLocator.FUNDTRANSFER_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.ADD_PAYEE_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.HUGOBANK_ACCOUNT_DETAILS_BUTTON)).click()

@step("I enter invalid HugoBank account number")
def step_enter_invalid_hugobank_account_number(context):
    wait = context.wait
    account_number = Testing.generate_random_number('11', 8)
    acc_field = wait.until(EC.element_to_be_clickable(PayeeLocator.ACCOUNT_INPUT_FIELD))
    acc_field.clear()
    acc_field.send_keys(account_number)

@step("I clear the internal account number field")
def step_clear_internal_account_number(context):
    context.wait.until(EC.element_to_be_clickable(PayeeLocator.ACCOUNT_INPUT_FIELD)).clear()

@step("I enter HugoBank account number")
def step_enter_hugobank_account_number(context):
    driver, wait = (context.driver, context.wait)
    account_number = DataStore.internal_account_number
    input_field = wait.until(EC.element_to_be_clickable(PayeeLocator.ACCOUNT_INPUT_FIELD))
    input_field.clear()
    input_field.send_keys(account_number)

@step("I enter HugoBank IBAN number")
def step_enter_hugobank_iban_number(context):
    driver, wait = (context.driver, context.wait)
    IBAN_number = DataStore.internal_IBAN_number
    input_field = wait.until(EC.element_to_be_clickable(PayeeLocator.ACCOUNT_INPUT_FIELD))
    input_field.clear()
    input_field.send_keys(IBAN_number)

@step("I should see an error message Insufficient account balance")
def step_error_insufficient_balance(context):
    context.wait.until(EC.presence_of_element_located(PayeeLocator.INSUFFICIENT_ACCOUNT_BALANCE_TEXT))

@step("I should see an error message Reached the account transfer limit")
def step_error_reached_account_transfer_limit(context):
    context.wait.until(EC.presence_of_element_located(PayeeLocator.REACHED_ACCOUNT_TRANSFER_LIMIT_TEXT))

@step("I click on the back button")
def step_back_button(context):
    context.wait(EC.presence_of_element_located(PayeeLocator.BACK_BUTTON))

@step("I edit my other bank limit to ([^']*)")
def edit_other_bank_limit(context, amount):
    driver, wait = (context.driver, context.wait)
    wait.until(EC.presence_of_element_located(PayeeLocator.HOMESCREEN_PROFILE_ICON)).click()
    Transaction_limits_button = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        f'new UiScrollable(new UiSelector().scrollable(true))'
        f'.scrollIntoView(new UiSelector().resourceId("transactionLimitsTexts"))'
    )
    time_module.sleep(3)
    wait.until(EC.visibility_of_element_located(Transaction_limits_button)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.TO_OTHER_BANK_ACCOUNT_TEXT))
    wait.until(EC.presence_of_element_located(PayeeLocator.LIMITS_EDIT_ICON)).click()

    limit_field = wait.until(EC.presence_of_element_located(PayeeLocator.OTHERBANK_LIMIT_BUTTON))
    limit_field.click()
    limit_field.clear()

    input_limit_field = wait.until(EC.presence_of_element_located(PayeeLocator.OTHERBANK_LIMIT_INPUT))
    input_limit_field.send_keys(amount)
    wait.until(EC.presence_of_element_located(PayeeLocator.TO_OTHER_BANK_ACCOUNT_TEXT)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.SAVE_BUTTON)).click()

    wait.until(EC.presence_of_element_located(PayeeLocator.ENTER_PASSCODE_TEXT))
    passcode_number = list('123456')
    actions = ActionChains(driver)
    for i in passcode_number:
        actions.send_keys(str(i)).perform()

    wait.until(EC.presence_of_element_located(PayeeLocator.GO_TO_DASHBOARD_BUTTON_LIMITS)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.BACK_BUTTON)).click()

    Non_prod_options_button = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        f'new UiScrollable(new UiSelector().scrollable(true))'
        f'.scrollIntoView(new UiSelector().resourceId("nonprodOptionsText"))'
    )

    wait.until(EC.presence_of_element_located(Non_prod_options_button)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.ACCOUNT_MANAGEMENT_ACTIVITIES_TEXT)).click()
    for i in range(3):
        wait.until(EC.presence_of_element_located(PayeeLocator.REMOVE_COOL_OFF_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.NON_PROD_BACK_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.TRANSACTIONS_TEXT)).click()

@step("I edit my other HugoBank limit to ([^']*)")
def edit_other_hugobank_limit(context, amount):
    driver, wait = (context.driver, context.wait)
    wait.until(EC.presence_of_element_located(PayeeLocator.HOMESCREEN_PROFILE_ICON)).click()
    Transaction_limits_button = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        f'new UiScrollable(new UiSelector().scrollable(true))'
        f'.scrollIntoView(new UiSelector().resourceId("transactionLimitsTexts"))'
    )
    wait.until(EC.visibility_of_element_located(Transaction_limits_button)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.TO_OTHER_HUGOBANK_ACCOUNT_TEXT))
    wait.until(EC.presence_of_element_located(PayeeLocator.LIMITS_EDIT_ICON)).click()

    limit_field = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        f'new UiScrollable(new UiSelector().scrollable(true))'
        f'.scrollIntoView(new UiSelector().text("50,000").instance(3))'
    )
    limit_field = wait.until(EC.presence_of_element_located(limit_field))
    limit_field.click()
    limit_field.clear()

    input_limit_field = wait.until(EC.presence_of_element_located(PayeeLocator.OTHER_HUGOBANK_LIMIT_INPUT))
    input_limit_field.send_keys(amount)
    wait.until(EC.presence_of_element_located(PayeeLocator.TO_OTHER_HUGOBANK_ACCOUNT_TEXT)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.SAVE_BUTTON)).click()

    wait.until(EC.presence_of_element_located(PayeeLocator.ENTER_PASSCODE_TEXT))
    passcode_number = list('123456')
    actions = ActionChains(driver)
    for i in passcode_number:
        actions.send_keys(str(i)).perform()

    wait.until(EC.presence_of_element_located(PayeeLocator.GO_TO_DASHBOARD_BUTTON_LIMITS)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.BACK_BUTTON)).click()

    Non_prod_options_button = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        f'new UiScrollable(new UiSelector().scrollable(true))'
        f'.scrollIntoView(new UiSelector().resourceId("nonprodOptionsText"))'
    )

    wait.until(EC.presence_of_element_located(Non_prod_options_button)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.ACCOUNT_MANAGEMENT_ACTIVITIES_TEXT)).click()

    for i in range(3):
        wait.until(EC.presence_of_element_located(PayeeLocator.REMOVE_COOL_OFF_BUTTON)).click()

    wait.until(EC.presence_of_element_located(PayeeLocator.NON_PROD_BACK_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.TRANSACTIONS_TEXT)).click()

@step("I select already added payee")
def select_payee(context):
    driver, wait = (context.driver, context.wait)
    wait.until(EC.presence_of_element_located(PayeeLocator.FUNDTRANSFER_TEXT))
    wait.until(EC.presence_of_element_located(PayeeLocator.FUNDTRANSFER_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.VIEW_PAYEE_BUTTON)).click()

@step("I click on the back button on the payee transaction screen")
def back_button(context):
    driver, wait = (context.driver, context.wait)
    wait.until(EC.presence_of_element_located(PayeeLocator.PAYEE_TRANSACTION_SCREEN_BACK_BUTTON)).click()

@step("I click on Create Payment Schedule button on the New Payee Screen")
def create_schedule(context):
    wait, driver = (context.wait, context.driver)
    wait.until(EC.presence_of_element_located(PayeeLocator.RIGHT_ICON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.CREATE_PAYMENT_SCHEDULE_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.SCHEDULE_PREVIEW))

@step("I verify the new schedule is displayed on Payee Screen")
def verify_new_schedule(context):
    wait, driver = (context.wait, context.driver)
    schedule = context.schedule_details

    wait.until(EC.presence_of_element_located(PayeeLocator.SCHEDULE_PAYMENT_PAYEE_SCREEN))
    wait.until(EC.presence_of_element_located(PayeeLocator.FUND_TRANSFER_TEXT_ON_NEW_SCHEDULE))

    amount_element = wait.until(EC.presence_of_element_located(PayeeLocator.CURRENCY_TEXT_ON_NEW_SCHEDULE))
    frequency_element = wait.until(EC.presence_of_element_located(PayeeLocator.FREQUENCY_SELECTION_ON_NEW_SCHEDULE))
    start_date_element = wait.until(EC.presence_of_element_located(PayeeLocator.START_DATE_ON_NEW_SCHEDULE))

    IST = pytz.timezone("Asia/Kolkata")

    cutoff_time = time(17, 30, 0)
    IST_time = datetime.now(IST).time().replace(microsecond=0)

    assert str(schedule['amount']) in amount_element.text
    assert schedule['frequency'].capitalize() in frequency_element.text

    schedule_date = schedule['start_date'].strftime("%a, %d %b")

    if cutoff_time < IST_time:
        schedule_date = (schedule['start_date'] + timedelta(days=1)).strftime("%a, %d %b")

    assert str(schedule_date) in start_date_element.text

@then("I verify the edited schedule is displayed on Payee Screen")
def verify_schedule(context):
    wait = context.wait
    schedule = context.schedule_details
    amount_element = wait.until(EC.presence_of_element_located(PayeeLocator.CURRENCY_TEXT_ON_NEW_SCHEDULE))
    frequency_element = wait.until(EC.presence_of_element_located(PayeeLocator.FREQUENCY_SELECTION_ON_NEW_SCHEDULE))
    assert str(schedule["amount"]) in amount_element.text
    assert schedule["frequency"].capitalize() in frequency_element.text

@step("I delete the payment schedule")
def delete_payment_schedule(context):
    wait, driver = (context.wait, context.driver)
    wait.until(EC.presence_of_element_located(PayeeLocator.SCHEDULE_PAYMENT_PAYEE_SCREEN))
    wait.until(EC.presence_of_element_located(PayeeLocator.FUND_TRANSFER_TEXT_ON_NEW_SCHEDULE)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.VIEW_SCHEDULE_TEXT))
    wait.until(EC.presence_of_element_located(PayeeLocator.SCHEDULE_DELETION_MENU)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.DELETE_SCHEDULE_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.SCHEDULE_YES)).click()

@step("I verify that the payment schedule has been deleted successfully")
def verify_delete_payment_schedule(context):
    wait, driver = (context.wait, context.driver)
    wait.until(EC.presence_of_element_located(PayeeLocator.SCHEDULE_DELETED_SUCCESSFULLY_TEXT))
    wait.until(EC.presence_of_element_located(PayeeLocator.RIGHT_ICON)).click()
    create_schedule_button = wait.until(EC.presence_of_element_located(PayeeLocator.CREATE_PAYMENT_SCHEDULE_BUTTON))
    assert create_schedule_button.is_enabled()

@step("I verify stopping the payment schedule")
def verify_stop_payment_schedule(context):
    wait, driver = (context.wait, context.driver)
    wait.until(EC.presence_of_element_located(PayeeLocator.FUND_TRANSFER_TEXT_ON_NEW_SCHEDULE)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.STOP_SCHEDULE_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.SCHEDULE_YES)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.SCHEDULE_STOPPED_TEXT))

@step("I verify Resuming the payment Schedule")
def verify_resume_payment_schedule(context):
    wait, driver = (context.wait, context.driver)
    wait.until(EC.presence_of_element_located(PayeeLocator.RESUME_SCHEDULE_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.SCHEDULE_ACTIVE_TEXT))

@step("I verify that the schedule is ([^']*) and amount ([^']*) is settled on the payee screen")
def verify_schedule_triggered(context, schedule_text, amount):
    wait, driver = (context.wait, context.driver)
    wait.until(EC.visibility_of_element_located(PayeeLocator.HOMESCREEN_PROFILE_ICON))
    fund_transfer = wait.until(EC.visibility_of_element_located(PayeeLocator.FUNDTRANSFER_BUTTON))
    wait.until(EC.element_to_be_clickable(PayeeLocator.FUNDTRANSFER_BUTTON))
    fund_transfer.click()
    wait.until(EC.presence_of_element_located(PayeeLocator.VIEW_PAYEE_BUTTON)).click()
    pull_to_refresh_from_middle(driver,3)
    wait.until(EC.presence_of_element_located(PayeeLocator.SCHEDULE_PAY_PAYEE_TEXT)).click()
    settled_text = wait.until(EC.presence_of_element_located(PayeeLocator.SETTLED_TEXT))
    assert "Settled" in settled_text.text

@step("I verify that the schedule is not triggered")
def verify_schedule_not_triggered(context):
    wait, driver = (context.wait, context.driver)
    wait.until(EC.visibility_of_element_located(PayeeLocator.HOMESCREEN_PROFILE_ICON))
    fund_transfer = wait.until(EC.visibility_of_element_located(PayeeLocator.FUNDTRANSFER_BUTTON))
    wait.until(EC.element_to_be_clickable(PayeeLocator.FUNDTRANSFER_BUTTON))
    fund_transfer.click()
    wait.until(EC.presence_of_element_located(PayeeLocator.VIEW_PAYEE_BUTTON)).click()
    pull_to_refresh_from_middle(driver, 3)
    wait.until_not(EC.presence_of_element_located(PayeeLocator.SCHEDULE_PAY_PAYEE_TEXT))

@step("I trigger the payment schedule using non-prod options")
def trigger_schedule_using_non_prod_options(context):
    wait, driver = (context.wait, context.driver)
    wait.until(EC.presence_of_element_located(PayeeLocator.HOMESCREEN_PROFILE_ICON)).click()

    Non_prod_options_button = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        f'new UiScrollable(new UiSelector().scrollable(true))'
        f'.scrollIntoView(new UiSelector().resourceId("nonprodOptionsText"))'
    )

    wait.until(EC.presence_of_element_located(Non_prod_options_button)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.SCHEDULE_TRIGGER_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.SCHEDULE_SELECT_TEXT)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.SCHEDULE_CURRENT_ACC_TEXT)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.SCHEDULE_DROPDOWN)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.SCHEDULE_PAYEE_TRIGGER)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.TICKLE_SCHEDULE_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.NON_PROD_BACK_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.TRANSACTIONS_TEXT)).click()

@step("I validate editing payee")
def validate_editing_payee(context):
    wait, driver = (context.wait, context.driver)
    wait.until(EC.presence_of_element_located(PayeeLocator.RIGHT_ICON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.EDIT_PAYEE_TEXT)).click()
    payee_nickname_input = wait.until(EC.presence_of_element_located(PayeeLocator.PAYEE_NICKNAME))
    payee_nickname_input.send_keys('haha')
    wait.until(EC.element_to_be_clickable(PayeeLocator.SAVE_TEXT)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.PAYEE_DETAILS_UPDATED_SUCCESSFULLY_TEXT))

@step("I validate deleting payee")
def validate_delete_payee(context):
    wait, driver = (context.wait, context.driver)
    wait.until(EC.presence_of_element_located(PayeeLocator.RIGHT_ICON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.DELETE_PAYEE)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.YES_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.PAYEE_DELETED_TEXT))

@step("I validate deleting payee with schedule")
def validate_delete_payee(context):
    wait, driver = (context.wait, context.driver)
    wait.until(EC.presence_of_element_located(PayeeLocator.RIGHT_ICON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.DELETE_PAYEE)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.YES_BUTTON)).click()
    wait.until(EC.presence_of_element_located(PayeeLocator.PAYEE_SCHEDULE_DELETED_TEXT))
