from behave import given, then, use_step_matcher
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from tests.ui.hugosave_automation.features.steps.data_class_parser import DataClassParser
from tests.ui.hugosave_automation.pages.payee_locators import PayeeLocators
from tests.ui.hugosave_automation.pages.util import Util
from tests.ui.hugosave_automation.steps_definition.data_class import PayeeDetails
import time
use_step_matcher("re")


@given(r"I tap on the Add Payee button on the ([^']*)")
def step_tap_add_payee(context,screen_name):
    add_payee_button = context.wait.until(EC.presence_of_element_located(PayeeLocators.ADD_PAYEE_BUTTON))
    add_payee_button.click()


@given(r"I wait for ([^']*) seconds")
def step_wait(context,seconds):
    print('waiting ',seconds, 'seconds')
    time.sleep(int(seconds))


@given(r'I enter Payee Name, Select Bank and Account Number')
def step_enter_payee_details(context):
    driver, wait = context.driver, context.wait

    payee_list = DataClassParser.parse_rows(context.table.rows, data_class= PayeeDetails)
    for row in payee_list:
        payee_name, bank_name, account_no = row.payee_name, row.bank_name, row.account_no
        if not hasattr(context, 'payee_details'):
            context.payee_details = {}
        if payee_name:
            payee_name_field = wait.until(EC.presence_of_element_located(PayeeLocators.PAYEE_NAME_INPUT_FIELD))
            payee_name_field.clear()
            payee_name_field.send_keys(payee_name)

        if bank_name:
            wait.until(EC.presence_of_element_located(PayeeLocators.BANK_NAME_FIELD)).click()
            time.sleep(2)
            Util.int_or_ext_payee(bank_name, driver)

        if account_no:
            Util.close_keyboard_if_shown(driver)
            account_no_field = wait.until(EC.presence_of_element_located(PayeeLocators.ACCOUNT_NUMBER_FIELD))
            account_no_field.clear(); account_no_field.send_keys(account_no)

        context.payee_details = {"payee_name":payee_name, "bank_name":bank_name, "account_no":account_no}


@then(r"I verify the payee name and validate the error message for invalid input")
def step_enter_user_details(context):
    Util.close_keyboard_if_shown(context.driver)
    if context.payee_details["payee_name"]:
        if Util.is_valid_payee_name(context.payee_details["payee_name"]):
            assert True
        else:
            context.wait.until(EC.presence_of_element_located(PayeeLocators.PAYEE_ERROR_MESSAGE))


@then(r"I verify the confirm button is ([^']*)")
def step_confirm_button_status(context,enabled_or_disabled ):
    wait = WebDriverWait(context.driver, 30)

    confirm_button = wait.until(EC.presence_of_element_located(PayeeLocators.CONFIRM_BUTTON))

    if enabled_or_disabled == "enabled":
         assert confirm_button.is_enabled(); f"Expected confirm button state to be enabled but got {confirm_button.is_enabled()}"
    elif enabled_or_disabled == "disabled":
        assert not confirm_button.is_enabled(); f"Expected confirm button state to be disabled but got {confirm_button.is_enabled()}"
    else:
        print("Invalid input, required 'enabled/disabled'")


@then('I tap on the back button on the Add New Payee screen')
def step_tap_back(context):
    context.wait.until(EC.element_to_be_clickable(PayeeLocators.BACK_BUTTON_ON_ADD_NEW_PAYEE)).click()


@then(r'I click on the confirm button')
def step_click_continue_button(context):
    context.wait.until(EC.presence_of_element_located(PayeeLocators.CONFIRM_BUTTON)).click()


@then(r'I verify that i reached the OTP Screen')
def step_payee_otp_screen(context):
    context.wait.until(EC.presence_of_element_located(PayeeLocators.OTP_SCREEN_TEXT))


@then(r"I enter the OTP ([^']*) to add payee")
def step_enter_otp(context, otp):
    otp_number = list(otp)
    actions = ActionChains(context.driver)
    for i in otp_number:  # Python range is exclusive of the end value.
        actions.send_keys(str(i)).perform()
    time.sleep(2)


@then(r'I tap on the Done button')
def step_tap_done_button(context):
    context.wait.until(EC.element_to_be_clickable(PayeeLocators.DONE_BUTTON)).click()


@then(r'I check for the error message for incorrect OTP while adding payee')
def step_check_for_error_message_for_incorrect_otp(context):
    otp_text = context.wait.until(EC.presence_of_element_located(PayeeLocators.INCORRECT_OTP_TEXT))
    assert otp_text.is_displayed(), f'otp text was not displayed'


@then(r"I wait for the 15-second timer to reach 0 and verify the presence of the Resend OTP button")
def step_verify_resend_button(context):
    wait = WebDriverWait(context.driver, 20)
    time.sleep(10)
    Util.close_keyboard_if_shown(context.driver)
    resend_otp_button = wait.until(EC.presence_of_element_located(PayeeLocators.RESEND_OTP_BUTTON))
    assert resend_otp_button.is_displayed(), f'resend otp button was not displayed';


@then('I tap on the back button on the Payee OTP screen')
def step_tap_back(context):
    context.wait.until(EC.element_to_be_clickable(PayeeLocators.BACK_BUTTON_ON_ADD_NEW_PAYEE)).click()


