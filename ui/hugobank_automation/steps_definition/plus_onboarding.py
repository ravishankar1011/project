from behave import *
from selenium.webdriver.support import expected_conditions as EC
from behave import use_step_matcher
from tests.ui.hugobank_automation.pages.plus_onboarding_locators import plus_onboarding_locators
from tests.ui.hugobank_automation.pages.utils import Testing
import time
use_step_matcher("re")

@step('I click on unlock more')
def click_unlock_plus(context):
    wait, driver = context.wait, context.driver

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.UNLOCK_MORE)).click()

@step('I click upgrade to plus button')
def click_upgrade_to_plus(context):
    wait, driver = context.wait, context.driver

    wait.until(EC.presence_of_element_located(plus_onboarding_locators.COMPARE_TEXT))

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.UPGRADE_TO_PLUS)).click()

@step('I select Incoming PKR')
def select_incoming_range(context):
    wait, driver = context.wait, context.driver

    wait.until(EC.presence_of_element_located(plus_onboarding_locators.EXPECTED_TURNOVER_TEXT))

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.INCOMING_RANGE_DROPDOWN)).click()

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.INCOMING_PKR)).click()

@step('I select outgoing PKR')
def select_outgoing_range(context):
    wait, driver = context.wait, context.driver

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.OUTGOING_RANGE_DROPDOWN)).click()

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.RANGE_PKR)).click()

@step('I check dual declaration checkbox')
def check_dual_checkbox(context):
    wait, driver = context.wait, context.driver

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.DECLARATION_CHECKBOX)).click()

@step('I select I earn')
def select_i_earn(context):
    wait, driver = context.wait, context.driver

    wait.until(EC.presence_of_element_located(plus_onboarding_locators.SOURCE_OF_YOUR_INCOMING_FUNDS_TEXT))

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.I_EARN)).click()

@step('I select Income options')
def select_freelance(context):
    wait, driver = context.wait, context.driver

    driver.find_element(*Testing.get_scrollable_locator('Interest Income'))

    time.sleep(2)
    for locator in plus_onboarding_locators.SOURCE_OF_FUNDS_OPTIONS.values():
        wait.until(EC.element_to_be_clickable(locator)).click()

@step('I give details')
def give_details(context):
    wait, driver = context.wait, context.driver

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.OCCUPATION_DROPDOWN)).click()

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.ACCOUNTS_OPTION)).click()

    data = context.table[0]
    name = data['name']
    line1 = data['line1']
    line2 = data['Line2']
    city = data['city']
    postal_code = data['postal code']

    employer_name = wait.until(EC.presence_of_element_located(plus_onboarding_locators.NAME_OF_EMPLOYER))
    employer_name.click()
    employer_name.send_keys(name)

    wait.until(EC.presence_of_element_located(plus_onboarding_locators.LINE1)).send_keys(line1)

    wait.until(EC.presence_of_element_located(plus_onboarding_locators.LINE2)).send_keys(line2)

    driver.find_element(*Testing.get_scrollable_locator('Select province...'))
    wait.until(EC.presence_of_element_located(plus_onboarding_locators.CITY)).send_keys(city)

    wait.until(EC.presence_of_element_located(plus_onboarding_locators.POSTAL_CODE)).send_keys(postal_code)

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.PROVINCE)).click()

    wait.until(EC.presence_of_element_located(plus_onboarding_locators.PUNJAB)).click()

    wait.until(EC.presence_of_element_located(plus_onboarding_locators.CONTINUE_BUTTON)).click()

@Step('I choose Airline')
def choose_airline(context):
    wait, driver = context.wait, context.driver

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.OCCUPATION_DROPDOWN)).click()

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.AIRLINE_OPTION)).click()

@step('I should navigate to upload document screen')
def upload_screen(context):
    wait, driver = context.wait, context.driver

    wait.until(EC.visibility_of_element_located(plus_onboarding_locators.ELIGIBLE_DOCUMENTS_TEXT))

@step('I select Iam funded by sponsor')
def select_iam_funded(context):
    wait, driver = context.wait, context.driver

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.FUNDED_BY_SPONSOR)).click()

@step('I select unemployed')
def select_unemployed(context):
    wait, driver = context.wait, context.driver

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.UNEMPLOYED_OPTION)).click()

@step("I enter sponsor name ([^']*)")
def enter_sponsor_name(context, name: str):
    wait, driver = context.wait, context.driver

    sponsor_name = wait.until(EC.presence_of_element_located(plus_onboarding_locators.SPONSOR_NAME_FIELD))
    sponsor_name.click()
    sponsor_name.clear()
    sponsor_name.send_keys(name)

@step('I select relationship with sponsor')
def select_sponsor_relationship(context):
    wait, driver = context.wait, context.driver

    for _ in range(2):
        wait.until(EC.element_to_be_clickable(plus_onboarding_locators.SPONSOR_DROPDOWN)).click()

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.TEXT_SISTER)).click()

@step('I choose relationship with sponsor')
def select_sponsor_relationship(context):
    wait, driver = context.wait, context.driver

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.SPONSOR_DROPDOWN)).click()

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.TEXT_SISTER)).click()

