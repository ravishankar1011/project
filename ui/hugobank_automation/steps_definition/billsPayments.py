from behave import given, when, then, step_matcher
from selenium.webdriver.support.ui import WebDriverWait
from tests.ui.hugobank_automation.pages.utils import *
from tests.ui.hugobank_automation.pages.billsPaymentsLocators import *
from behave import use_step_matcher
from selenium.webdriver.common.action_chains import ActionChains
import pytz
from datetime import datetime, timedelta
IST = pytz.timezone('Asia/Kolkata')
use_step_matcher("re")


@given(u"I tap on the Bills & Recharges and select the ([^']*)")
def step_select_category(context, category):
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.BILLS_AND_RECHARGES)).click()
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.NEW_PAYMENT_ICON)).click()
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.RECHARGE_TEXT))
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.UTILITY_BILLS_TEXT))
    if category in BillsPaymentsLocators.CATEGORY_LIST:
        context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.CATEGORY_LIST[category]['locator'])).click()
        context.bill_category = category
    else:
        raise NotImplementedError


@when(u"I select the ([^']*) operator and tap on the Add Consumer card")
def step_select_operator(context, operator):
    category = context.bill_category
    context.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Mobilink Prepaid")')))
    if operator in BillsPaymentsLocators.CATEGORY_LIST[category]:
        element = context.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().description("{BillsPaymentsLocators.CATEGORY_LIST[category][operator]}"))'
        )
        element.click()
        context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.ADD_CONSUMER)).click()
        context.bill_operator = operator
    else:
        raise NotImplementedError


@when(u"I tap on the back button")
def tap_back_button(context):
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.BACK_BUTTON_OPERATOR_SCREEN)).click()


@when(u"I enter the mobile number ([^']*)")
def enter_number(context, mobile_number ):
    input_field = context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.INPUT_FIELD))
    input_field.clear()
    input_field.send_keys(mobile_number)
    context.biller_number = mobile_number


@then(u"I tap on the Cancel button")
def tap_cancel_button(context):
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.CANCEL_BUTTON)).click()


@then(u'I tap on the Confirm button')
def tap_confirm_button(context):
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.CONFIRM_BUTTON)).click()


@then(u"the confirm button should be ([^']*)")
def button_state(context, button_state):
        otp_button = context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.CONFIRM_BUTTON))
        if button_state == 'enabled':
            assert otp_button.is_enabled()
        elif button_state == 'disabled':
            assert not otp_button.is_enabled()
        else:
            raise NotImplementedError


@then(u"I should see the error message \"([^']*)\"")
def check_error_message(context, error_message):
    error_msg = context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.INVALID_ID_MESSAGE))
    assert error_msg.text == error_message, f'expected error message = "{error_msg} but got {error_msg.text}"'


@then(u'I enter the biller nickname and validate the \'Get OTP\' button')
def enter_biller_name(context):
    for row in context.table:
        nickname, button_state = row['Name'], row['Button state']
        nick_name = context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.NICK_NAME_FIELD))
        nick_name.clear()
        nick_name.send_keys(nickname)
        time.sleep(2)
        otp_button = context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.GET_OTP))
        if button_state == 'enabled':
            assert otp_button.is_enabled()
            context.biller_name = nick_name
        elif button_state == 'disabled':
            assert not otp_button.is_enabled()
        else:
            raise NotImplementedError


@when(u'I tap on the Get OTP button')
def tap_otp_button(context):
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.GET_OTP)).click()


@then(u'I navigate to the OTP screen, enter the OTPs, and verify the error messages')
def otp_verify(context):
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.OTP_TEXT)).click()
    for row in context.table:
        actions = ActionChains(context.driver)
        for i in row['OTP']:
            actions.send_keys(str(i)).perform()
        incorrect_otp = context.wait.until(
            EC.presence_of_element_located(BillsPaymentsLocators.INCORRECT_OTP_MESSAGE))
        assert row['Error message'] in incorrect_otp.text, f'expected error message = "{row["Error message"]} but got {incorrect_otp.text}'


@then(u"I tap on the \'Go to Bill\' and verify the biller name ([^']*) on the individual biller screen")
def verify_name(context, name):
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.GO_TO_BILL)).click()
    context.wait.until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{name} ")')))


@then(u"the \'Get OTP\' button should be ([^']*)")
def button_state(context, state):
    otp_button = context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.GET_OTP))
    if state == 'enabled':
        assert otp_button.is_enabled()
    elif state == 'disabled':
        assert not otp_button.is_enabled()
    else:
        raise NotImplementedError


