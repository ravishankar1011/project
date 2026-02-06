from behave import *
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
import time
from tests.ui.hugosave_automation.pages.signup_locators import Signup
from tests.ui.hugosave_automation.pages.create_schedule_locators import CreateSchedule
from tests.ui.hugosave_automation.pages.non_prod_options_locators import NonProd
from tests.ui.hugosave_automation.pages.home_screen_locators import HomeScreen
from tests.ui.hugosave_automation.pages.util import Util
from tests.ui.hugosave_automation.steps_definition.data_class import *
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from behave import use_step_matcher
use_step_matcher("re")

@step("I create a schedule")
def create_schedule(context):
    driver, wait = (context.driver, context.wait)
    row = context.table[0]
    schedule = ScheduleData(
        frequency=row["Frequency"].strip(),
        week=row["Week"].strip() if row["Week"] else None,
        day=row["Day"].strip() if row["Day"] else None,
        amount=row["amount"]
    )
    freq = schedule.frequency.lower()
    if freq == "daily":
        wait.until(EC.element_to_be_clickable(CreateSchedule.AMOUNT_FIELD)).send_keys(schedule.amount)
    elif freq == "weekly":
        wait.until(EC.element_to_be_clickable(CreateSchedule.WEEKLY_RADIO_BUTTON)).click()
        wait.until(EC.element_to_be_clickable(CreateSchedule.AMOUNT_FIELD)).send_keys(schedule.amount)
        if schedule.day == "Mon":
            pass
        elif schedule.day == "Tue":
            wait.until(EC.element_to_be_clickable(CreateSchedule.TUESDAY_OPTION)).click()
        elif schedule.day == "Wed":
            wait.until(EC.element_to_be_clickable(CreateSchedule.WEDNESDAY_OPTION)).click()
        elif schedule.day == "Thu":
            wait.until(EC.element_to_be_clickable(CreateSchedule.THURSDAY_OPTION)).click()
        elif schedule.day == "Fri":
            wait.until(EC.element_to_be_clickable(CreateSchedule.FRIDAY_OPTION)).click()

    elif freq == "monthly":
        wait.until(EC.element_to_be_clickable(CreateSchedule.MONTHLY_RADIO_BUTTON)).click()
        wait.until(EC.element_to_be_clickable(CreateSchedule.AMOUNT_FIELD)).send_keys(schedule.amount)
        wait.until(EC.element_to_be_clickable(CreateSchedule.WEEK_DROPDOWN)).click()

        if schedule.week == "1st":
            wait.until(EC.element_to_be_clickable(CreateSchedule.FIRST_WEEK)).click()
        elif schedule.week == "2nd":
            wait.until(EC.element_to_be_clickable(CreateSchedule.SECOND_WEEK)).click()
        elif schedule.week == "3rd":
            wait.until(EC.element_to_be_clickable(CreateSchedule.THIRD_WEEK)).click()
        elif schedule.week == "4th":
            wait.until(EC.element_to_be_clickable(CreateSchedule.FOURTH_WEEK)).click()

        if schedule.day == "Mon":
            pass
        elif schedule.day == "Tue":
            wait.until(EC.element_to_be_clickable(CreateSchedule.TUESDAY_OPTION)).click()
        elif schedule.day == "Wed":
            wait.until(EC.element_to_be_clickable(CreateSchedule.WEDNESDAY_OPTION)).click()
        elif schedule.day == "Thu":
            wait.until(EC.element_to_be_clickable(CreateSchedule.THURSDAY_OPTION)).click()
        elif schedule.day == "Fri":
            wait.until(EC.element_to_be_clickable(CreateSchedule.FRIDAY_OPTION)).click()




