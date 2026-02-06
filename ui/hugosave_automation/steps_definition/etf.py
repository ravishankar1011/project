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
from tests.ui.hugosave_automation.pages.home_screen_locators import HomeScreen
from tests.ui.hugosave_automation.pages.etfs_locators import ETFs
from behave import *
import re
from tests.ui.hugosave_automation.pages import metals_locators
use_step_matcher("re")

@when(u'I complete investment personality quiz from the homescreen')
def completes_quiz(context):

    driver,wait = (context.driver, context.wait)

    #wait.until(EC.element_to_be_clickable(NonProd.PROFILE_ICON_HOMESCREEN)).click()

    driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true).instance(0))'
        '.setAsVerticalList()'
        '.scrollIntoView(new UiSelector().resourceId("defaultQuizButtonTestId"));'
    )

    wait.until(EC.element_to_be_clickable(ETFs.QUIZ_LINK_ON_THE_HOMESCREEN)).click()

    wait.until(EC.element_to_be_clickable(ETFs.START_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(ETFs.PRO_OPTION)).click()

    wait.until(EC.element_to_be_clickable(ETFs.NEXT_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(ETFs.FIVE_YEARS_OR_MORE)).click()

    wait.until(EC.element_to_be_clickable(ETFs.NEXT_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(ETFs.TO_GROW_MONEY_AGGRESSIVELY)).click()

    wait.until(EC.element_to_be_clickable(ETFs.NEXT_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(ETFs.BUY_MORE)).click()

    wait.until(EC.element_to_be_clickable(ETFs.NEXT_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(ETFs.A_LARGE_LOSS)).click()

    wait.until(EC.element_to_be_clickable(ETFs.GET_RESULTS_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(ETFs.BACK_TO_HOME_BUTTON)).click()

@when(u'I move to the mmf dashboard from the homescreen')
def move_to_mmf_dashboard(context):

    driver,wait = (context.driver, context.wait)

    wait.until(EC.element_to_be_clickable(ETFs.SCROLL_TO_EXPLORE_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(ETFs.ETFS_DASHBOARD_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(ETFs.MMF_GET_STARTED_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(ETFs.MMF_DASHBOARD_BUTTON_ON_LEARNING_SCREEN)).click()

@when(u'I move to the cautious dashboard from the homescreen')
def move_to_cautious_dashboard(context):

    driver,wait = (context.driver, context.wait)

    wait.until(EC.element_to_be_clickable(ETFs.SCROLL_TO_EXPLORE_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(ETFs.ETFS_DASHBOARD_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(ETFs.CAUTIOUS_GET_STARTED_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(ETFs.CAUTIOUS_DASHBOARD_BUTTON)).click()

@when(u'I move to the balanced dashboard from the homescreen')
def move_to_balanced_dashboard(context):

    driver,wait = (context.driver, context.wait)

    wait.until(EC.element_to_be_clickable(ETFs.SCROLL_TO_EXPLORE_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(ETFs.ETFS_DASHBOARD_BUTTON)).click()

    driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true).instance(0))'
        '.setAsVerticalList()'
        '.scrollIntoView(new UiSelector().resourceId("initialCardBtnBalanced"));'
    )

    wait.until(EC.element_to_be_clickable(ETFs.BALANCED_GET_STARTED_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(ETFs.BALANCED_DASHBOARD_BUTTON)).click()

@when(u'I move to the growth dashboard from the homescreen')
def move_to_growth_dashboard(context):

    driver,wait = (context.driver, context.wait)

    wait.until(EC.element_to_be_clickable(ETFs.SCROLL_TO_EXPLORE_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(ETFs.ETFS_DASHBOARD_BUTTON)).click()

    driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true).instance(0))'
        '.setAsVerticalList()'
        '.scrollIntoView(new UiSelector().resourceId("initialCardBtnGrowth"));'
    )

    wait.until(EC.element_to_be_clickable(ETFs.GROWTH_GET_STARTED_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(ETFs.GROWTH_DASHBOARD_BUTTON)).click()




















