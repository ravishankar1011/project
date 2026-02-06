from behave import *
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from tests.ui.hugobank_automation.pages.billsPaymentsLocators import BillsPaymentsLocators
from tests.ui.hugobank_automation.pages.homescreen_locators import Homescreen
from tests.ui.hugobank_automation.pages.non_prod_option_locators import *
from tests.ui.hugobank_automation.pages.savings_pot_locators import *
from tests.ui.hugobank_automation.features.steps.data_class_parser import *
from tests.ui.hugobank_automation.features.data_models.__dataclasses import *
from tests.ui.hugobank_automation.pages.utils import *
from datetime import datetime
import pytz

use_step_matcher("re")

IST = pytz.timezone("Asia/Kolkata")


@step('I navigate to the savings pot dashboard')
def step_pot_dashboard(context):
    driver, wait = context.driver, context.wait
    driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true))'
        '.scrollIntoView(new UiSelector().description("Explore"))'
    )
    time.sleep(2)
    wait.until(EC.presence_of_element_located(SavingsPotLocator.EXPLORE_BUTTON)).click()
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.SAVINGS_POT_LEARNING_DASHBOARD)).click()


@step('I create a new savings pot with the following details')
def step_create_pot(context):
    driver, wait = context.driver, context.wait
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.NEW_POT_ICON_BUTTON)).click()
    pot_list = DataClassParser.parse_rows(context.table.rows, data_class=PotDetails)
    if not hasattr(context, "pot_details"):
        context.pot_details = {}
    for pot in pot_list:
        if pot.pot_name and valid_pot_name(pot.pot_name):
            name_field = wait.until(EC.presence_of_element_located(SavingsPotLocator.POT_NAME_INPUT))
            name_field.clear()
            name_field.send_keys(pot.pot_name)
        else:
            raise ValueError(f"Invalid pot name: {pot.pot_name}")

        if pot.goal_amount:
            amount_field = wait.until(EC.presence_of_element_located(SavingsPotLocator.GOAL_AMOUNT_INPUT))
            amount_field.clear()
            amount_field.send_keys(pot.goal_amount)
        if pot.goal_date:
            if isinstance(pot.goal_date, datetime):
                goal_date = pot.goal_date
            else:
                goal_date = datetime.strptime(pot.goal_date, "%Y-%m-%d")
            date_str = goal_date.strftime("%d %B %Y")
            wait.until(EC.element_to_be_clickable(SavingsPotLocator.POT_GOAL_DATE_INPUT)).click()
            date_ele = wait.until(EC.element_to_be_clickable(
                (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().description("{date_str}")')
            ))
            date_ele.click()
            wait.until(EC.element_to_be_clickable(SavingsPotLocator.GOAL_DATE_OK)).click()
        context.pot_details[pot.pot_name] = {
            "pot_name": pot.pot_name,
            "goal_amount": pot.goal_amount,
            "goal_date": pot.goal_date
        }
        time.sleep(1)


@step(r'I complete the pot creation process by choosing "(I\'ll do it later|Yes, Add PKR 1)"')
def step_complete_creation(context, option: str):
    wait = context.wait
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.NEXT_BUTTON)).click()
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.CREATE_POT_BUTTON)).click()

    if option == "I'll do it later":
        wait.until(EC.element_to_be_clickable(SavingsPotLocator.ADD_MONEY_LATER_BUTTON)).click()
    elif option == "Yes, Add PKR 1":
        wait.until(EC.element_to_be_clickable(SavingsPotLocator.YES_ADD_PKR_BUTTON)).click()
        wait.until(EC.element_to_be_clickable(SavingsPotLocator.ADD_MONEY_BUTTON)).click()
    else:
        raise ValueError(f"Unknown option for pot creation process: {option}")


@step(r"the pot should show a current balance of ([^']*) PKR")
def step_verify_balance(context, amount):
    driver, wait = context.driver, context.wait
    expected_text = amount
    pull_to_refresh(driver, 5)
    wait.until(EC.text_to_be_present_in_element(SavingsPotLocator.DASHBOARD_CURRENCY_VALUE, expected_text))
    balance_ele = wait.until(EC.presence_of_element_located(SavingsPotLocator.DASHBOARD_CURRENCY_VALUE))
    balance = balance_ele.text.strip()
    assert balance == expected_text, f"Expected balance '{expected_text}', but got '{balance}'"  # additionao text