@when(u"I provide the OTP ([^']*)")
def enter_otp(context, otp):
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.OTP_TEXT))
    otp_number = list(otp)
    actions = ActionChains(context.driver)
    for i in otp_number:  # Python range is exclusive of the end value.
        actions.send_keys(str(i)).perform()
    time.sleep(2)


@then(u'I navigate to the passcode screen, enter invalid passcodes, and verify the error messages')
def passcode_error_msg(context):
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.PASSCODE_TEXT))
    for row in context.table:
        actions = ActionChains(context.driver)
        for i in row['Passcode']:
            actions.send_keys(str(i)).perform()
        incorrect_passcode = context.wait.until(
            EC.presence_of_element_located(BillsPaymentsLocators.INCORRECT_PASSCODE_MESSAGE))
        assert incorrect_passcode.text == row['Error message'], f'expected error message = "{row["Error message"]} but got {incorrect_passcode.text}'


@then(u"I verify the biller name ([^']*) on the individual biller screen")
def verify_name(context, name):
    print(context.bill_operator)
    if 'prepaid' in context.bill_operator:
        context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.TOP_UP_BUTTON))
    elif 'Bundle' in context.bill_operator:
        context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.SELECT_BUNDLE_BUTTON))
    context.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{name} ")')))


@then(u'I verify the biller card on the bill operator screen')
def verify_biller_card(context):
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.BACK_BUTTON)).click()
    for row in context.table:
        context.wait.until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{row["Name"]}")')))
        context.wait.until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("Consumer ID - {row["consumer number"]}")')))


@then(u'I tap on the Add Consumer card')
def tap_consumer_button(context):
    time.sleep(3)
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.ADD_CONSUMER)).click()


@then(u'I should see the error message for adding an existing biller')
def error_msg(context):
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.EXITED_BILLER_ERROR))


@when(u"I tap on the \"Edit Details\" option and verify the biller details")
def tap_edit_button(context):
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.EDIT_BUTTON)).click()
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.EDIT_DETAILS)).click()
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.MOBILE_NUMBER_TEXT))
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.SERVICE_OPERATOR_TEXT))
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.ADD_NICKNAME_TEXT))
    for row in context.table:
        context.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{row["Mobile Number"]}")')))
        context.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{row["Service Operator"]}")')))
        context.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{row["Nickname"]}")')))


@then(u"I navigate to the create schedule screen")
def go_to_schedule(context):
# need locators to tap on the create schedule button
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.CREATE_SCHEDULE_TEXT))
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.TOP_UP_BUTTON)).click()


@then(u"I delete the ([^']*) biller and verify if it is deleted")
def delete_biller(context, name):
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.EDIT_BUTTON)).click()
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.DELETE_CONSUMER)).click()
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.DELETE_BUTTON)).click()
    WebDriverWait(context.driver,30).until_not(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{name}")')))


@then(u"I update the biller nickname to ([^']*)")
def update_name(context, name):
    input_field = context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.INPUT_FIELD))
    input_field.clear()
    input_field.send_keys(name)
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.SAVE_BUTTON)).click()


@when(u"I select the ([^']*) operator and enter the mobile number ([^']*)")
def step_select_operator(context, operator, mobile_number):
    category = context.bill_category
    context.wait.until(EC.presence_of_element_located(
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Mobilink Prepaid")')))
    if operator in BillsPaymentsLocators.CATEGORY_LIST[category]:
        element = context.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().description("{BillsPaymentsLocators.CATEGORY_LIST[category][operator]}"))'
        )
        element.click()
        context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.ADD_CONSUMER)).click()
        input_field = context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.INPUT_FIELD))
        input_field.clear()
        input_field.send_keys(mobile_number)
        context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.CONFIRM_BUTTON)).click()
        context.bill_operator = operator
        context.biller_number = mobile_number
    else:
        raise NotImplementedError


@then(u"I provide the OTP ([^']*) and the passcode ([^']*)")
def enter_otp_passcode(context, otp, passcode):
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.GET_OTP)).click()
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.OTP_TEXT)).click()
    otp_number = list(otp)
    actions = ActionChains(context.driver)
    for i in otp_number:  # Python range is exclusive of the end value.
        actions.send_keys(str(i)).perform()
    time.sleep(2)
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.PASSCODE_TEXT))
    actions = ActionChains(context.driver)
    for i in passcode:
        actions.send_keys(str(i)).perform()