@step("I clear sponsor name input")
def clear_sponsor_name(context):
    wait, driver = context.wait, context.driver

    wait.until(EC.presence_of_element_located(plus_onboarding_locators.SPONSOR_NAME_FIELD)).clear()

@step('I select source of income')
def select_income_salary(context):
    wait, driver = context.wait, context.driver

    selected_sources = ['FREELANCE', 'PENSION', 'INHERITANCE']
    for source in selected_sources:
        locator = plus_onboarding_locators.SOURCE_OF_FUNDS_OPTIONS[source]
        checkbox = wait.until(EC.element_to_be_clickable(locator))
        checkbox.click()

@step('I click back button')
def click_back_button(context):
    wait, driver = context.wait, context.driver

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.BACK_BUTTON)).click()

@step('The continue button is disabled in source of funds screen')
def check_continue_button(context):
    wait, driver = context.wait, context.driver

    wait.until(EC.presence_of_element_located(plus_onboarding_locators.SOURCE_OF_YOUR_INCOMING_FUNDS_TEXT))

    button = wait.until(EC.presence_of_element_located(plus_onboarding_locators.CONTINUE_BUTTON))
    assert button.get_attribute("enabled") == 'false', "Continue button is not disabled"

@step('I select student')
def select_student(context):
    wait, driver = context.wait, context.driver
    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.STUDENT_OPTION)).click()

@step('Error text should appear')
def enter_invalid_name_error(context):
    wait, driver = context.wait, context.driver
    wait.until(EC.presence_of_element_located(plus_onboarding_locators.ERROR_TEXT))

@step("I select source of incoming funds ([^']*)")
def select_income_sources(context, sources):
    wait, driver = context.wait, context.driver
    selected_sources = [s.strip().upper() for s in sources.split(',')]
    driver.find_element(*Testing.get_scrollable_locator('Interest Income'))
    time.sleep(1)
    for source in selected_sources:
        locator = plus_onboarding_locators.SOURCE_OF_FUNDS_OPTIONS[source]
        wait.until(EC.element_to_be_clickable(locator)).click()

@step('I give sponsor details then continue button should disable')
def give_details(context):
    wait, driver = context.wait, context.driver

    def check_continue_button_disabled():
        button = wait.until(EC.presence_of_element_located(plus_onboarding_locators.CONTINUE_BUTTON))
        assert button.get_attribute("enabled") == 'false', "Continue button is not disabled"

    for row in context.table:
        name = row['name']
        if name:
            name_field = wait.until(EC.presence_of_element_located(plus_onboarding_locators.NAME_OF_EMPLOYER))
            name_field.clear()
            name_field.send_keys(name)
            check_continue_button_disabled()
            name_field.clear()

        line1 = row['line1']
        if line1:
            line1_field = wait.until(EC.presence_of_element_located(plus_onboarding_locators.LINE1))
            line1_field.send_keys(line1)
            check_continue_button_disabled()
            wait.until(EC.presence_of_element_located(plus_onboarding_locators.LINE1_FIELD)).clear()

        line2 = row['Line2']
        if line2:
            line2_field = wait.until(EC.presence_of_element_located(plus_onboarding_locators.LINE2))
            line2_field.send_keys(line2)
            check_continue_button_disabled()
            wait.until(EC.presence_of_element_located(plus_onboarding_locators.LINE2_FIELD)).clear()

        driver.find_element(*Testing.get_scrollable_locator('Select province...'))
        city = row['city']
        if city:
            city_field = wait.until(EC.presence_of_element_located(plus_onboarding_locators.CITY))
            city_field.send_keys(city)
            check_continue_button_disabled()
            wait.until(EC.presence_of_element_located(plus_onboarding_locators.CITY_FIELD)).clear()

        postal_code = row['postal code']
        if postal_code:
            postal_code_field = wait.until(EC.presence_of_element_located(plus_onboarding_locators.POSTAL_CODE))
            postal_code_field.send_keys(postal_code)
            check_continue_button_disabled()

            wait.until(EC.presence_of_element_located(plus_onboarding_locators.POSTAL_CODE_FIELD)).clear()

            wait.until(EC.element_to_be_clickable(plus_onboarding_locators.PROVINCE)).click()

            wait.until(EC.presence_of_element_located(plus_onboarding_locators.PUNJAB)).click()

@step('I navigate to source of incoming funds screen')
def navigate_to_source(context):
    wait, driver = context.wait, context.driver

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.UNLOCK_MORE)).click()

    wait.until(EC.presence_of_element_located(plus_onboarding_locators.COMPARE_TEXT))

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.UPGRADE_TO_PLUS)).click()

    wait.until(EC.presence_of_element_located(plus_onboarding_locators.EXPECTED_TURNOVER_TEXT))

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.INCOMING_RANGE_DROPDOWN)).click()

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.INCOMING_PKR)).click()

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.OUTGOING_RANGE_DROPDOWN)).click()

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.RANGE_PKR)).click()

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.DECLARATION_CHECKBOX)).click()

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.CONTINUE_BUTTON)).click()

@Step('I click continue to upload documents')
def click_continue_to_upload_documents(context):
    wait, driver = context.wait, context.driver

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.CONFIRMATION_MODAL_FOR_UPLOAD_DOCUMENTS))

    wait.until(EC.element_to_be_clickable(plus_onboarding_locators.CONTINUE_BUTTON)).click()