@step(r'I click on Schedule Dashboard')
def schedule_dashboard(context):
    wait = context.wait
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.POT_SCHEDULE_DASHBOARD)).click()


@step('I should see the new pot on the dashboard with correct details')
def step_verify_pot(context):
    driver, wait = context.driver, context.wait

    last_pot_name = list(context.pot_details.keys())[-1]
    details = context.pot_details[last_pot_name]

    pot_name_ele = wait.until(EC.presence_of_element_located(SavingsPotLocator.DASHBOARD_POT_NAME))
    assert pot_name_ele.text.strip() == details["pot_name"], \
        f"Expected pot name '{details['pot_name']}', got '{pot_name_ele.text.strip()}'"

    if details.get("goal_amount"):
        pot_goal_amount_ele = wait.until(EC.presence_of_element_located(SavingsPotLocator.DASHBOARD_CARD_CURRENCY))
        expected_amount = f"{float(details['goal_amount']):.2f}"
        assert expected_amount in pot_goal_amount_ele.text.strip(), \
            f"Expected amount '{expected_amount}', got '{pot_goal_amount_ele.text.strip()}'"

    if details.get("goal_date"):
        pot_goal_date_ele = wait.until(EC.presence_of_element_located(SavingsPotLocator.DASHBOARD_POT_GOAL_DATE))
        expected_date = details["goal_date"].strftime("%d %b '%y")
        ui_text = pot_goal_date_ele.text.strip()
        if ui_text.lower().startswith("goal date"):
            ui_text = ui_text.split(" ", 2)[-1]
        assert expected_date == ui_text, \
            f"Expected date '{expected_date}', got '{ui_text}'"


@step(r"I have deposited ([^']*) PKR into my account using non-prod options")
def deposit_amount_using_non_prod_options(context, amount):
    driver, wait = (context.driver, context.wait)
    wait.until(EC.element_to_be_clickable(NonProd.PROFILE_ICON_HOMESCREEN)).click()
    current_version_elem = driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true))'
        '.scrollIntoView(new UiSelector().descriptionContains("Current Version"))'
    )
    for _ in range(12):
        current_version_elem.click()
    wait.until(EC.element_to_be_clickable(NonProd.NON_PROD_OPTIONS_BUTTON)).click()
    wait.until(EC.element_to_be_clickable(NonProd.TRANSACTION_ACTIVITIES)).click()
    input_amount = wait.until(EC.presence_of_element_located(NonProd.INPUT_AMOUNT_FIELD))
    input_amount.clear()
    input_amount.send_keys(amount)
    wait.until(EC.element_to_be_clickable(NonProd.DEPOSIT_TO_YOUR_ACCOUNT_BUTTON)).click()
    wait.until(EC.element_to_be_clickable(NonProd.NON_PROD_BACK_BUTTON)).click()
    wait.until(EC.element_to_be_clickable(Homescreen.NOTIFICATIONS_BUTTON)).click()
    time.sleep(2)
    wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.CURRENT_ACCOUNT_CARD)).click()
    wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.HUGOBANK_ACCOUNT_DASHBOARD_BUTTON)).click()
    wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.ADD_MONEY_BUTTON))
    wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.BACK_BUTTON)).click()
    wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.HUGOBANK_ACCOUNT_DASHBOARD_BUTTON))
    wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.BACK_BUTTON)).click()
    wait.until(EC.element_to_be_clickable(BillsPaymentsLocators.CURRENT_ACCOUNT_CARD))
    pull_to_refresh(driver, n_times=3)



@step(r'I add ([\d.]+) PKR to the pot')
def step_add_money(context, amount):
    wait = context.wait
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.ADD_MONEY_TO_POT)).click()
    input_amount = wait.until(EC.presence_of_element_located(SavingsPotLocator.ENTER_PKR_AMOUNT))
    input_amount.clear()
    input_amount.send_keys(amount)
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.PREVIEW_BUTTON)).click()
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.ADD)).click()


@step(r'I click on "Edit Pot Name" and I enter a new pot name as "(.+)"')
def step_edit_and_update_pot(context, pot_name):
    wait = context.wait
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.EDIT_CLOSE_POT_MENU)).click()
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.EDIT_POT_BUTTON)).click()
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.EDIT_POT_ICON_BUTTON)).click()
    input_name = wait.until(EC.presence_of_element_located(SavingsPotLocator.EDIT_POT_INPUT_BUTTON))
    input_name.click()
    input_name.clear()
    input_name.send_keys(pot_name)
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.EDIT_POT_SAVE_BUTTON)).click()