@then(u"I navigate to the New Payment screen and verify the input field")
def verify_input_field(context):
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.TOP_UP_BUTTON)).click()
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.NEW_PAYMENT_TEXT))
    for row in context.table:
        input_field = context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.INPUT_FIELD))
        input_field.clear()
        input_field.send_keys(row['Amount'])
        button = context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.PROCEED_BUTTON))
        if row['Proceed button state'] == 'enabled':
            assert button.is_enabled(), f'expected button is enabled=true, but was {button.is_enabled()}'
        elif row['Proceed button state'] == 'disabled':
            assert not button.is_enabled(), f'expected button is disabled=false, but was {button.is_enabled()}'
        else:
            assert False, f'expected button is enabled or disabled, but was {row["Proceed button state"]}'


@then(u"I enter the amount ([^']*) and verify the error message \'Insufficient account balance\'")
def verify_error_msg(context, amount):
    input_field = context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.INPUT_FIELD))
    input_field.clear()
    input_field.send_keys(amount)
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.INSUFFICIENT_BALANCE_TEXT))


@then(u"I tap on the Cancel button and re-visit the new payment screen")
def tap_cancel_button(context):
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.CANCEL_BUTTON)).click()
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.TOP_UP_BUTTON)).click()
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.NEW_PAYMENT_TEXT))


@then(u"I enter the amount ([^']*) and navigate to the preview screen")
def enter_amount(context, amount):
    input_field = context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.INPUT_FIELD))
    input_field.clear()
    input_field.send_keys(amount)
    time.sleep(2)
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.PROCEED_BUTTON)).click()
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.PREVIEW_TEXT))
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.PAY))


@then("I click on the ([^']*) button")
def tap_top_up_button(context, button):
    if button == 'Top-up':
        context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.TOP_UP_BUTTON)).click()
    elif button == 'Pay':
        context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.PAY_BUTTON)).click()
    elif button == 'Select Bundle':
        context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.SELECT_BUNDLE_BUTTON)).click()
        context.wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{context.bill_operator}")'))).click()


@when(u"I enter the amount ([^']*)")
def enter_amount(context, amount):
    input_field = context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.INPUT_FIELD))
    input_field.clear()
    input_field.send_keys(amount)
    time.sleep(2)
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.PROCEED_BUTTON)).click()
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.PREVIEW_TEXT))
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.PAY)).click()


@then(u"I enter the amount ([^']*) and enter the passcode ([^']*)")
def enter_amount_passcode(context, amount, passcode):
    input_field = context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.INPUT_FIELD))
    input_field.clear()
    input_field.send_keys(amount)
    time.sleep(2)
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.PROCEED_BUTTON)).click()
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.PREVIEW_TEXT))
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.PAY)).click()
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.PASSCODE_TEXT))
    actions = ActionChains(context.driver)
    for i in passcode:
        actions.send_keys(str(i)).perform()

@then(u"I click the proceed, pay buttons and enter the passcode ([^']*)")
def enter_amount_passcode(context, passcode):
    context.wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("New Payment")'))).click()
    time.sleep(3)
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.PROCEED_BUTTON)).click()
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.PREVIEW_TEXT))
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.PAY)).click()
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.PASSCODE_TEXT))
    actions = ActionChains(context.driver)
    for i in passcode:
        actions.send_keys(str(i)).perform()


@then(u"I validate the transaction is ([^']*)")
def validate_transaction(context, state):
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.OUTGOING_PAYMENT))
    pull_to_refresh(context.driver,3)
    if state=='Settled':
        amount = context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.TRANSACTION_STATE))
        assert state in amount.text.strip(), f'amount is not settled {amount.text}'
    elif state=='Processing':
        amount = context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.TRANSACTION_STATE))
        assert state in amount.text.strip(), f'amount is not settled {amount.text}'
    else:
        assert False, f'Incorrect state has been given {state}'


@then(u"I enter invalid passcodes, and verify the error messages")
def verify_error_msg(context):
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.PASSCODE_TEXT))
    for row in context.table:
        actions = ActionChains(context.driver)
        for i in row['Passcode']:
            actions.send_keys(str(i)).perform()
        incorrect_passcode = context.wait.until(
            EC.presence_of_element_located(BillsPaymentsLocators.INCORRECT_PASSCODE_MESSAGE))
        assert incorrect_passcode.text == row['Error message'], f'expected error message = "{row["Error message"]} but got {incorrect_passcode.text}'