@then(r"I verify the payee's addition by checking the payee ([^']*) account number on the auto-directed payee individual screen")
def step_verify_payee_individual_screen(context, name):
    payee_account_no = context.wait.until(EC.presence_of_element_located(PayeeLocators.PAYEE_ACCOUNT_NUMBER_ON_PAYEE_SCREEN))
    assert payee_account_no.is_displayed(), f'payee account number was not displayed';
    assert payee_account_no.text==context.payee_details["account_no"],f'{payee_account_no.is_displayed()} payee account number not displayed'


@then(r'I tap on the back button on the payee individual screen')
def step_tap_back(context):
    context.wait.until(EC.element_to_be_clickable(PayeeLocators.BACK_BUTTON_ON_ADD_NEW_PAYEE)).click()


@then(r"I check if the newly added payee ([^']*) is appearing on the ([^']*)")
def step_payee_name(context,name,screen_name):
    payee_name = context.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{context.payee_details["payee_name"]}")')))
    assert payee_name.text == context.payee_details["payee_name"]


@then(r"I tap on the payee name ([^']*)")
def step_tap_payee_name(context,name):
    payee_name = context.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, f'{name[0]}, {name}')))
    payee_name.click()

@then(r"On the All Payees screen, I tap on the payee name ([^']*)")
def step_tap_payee_name(context,name):
    payee_name = context.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, f'{name[0]}')))
    payee_name.click()


@then(r'I tap on the See All text link on the Spend account dashboard')
def step_see(context):
    payee_name =  context.wait.until(EC.presence_of_all_elements_located(PayeeLocators.SEE_ALL_LINK))
    if payee_name:
        payee_name[0].click()
        payee_name[0].click()


@then(r'I verify that i reached the All Payees Screen')
def step_all_payees_screen(context):
    all_payees_text = WebDriverWait(context.driver, 20).until(EC.presence_of_element_located(PayeeLocators.ALL_PAYEES_TEXT))
    assert all_payees_text.is_displayed(), f'all payees text was not displayed';
    assert all_payees_text.text=='All Payees', f'all payees text was not as expected'


@then(r'I tap on the back button on the All Payees screen')
def step_tap_back(context):
    context.wait.until(EC.element_to_be_clickable(PayeeLocators.BACK_BUTTON_ON_ADD_NEW_PAYEE)).click()

@then(r"I click on the payee name ([^']*) on the Payee individual screen")
def step_tap_payee_name(context,name):
    context.wait.until(EC.presence_of_element_located(PayeeLocators.PAYEE_NAME)).click()


@then(r'I tap on the three vertical dots on the payee edit screen')
def step_tap_vertical_dots(context):
    context.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().className("com.horcrux.svg.SvgView").instance(4)'))).click()


@then(r'I click on the delete payee option')
def step_tap_delete_payee(context):
    context.wait.until(EC.presence_of_element_located(PayeeLocators.DELETE_TEXT)).click()


@then(r"I click on the Favourite icon")
def step_tap_favourite_icon(context):
    context.wait.until(EC.presence_of_element_located(PayeeLocators.FAVOURITE_ID)).click()


@then(r"I tap on the save button on the payee edit screen")
def step_tap_save(context ):
    context.wait.until(EC.presence_of_element_located(PayeeLocators.SAVE_BUTTON)).click()


@then(r"I verify if i auto-directed to the payee ([^']*) individual screen")
def step_verify_payee_individual_screen(context, name):
    payee_account_no = context.wait.until(EC.presence_of_element_located(PayeeLocators.PAYEE_ACCOUNT_NUMBER_ON_PAYEE_SCREEN))
    assert payee_account_no.text==context.payee_details["account_no"],f'payee account number is not as expected'


@then('I tap on the New Payment button on the payee individual screen')
def step_tap_new_payment(context):
    context.wait.until(EC.presence_of_element_located(PayeeLocators.NEW_PAYMENT_BUTTON)).click()


@then(r"I enter the payee amount ([^']*) on the New Payment screen")
def step_tap_transaction_activities_option(context,amount):
    context.wait.until(EC.element_to_be_clickable(PayeeLocators.PAYEMNT_INPUT_FIELD)).send_keys(amount)


@then("I select the reason chip on the ([^']*) payee New payment screen")
def step_select_reason_chip(context,name):
    context.wait.until(EC.presence_of_element_located(PayeeLocators.REASON_CHIP)).click()


@then(r"I tap on the Preview button on the New Payment screen")
def step_tap_preview_button(context):
    context.wait.until(EC.presence_of_element_located(PayeeLocators.PREVIEW_BUTTON)).click()


@then(r"I tap on the Pay button on the New Payment Preview screen")
def step_tap_pay_button(context):
    context.wait.until(EC.presence_of_element_located(PayeeLocators.PAY_BUTTON)).click()


@then("I click on the latest transaction record appears for the ([^']*) payee")
def step_verify_transaction_record(context, name):
    Util.pull_to_refresh(context.driver,3)
    context.wait.until(EC.presence_of_element_located(PayeeLocators.PAY_PAYEE_TEXT)).click()


@then("I verify the latest transaction is ([^']*) for the ([^']*) payee")
def step_verify_transaction_record(context, state, name):
    context.wait.until(EC.presence_of_element_located(PayeeLocators.PAYMENT_TEXT))
    Util.pull_to_refresh(context.driver,3)
    status = context.wait.until(EC.presence_of_element_located(PayeeLocators.TRANSACTION_STATUS))
    assert state in status.text, f"Expected 'Settled' in text but got '{status.text}'"