@step('I verify that the pot name is updated to "(.+)"')
def step_verify_pot(context, pot_name):
    wait = context.wait
    expected_pot_name = pot_name
    wait.until(EC.text_to_be_present_in_element(SavingsPotLocator.DASHBOARD_POT_NAME, expected_pot_name))
    pot_name_ele = wait.until(EC.presence_of_element_located(SavingsPotLocator.DASHBOARD_POT_NAME))
    actual_pot_name = pot_name_ele.text.strip()
    assert actual_pot_name == expected_pot_name, f"Expected pot name : '{expected_pot_name}', but got '{actual_pot_name}'"


@step(r'I withdraw ([\d.]+) PKR from the pot')
def step_withdraw_amount(context, amount):
    wait = context.wait
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.WITHDRAW_BUTTON)).click()
    withdraw_amount = wait.until(EC.presence_of_element_located(SavingsPotLocator.ENTER_WITHDRAW_AMOUNT_BUTTON))
    withdraw_amount.clear()
    withdraw_amount.send_keys(amount)
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.PREVIEW_BUTTON)).click()
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.WITHDRAW_BUTTON)).click()


@step(r'I open the pot\'s options menu and select Close, then confirm with Yes')
def step_pot_menu(context):
    wait = context.wait
    options_menu = wait.until(EC.element_to_be_clickable(SavingsPotLocator.EDIT_CLOSE_POT_MENU))
    options_menu.click()
    close_btn = wait.until(EC.element_to_be_clickable(SavingsPotLocator.CLOSE_POT_BUTTON))
    close_btn.click()
    confirm_btn = wait.until(EC.element_to_be_clickable(SavingsPotLocator.YES_BUTTON))
    confirm_btn.click()
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.CLOSE_SAVINGS_POT_BUTTON)).click()


@step(r'the pot should appear in the Closed Pots section with name "([^"]*)"')
def step_verify_pot_close(context, pot_name):
    driver, wait = context.driver, context.wait
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.BACK_TO_SAVINGS_POT)).click()
    pull_to_refresh(driver)
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.VIEW_CLOSED_POTS)).click()
    pot_elem = driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        f'new UiScrollable(new UiSelector().scrollable(true))'
        f'.scrollIntoView(new UiSelector().descriptionContains("{pot_name}"))'
    )
    time.sleep(7)
    assert pot_elem.is_displayed(), f"Closed pot with name '{pot_name}' not found!"