@then(u"I select the ([^']*) operator")
def select_operator(context, operator):
    category = context.bill_category
    if operator in BillsPaymentsLocators.CATEGORY_LIST[category]:
        element = context.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().description("{BillsPaymentsLocators.CATEGORY_LIST[category][operator]}"))')
        element.click()
    time.sleep(2)


@then(u"I enter the mobile number, name, otp and passcode")
def enter_biller_details(context):
    for row in context.table:
        context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.ADD_CONSUMER)).click()
        input_field = context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.INPUT_FIELD))
        input_field.clear()
        input_field.send_keys(row['Mobile Number'])
        time.sleep(2)
        context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.CONFIRM_BUTTON)).click()

        # enter the biller name
        nick_name = context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.NICK_NAME_FIELD))
        nick_name.clear()
        nick_name.send_keys(row['Nick name'])
        time.sleep(2)
        context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.GET_OTP)).click()

        # enter the otp
        context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.OTP_TEXT))
        otp_number = list(row["Otp"])
        actions = ActionChains(context.driver)
        for i in otp_number:  # Python range is exclusive of the end value.
            actions.send_keys(str(i)).perform()
        time.sleep(2)

        # enter the passcode
        context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.PASSCODE_TEXT))
        actions = ActionChains(context.driver)
        for i in row['Passcode']:
            actions.send_keys(str(i)).perform()
        context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.TOP_UP_BUTTON))
        context.wait.until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{row["Nick name"]} ")')))

        context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.BACK_BUTTON)).click()
        context.wait.until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{row["Nick name"]}")')))
        context.wait.until(
            EC.presence_of_element_located(
                (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("Consumer ID - {row["Mobile Number"]}")')))


@then(u"I check the 'Add consumer' button is in the ([^']*) state")
def check_button_state(context, button_state):
    add_consumer = context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.DISABLED_ADD_CONSUMER))
    if button_state == 'enabled':
        assert add_consumer.is_enabled()
    elif button_state == 'disabled':
        assert not add_consumer.is_enabled()
    else:
        raise NotImplementedError


@when(u"I navigate to the create schedule screen for the ([^']*) operator")
def go_to_schedule(context, operator_type):
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.EDIT_BUTTON)).click()
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.CREATE_PAYMENT_SCHEDULE)).click()
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.TEXT_WANT_TO_CREATE_SCHEDULE))
    if operator_type == 'Prepaid':
        context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.TOP_UP_SCHEDULE)).click()
    elif operator_type == 'Bundle':
        context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.BUNDLE_RECHARGE_SCHEDULE)).click()
        time.sleep(3)
        context.wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{context.bill_operator}")'))).click()


@when(u'I click the Preview button and Confirm button')
def go_to_preview(context):
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.PREVIEW_BUTTON)).click()
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.CONFIRM_SCHEDULE_BUTTON)).click()
    if 'Prepaid' in context.bill_operator:
        context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.TOP_UP_BUTTON))
    elif 'Bundle' in context.bill_operator:
        context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.SELECT_BUNDLE_BUTTON))


@then("I verify the newly created schedule is displayed in the biller dashboard")
def verify_schedule(context):
    wait = context.wait
    schedule = context.schedule_details
    print("biller dashboard:", context.schedule_details)

    if 'Prepaid' in context.bill_operator:
        amount_ele = wait.until(EC.presence_of_element_located(BillsPaymentsLocators.AMOUNT_SCHEDULE_DASHBOARD))
        assert str(schedule[ "amount"]) in amount_ele.text, f"Amount mismatch! Expected: {schedule['amount']}, Found: {amount_ele.text}"

    freq_ele = wait.until(EC.presence_of_element_located(BillsPaymentsLocators.FREQUENCY_SCHEDULE_DASHBOARD))
    date_ele = wait.until(EC.presence_of_element_located(BillsPaymentsLocators.STARTING_DATE_SCHEDULE_DASHBOARD))
    assert schedule["frequency"].capitalize() in freq_ele.text, \
        f"Frequency mismatch! Expected: {schedule['frequency']}, Found: {freq_ele.text}"

    now_ist = datetime.now(IST)
    cutoff_time = now_ist.replace(hour=17, minute=30, second=0, microsecond=0)
    schedule_date = schedule["start_date"]
    if isinstance(schedule_date, str):
        try:
            schedule_date = datetime.strptime(schedule_date, "%Y-%m-%d")
        except ValueError:
            schedule_date = datetime.strptime(schedule_date, "%d %B %Y")
    if schedule_date.date() == now_ist.date() and now_ist > cutoff_time:
        expected_dashboard_date = now_ist + timedelta(days=1)
    else:
        expected_dashboard_date = schedule_date
    expected_date_str = expected_dashboard_date.strftime("%d %b")
    match = re.search(r"\d{1,2} \w{3}", date_ele.text)
    dashboard_date_str = match.group(0) if match else date_ele.text
    assert expected_date_str == dashboard_date_str, \
        f"Start date mismatch! Expected: {expected_date_str}, Found: {dashboard_date_str}"


@when(u'I navigate to the edit schedule screen')
def go_to_schedule(context):
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.SCHEDULED_PAYMENT_TEXT)).click()
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.VIEW_SCHEDULE_TEXT))
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.SCHEDULE_EDIT_BUTTON)).click()
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.EDIT_SCHEDULE_TEXT))


@when(u'I click the Save button')
def go_to_preview(context):
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.EDIT_SAVE_BUTTON)).click()
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.VIEW_SCHEDULE_TEXT))
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.BACK_BUTTON)).click()
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.SCHEDULED_PAYMENT_TEXT))


@when(u'I stop the schedule')
def go_to_preview(context):
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.SCHEDULED_PAYMENT_TEXT)).click()
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.STOP_BUTTON)).click()
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.STOP_YES_BUTTON)).click()
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.RESUME_BUTTON))
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.BACK_BUTTON)).click()
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.RESUME_BUTTON_TEXT))


@when(u'I skip the schedule')
def go_to_preview(context):
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.SCHEDULED_PAYMENT_TEXT)).click()
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.SKIP_BUTTON)).click()
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.SKIP_YES_BUTTON)).click()
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.SKIPPED_TEXT))
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.BACK_BUTTON)).click()
    context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.NEXT_SCHEDULE_SKIPPED_TEXT))


@then("I verify the edited schedule details in the biller dashboard")
def verify_schedule(context):
    wait = context.wait
    schedule = context.schedule_details
    amount_ele = wait.until(EC.presence_of_element_located(BillsPaymentsLocators.AMOUNT_SCHEDULE_DASHBOARD))
    freq_ele = wait.until(EC.presence_of_element_located(BillsPaymentsLocators.FREQUENCY_SCHEDULE_DASHBOARD))
    assert str(schedule["amount"]) in amount_ele.text, \
        f"Amount mismatch! Expected: {schedule['amount']}, Found: {amount_ele.text}"
    assert schedule["frequency"].capitalize() in freq_ele.text, \
        f"Frequency mismatch! Expected: {schedule['frequency']}, Found: {freq_ele.text}"


@when(u'I navigate to the home screen')
def go_to_home_Screen(context):
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.BACK_BUTTON)).click()
    time.sleep(3)
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.BACK_BUTTON_OPERATOR_SCREEN)).click()
    time.sleep(3)
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.BACK_BUTTON_SERVICE_SCREEN)).click()
    time.sleep(3)
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.BACK_BUTTON_PAYMENT_CATEGORY_SCREEN)).click()
    time.sleep(3)
    context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.BACK_BUTTON_BILLS_AND_RECHARGES_SCREEN)).click()


@then(u'I navigate to the biller dashboard')
def go_to_biller_dashboard(context):
    for row in context.table:
        context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.BILLS_AND_RECHARGES)).click()
        context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.NEW_PAYMENT_ICON))
        time.sleep(3)
        context.wait.until(EC.element_to_be_clickable(
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{row["operator"]}")'))).click()
        context.wait.until(EC.element_to_be_clickable(
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{row["biller name"]}")'))).click()


@then(u"I verify the schedule transaction is ([^']*)")
def verify_schedule_transaction(context, schedule_tnx):
    pull_to_refresh(context.driver, 3)
    if schedule_tnx == 'Settled':
        context.wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.SCHEDULE_BILL_PAYMENTS_TEXT)).click()
        pull_to_refresh(context.driver, 3)
        amount = context.wait.until(EC.presence_of_element_located(BillsPaymentsLocators.TRANSACTION_STATE))
        assert schedule_tnx in amount.text.strip(), f'amount is not settled {amount.text}'
    elif schedule_tnx == 'not occurred':
        context.wait.until_not(EC.presence_of_element_located(BillsPaymentsLocators.SCHEDULE_BILL_PAYMENTS_TEXT))
    else:
        assert False, f'Incorrect state has been given {schedule_tnx}'