@step('I create a new schedule with the following details')
def schedule_details(context):
    wait = context.wait
    schedule_list = DataClassParser.parse_rows(context.table.rows, data_class=Schedule)
    if not hasattr(context, "schedule_details"):
        context.schedule_details = {}
    for schedule in schedule_list:
        if schedule.frequency:
            freq_locator = frequency_map.get(schedule.frequency)
            if freq_locator:
                wait.until(EC.element_to_be_clickable(freq_locator)).click()
            else:
                continue

        if schedule.amount:
            if not schedule.bundle_schedule:
                amount_field = wait.until(
                    EC.presence_of_element_located(SavingsPotLocator.ENTER_SCHEDULE_AMOUNT_BUTTON)
                )
                amount_field.clear()
                amount_field.send_keys(str(schedule.amount))

        if schedule.start_date:
            if str(schedule.start_date).lower() == "today":
                start_date = datetime.today()
            elif isinstance(schedule.start_date, datetime):
                start_date = schedule.start_date
            else:
                try:
                    start_date = datetime.strptime(schedule.start_date, "%Y-%m-%d")
                except ValueError:
                    start_date = datetime.strptime(schedule.start_date, "%d %B %Y")
            date_str = start_date.strftime("%d %B %Y")
            wait.until(EC.element_to_be_clickable(SavingsPotLocator.SCHEDULE_START_DATE_BUTTON)).click()
            date_ele = wait.until(EC.element_to_be_clickable(
                (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().description("{date_str}")')
            ))
            date_ele.click()
            wait.until(EC.element_to_be_clickable(SavingsPotLocator.GOAL_DATE_OK)).click()

        if schedule.make_payment:
            dropdown = wait.until(
                EC.presence_of_element_located(SavingsPotLocator.MAKE_PAYMENT_DROPDOWN)
            )
            dropdown.click()
            payment_ele = payment_map.get(schedule.make_payment)
            if payment_ele:
                wait.until(EC.element_to_be_clickable(payment_ele)).click()

        preview_btn = wait.until(EC.presence_of_element_located(SavingsPotLocator.PREVIEW_BUTTON))
        if schedule.preview_button=='enabled':
            assert preview_btn.is_enabled()
        elif schedule.preview_button=='disabled':
            assert not preview_btn.is_enabled()

        if all([
            schedule.frequency,
            schedule.amount,
            schedule.start_date,
            schedule.make_payment,
            schedule.preview_button]):
            context.schedule_details = {
                "frequency": schedule.frequency,
                "amount": schedule.amount,
                "start_date": schedule.start_date,
                "make_payment": schedule.make_payment,
                "bundle": schedule.bundle_schedule
            }
            print("Schedule details:", context.schedule_details)

    time.sleep(0.5)


@step('I edit the schedule with the following details')
def schedule_details(context):
    wait = context.wait
    schedule_list = DataClassParser.parse_rows(context.table.rows, data_class=Schedule)
    if not hasattr(context, "schedule_details"):
        context.schedule_details = {}
    for schedule in schedule_list:
        if schedule.frequency:
            freq_locator = frequency_map.get(schedule.frequency)
            if freq_locator:
                wait.until(EC.element_to_be_clickable(freq_locator)).click()
                context.schedule_details["frequency"] = schedule.frequency
            else:
                continue

        if schedule.amount:
            amount_field = wait.until(
                EC.presence_of_element_located(SavingsPotLocator.ENTER_SCHEDULE_AMOUNT_BUTTON)
            )
            amount_field.clear()
            amount_field.send_keys(str(schedule.amount))
            context.schedule_details["amount"] = schedule.amount

        if schedule.make_payment:
            dropdown = wait.until(
                EC.presence_of_element_located(SavingsPotLocator.MAKE_PAYMENT_DROPDOWN)
            )
            dropdown.click()
            payment_ele = payment_map.get(schedule.make_payment)
            if payment_ele:
                wait.until(EC.element_to_be_clickable(payment_ele)).click()
                context.schedule_details["make_payment"] = schedule.make_payment

        save_btn = wait.until(EC.presence_of_element_located(BillsPaymentsLocators.EDIT_SAVE_BUTTON))
        if schedule.save_button == 'enabled':
            assert save_btn.is_enabled()
        elif schedule.save_button == 'disabled':
            assert not save_btn.is_enabled()
    time.sleep(0.5)


@step("I confirm the Schedule")
def confirm_schedule(context):
    wait = context.wait
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.PREVIEW_BUTTON)).click()
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.CONFIRM_SCHEDULE)).click()


@step("I verify the new schedule is displayed in the savings pot dashboard")
def verify_schedule(context):
    wait = context.wait
    for schedule in context.schedule_details.values():
        amount_ele = wait.until(EC.presence_of_element_located(SavingsPotLocator.AMOUNT_SCHEDULE_DASHBOARD))
        freq_ele = wait.until(EC.presence_of_element_located(SavingsPotLocator.FREQUENCY_SCHEDULE_DASHBOARD))
        date_ele = wait.until(EC.presence_of_element_located(SavingsPotLocator.STARTING_DATE_SCHEDULE_DASHBOARD))
        assert str(schedule["amount"]) in amount_ele.text, \
            f"Amount mismatch! Expected: {schedule['amount']}, Found: {amount_ele.text}"
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


@step(r'I delete the schedule and confirm by selecting "(.*)"')
def delete_schedule(context, choice):
    wait = context.wait
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.POT_SCHEDULE_DASHBOARD)).click()
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.SCHEDULE_DELETE_MENU)).click()
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.DELETE_SCHEDULE)).click()

    if choice == "Yes":
        wait.until(EC.element_to_be_clickable(SavingsPotLocator.YES_BUTTON)).click()
    elif choice == "No":
        wait.until(EC.element_to_be_clickable(SavingsPotLocator.NO_BUTTON)).click()


@step(r'I verify that the schedule has been deleted')
def verify_schedule_deleted(context):
    wait = context.wait
    element = wait.until(EC.visibility_of_element_located(SavingsPotLocator.CREATE_SCHEDULE_BUTTON))
    actual_text = element.text.strip()
    expected_text = "Create Schedule"
    assert actual_text == expected_text, f"Expected text '{expected_text}' but got '{actual_text}'"


@step('I create a new savings pot with an invalid name "(.*)"')
def step_create_invalid_pot(context, pot_name):
    driver, wait = context.driver, context.wait
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.NEW_POT_ICON_BUTTON)).click()
    name_field = wait.until(EC.presence_of_element_located(SavingsPotLocator.POT_NAME_INPUT))
    name_field.clear()
    name_field.send_keys(pot_name)


@step('the warning "(.*)" should be displayed the Next button should be disabled')
def step_validate_warning_and_button(context, expected_message):
    driver, wait = context.driver, context.wait
    warning = wait.until(
        EC.visibility_of_element_located(SavingsPotLocator.CREATE_POT_NAME_WARNING)
    )
    actual_text = warning.text
    assert actual_text == expected_message, \
        f"Expected warning '{expected_message}' but got '{actual_text}'"
    next_btn = wait.until(EC.presence_of_element_located(SavingsPotLocator.NEXT_BUTTON))
    assert next_btn.get_attribute("enabled") == "false", "Next button should be disabled"


@step(r'I navigate to Homescreen')
def navigate_to_homescreen(context):
    wait = context.wait
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.GO_BACK_POT_HOME_BUTTON)).click()
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.POT_BACK_BUTTON)).click()


@step(r'I trigger the schedule using non-prod options')
def trigger_schedule(context):
    driver, wait = context.driver, context.wait
    wait.until(EC.element_to_be_clickable(NonProd.PROFILE_ICON_HOMESCREEN)).click()
    driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true))'
        '.scrollIntoView(new UiSelector().descriptionContains("NonProd Options"))'
    ).click()
    wait.until(EC.element_to_be_clickable(NonProd.SCHEDULE_ACTIVITIES)).click()
    wait.until(EC.element_to_be_clickable(NonProd.SELECT)).click()
    wait.until(EC.element_to_be_clickable(NonProd.CURRENT_ACCOUNT)).click()
    wait.until(EC.element_to_be_clickable(NonProd.SELECT)).click()
    wait.until(EC.element_to_be_clickable(NonProd.SCHEDULE_DROP_DOWN)).click()
    wait.until(EC.element_to_be_clickable(NonProd.TICKLE_SCHEDULE)).click()
    wait.until(EC.element_to_be_clickable(NonProd.NON_PROD_BACK_BUTTON)).click()
    wait.until(EC.element_to_be_clickable(Homescreen.NOTIFICATIONS_BUTTON)).click()
    pull_to_refresh(driver)


@step(r'I stop the schedule and confirm by clicking "(.*)"')
def stop_schedule(context, choice):
    wait = context.wait
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.POT_SCHEDULE_DASHBOARD)).click()
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.STOP)).click()
    if choice == "Yes":
        wait.until(EC.element_to_be_clickable(SavingsPotLocator.YES_BUTTON)).click()
    elif choice == "No":
        wait.until(EC.element_to_be_clickable(SavingsPotLocator.NO_BUTTON)).click()


@step(r'I verify that the schedule has been "(.*)"')
def verify_stop_schedule(context, expected_text: str):
    wait = context.wait
    try:
        element = wait.until(EC.presence_of_element_located(SavingsPotLocator.STOPPED))
        assert element.is_displayed(), f'Text "{expected_text}" is not visible on the screen'
    except NoSuchElementException:
        raise AssertionError(f'Text "{expected_text}" not found on the screen')


@step('I navigate to list of pots dashboard')
def navigate_to_list_of_pots(context):
    wait = context.wait
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.GO_BACK_POT_HOME_BUTTON)).click()


@step('I verify that "(.*)" text should appear')
def verify_pot_limit(context, expected_text):
    wait = context.wait
    try:
        element = wait.until(EC.presence_of_element_located(SavingsPotLocator.LIMIT_REACHED))
        assert element.is_displayed(), f'Text "{expected_text}"is not visible on the screen'
    except NoSuchElementException:
        raise AssertionError(f'Text "{expected_text}" not found on the screen')


@step(r'I cancel the pot creation by clicking "(.*)" and confirming with "(.*)"')
def cancel_pot_creation(context, cancel: str, confirm: str):
    wait = context.wait
    if cancel == "Cancel":
        wait.until(EC.element_to_be_clickable(SavingsPotLocator.CANCEL)).click()
    if confirm == "Yes":
        wait.until(EC.element_to_be_clickable(SavingsPotLocator.YES_BUTTON)).click()


@step(r'I Verify that navigated back to the savings pots dashboard')
def verify_back_to_dashboard(context):
    wait = context.wait
    element = wait.until(EC.presence_of_element_located(SavingsPotLocator.NEW_POT_NAME_BUTTON))
    assert element.text == "New Pot", f"Expected 'New Pot' button, but got '{element.text}'"


@step(r'I add ([\d.]+) PKR to the pot, then I should see "(.*)"')
def verify_amount_greater_than_curr_acc(context, amount, message):
    wait = context.wait
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.ADD_MONEY_TO_POT)).click()
    input_amount = wait.until(EC.presence_of_element_located(SavingsPotLocator.ENTER_PKR_AMOUNT))
    input_amount.clear()
    input_amount.send_keys(amount)
    insufficient_ele = wait.until(EC.presence_of_element_located(SavingsPotLocator.INSUFFICIENT_BALANCE))
    actual_text = insufficient_ele.text.strip()
    expected_text = message.strip()
    assert expected_text.lower() in actual_text.lower(), \
        f"Expected message '{expected_text}' not found in actual text '{actual_text}'"


@step(r'I click the Favourite icon to mark the pot as Favourite')
def fav_pot_select(context):
    wait = context.wait
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.DASHBOARD_FAV_POT)).click()


@step(r'the pot should appear in the list of Favourite pots on the dashboard')
def verify_pot_select(context):
    wait = context.wait
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.GO_BACK_POT_HOME_BUTTON)).click()
    fav_icon = wait.until(EC.presence_of_element_located(SavingsPotLocator.STAR_FILLED_ICON))
    assert fav_icon.is_displayed()


@step(r'I click the Favourite icon again to remove it from Favourite')
def unselect_fav_pot(context):
    wait = context.wait
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.POT_CLICK_BUTTON)).click()
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.DASHBOARD_FAV_POT)).click()


@step(r'The pot should no longer appear in the list of Favourite pots on the dashboard')
def verify_unselect_fav_pot(context):
    wait = context.wait
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.GO_BACK_POT_HOME_BUTTON)).click()
    time.sleep(2)
    result = wait.until(
        EC.invisibility_of_element_located(SavingsPotLocator.STAR_FILLED_ICON)
    )
    assert result, "Pot is still marked as Favourite"


@step(r'I Click on "(.*)" to activate the schedule')
def resume_schedule(context, option):
    wait = context.wait
    if option == "Resume":
        wait.until(EC.element_to_be_clickable(SavingsPotLocator.RESUME)).click()
        wait.until(EC.element_to_be_clickable(SavingsPotLocator.YES_BUTTON)).click()


@step(r'I Verify that the schedule has been Activated')
def verify_resume_schedule(context):
    wait = context.wait
    active_text = wait.until(EC.presence_of_element_located(SavingsPotLocator.ACTIVE))
    assert active_text.is_displayed()


@step(r'I verify that the schedule is triggered and amount ([\d.]+) is settled')
def verify_schedule_triggered(context, amount):
    wait, driver = context.wait, context.driver
    driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true))'
        '.scrollIntoView(new UiSelector().descriptionContains("Savings Pot"))'
    ).click()
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.POT_ONE_CLICK_BUTTON)).click()
    expected_text = amount
    pull_to_refresh(driver, 10)
    balance_ele = wait.until(EC.presence_of_element_located(SavingsPotLocator.DASHBOARD_CURRENCY_VALUE))
    balance = balance_ele.text.strip()
    assert balance == expected_text, f"Expected balance '{expected_text}', but got '{balance}'"


@step(r'I (.*) the scheduled amount as ([\d.]+) PKR')
def edit_schedule_amount(context, edit, amount):
    wait = context.wait
    wait.until(EC.element_to_be_clickable(SavingsPotLocator.POT_SCHEDULE_DASHBOARD)).click()
    edit_ele = wait.until(EC.element_to_be_clickable(SavingsPotLocator.EDIT_SCHEDULE)).click()
    if edit_ele == edit:
        edit_ele.click()
    edit_amount_input = wait.until(EC.presence_of_element_located(SavingsPotLocator.EDIT_SCHEDULE_AMOUNT))
    edit_amount_input.clear()
    edit_amount_input.send_keys(amount)


@step(r'I verify that schedule amount snap back to (.*)')
def verify_edit_schedule_amount(context, amount):
    wait = context.wait
    edit_ele = wait.until(EC.presence_of_element_located(SavingsPotLocator.EDIT_SCHEDULE_AMOUNT))
    edit_ele = edit_ele.text
    assert edit_ele.strip() == amount.strip()
