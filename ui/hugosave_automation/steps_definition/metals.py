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
from selenium.webdriver.support.ui import WebDriverWait
from tests.ui.hugosave_automation.pages.home_screen_locators import HomeScreen
from behave import *
import re
from tests.ui.hugosave_automation.pages import metals_locators
use_step_matcher("re")

@given(u'I move to the gold dashboard')
def move_to_the_gold(context):
    
    driver,wait = (context.driver, context.wait)

    wait.until(EC.element_to_be_clickable(GoldPage.SCROLL_TO_INVEST_EXPLORE_BUTTON)).click()
    
    wait.until(EC.element_to_be_clickable(GoldPage.PRECIOUS_METALS_DASHBOARD_BUTTON)).click()
    
    wait.until(EC.element_to_be_clickable(GoldPage.GOLD_GET_STARTED_BUTTON)).click()
    
    wait.until(EC.element_to_be_clickable(GoldPage.GOLD_DASHBOARD_BUTTON)).click()
    

@then(u'I validate buy and sell buttons')
def validate_buttons(context):

    driver,wait = (context.driver, context.wait)
    
    BUY = wait.until(EC.visibility_of_element_located(GoldPage.BUY_BUTTON))

    SELL = wait.until(EC.visibility_of_element_located(GoldPage.SELL_BUTTON))


    assert not BUY.is_enabled() and not SELL.is_enabled()
    
    
@when(u'I move to the homescreen')
def move_to_the_homescreen(context):

    driver,wait = (context.driver, context.wait)

    wait.until(EC.element_to_be_clickable(GoldPage.BACK_BUTTON_GOLD_DASHBOARD)).click()
    
    wait.until(EC.element_to_be_clickable(GoldPage.BACK_BUTTON_ON_LEARNING_SCREEN)).click()
    
    wait.until(EC.element_to_be_clickable(GoldPage.BACK_BUTTON_ON_PRECIOUS_METALS_DASHBOARD)).click()
    
    wait.until(EC.element_to_be_clickable(GoldPage.BACK_BUTTON_ON_LEARNING_SCREEN)).click()
    


@when(r"I add ([^']*) to the cash account")
def add_amount_to_the_save_account(context,amount):

    driver,wait = (context.driver, context.wait)
    
    amount = int(amount)
    
    wait.until(EC.element_to_be_clickable(NonProd.PROFILE_ICON_HOMESCREEN)).click()
    
    tap_on_version = wait.until(EC.element_to_be_clickable(NonProd.VERSION_BUTTON))
    
    for i in range(1,16):
        tap_on_version.click()
        time.sleep(0.5)
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Enjoying our app?"))')
    
    wait.until(EC.element_to_be_clickable(NonProd.NON_PROD_OPTIONS_BUTTON)).click()
    
    wait.until(EC.element_to_be_clickable(NonProd.TRANSACTION_ACTIVITIES)).click()
    
    wait.until(EC.element_to_be_clickable(NonProd.INPUT_AMOUNT_FIELD)).send_keys(amount)

    wait.until(EC.element_to_be_clickable(NonProd.DEPOSIT_TO_YOUR_ACCOUNT_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(NonProd.BACK_BUTTON_ON_NONPROD)).click()

    time.sleep(5)

    wait.until(EC.element_to_be_clickable(NonProd.UMOH_BUTTON_ON_HOMESCREEN)).click()

@then(u'I validate buy and sell buttons state')
def validation(context):

    driver,wait = (context.driver, context.wait)
    
    wait.until(EC.element_to_be_clickable(GoldPage.SCROLL_TO_INVEST_EXPLORE_BUTTON)).click()
    
    wait.until(EC.element_to_be_clickable(GoldPage.GOLD_GET_STARTED_BUTTON)).click()
    
    Util.pull_to_refresh(driver, n_times=2)
    
    buy = wait.until(EC.element_to_be_clickable(GoldPage.BUY_BUTTON))

    assert buy.is_enabled()
    
    sell = wait.until(EC.visibility_of_element_located(GoldPage.SELL_BUTTON))

    assert not sell.is_enabled()
@when(u'I click on the buy button')
def click_on_buy_button(context):

    driver,wait = (context.driver, context.wait)
    
    Util.pull_to_refresh(driver, n_times=1)
    
    wait.until(EC.element_to_be_clickable(GoldPage.BUY_BUTTON)).click()

@when(u'I enter amount greater than cash account balance')
def input_amount_greater_than_balance(context):

    driver,wait = (context.driver, context.wait)
    amount = 500
    wait.until(EC.element_to_be_clickable(GoldPage.AMOUNT_INPUT)).send_keys(amount)

@when(r"I enter amount ([^']*) and click on preview")
def enter_amount_click_preview(context,amount):
    driver,wait = (context.driver, context.wait)
    amount = int(amount)
    wait.until(EC.element_to_be_clickable(GoldPage.AMOUNT_INPUT)).send_keys(amount)
    wait.until(EC.element_to_be_clickable(GoldPage.PREVIEW_BUTTON)).click()

@when(u'I click on buy button on the preview screen')
def clicks_on_preview_btn(context):
    driver,wait = (context.driver, context.wait)
    wait.until(EC.element_to_be_clickable(GoldPage.BUY_BUTTON)).click()

@then(u'I validate successfully bought message on the screen')
def buy_text_validation(context):

    driver,wait = (context.driver, context.wait)
    
    wait.until(EC.visibility_of_element_located(GoldPage.BOUGHT_SUCCESSFULLY_TEXT))
    
    wait.until(EC.visibility_of_element_located(GoldPage.AUTOMATE_YOUR_SAVINGS_TEXT))
    
@when(r"I switch to grams and enter ([^']*) grams")
def clicks_on_conversion_btn(context,amount):

    driver,wait = (context.driver, context.wait)
    amount = int(amount)
    
    wait.until(EC.element_to_be_clickable(GoldPage.GRAMS_BUTTON)).click()
    
    wait.until(EC.element_to_be_clickable(GoldPage.GRAMS_INPUT_FIELD)).clear()
    
    wait.until(EC.element_to_be_clickable(GoldPage.AMOUNT_INPUT)).send_keys(amount)

@when(u'I click on the preview button')
def clicks_preview_btn(context):
    driver,wait = (context.driver, context.wait)
    wait.until(EC.element_to_be_clickable(GoldPage.PREVIEW_BUTTON)).click()

@when(u'I click on the skip button')
def clicks_skip_btn(context):
    driver,wait = (context.driver, context.wait)
    wait.until(EC.element_to_be_clickable(GoldPage.SKIP_BUTTON)).click()

@when(u'I click on the sell button')
def clicks_sell_btn(context):
    driver,wait = (context.driver, context.wait)
    Util.pull_to_refresh(driver, n_times=5)
    wait.until(EC.element_to_be_clickable(GoldPage.SELL_BUTTON)).click()

@when(r"I buy gold of ([^']*)")
def buy_gold(context,amount):

    driver,wait = (context.driver, context.wait)

    wait.until(EC.element_to_be_clickable(GoldPage.SCROLL_TO_INVEST_EXPLORE_BUTTON)).click()
    
    wait.until(EC.element_to_be_clickable(GoldPage.PRECIOUS_METALS_DASHBOARD_BUTTON)).click()
    
    wait.until(EC.element_to_be_clickable(GoldPage.GOLD_GET_STARTED_BUTTON)).click()
    
    wait.until(EC.element_to_be_clickable(GoldPage.GOLD_DASHBOARD_BUTTON)).click()
    
    wait.until(EC.element_to_be_clickable(GoldPage.BUY_BUTTON)).click()
    
    amount = 500
    
    wait.until(EC.element_to_be_clickable(GoldPage.AMOUNT_INPUT)).send_keys(amount)
    
    wait.until(EC.element_to_be_clickable(GoldPage.PREVIEW_BUTTON)).click()
    
    wait.until(EC.element_to_be_clickable(GoldPage.BUY_BUTTON)).click()
    
    wait.until(EC.element_to_be_clickable(GoldPage.SKIP_BUTTON)).click()
    
    Util.pull_to_refresh(driver, n_times=2)

@when(u'I move to the gold dashboard from the homescreen')
def move_to_gold_dashboard_from_homescreen(context):

    driver,wait = (context.driver, context.wait)

    wait.until(EC.element_to_be_clickable(GoldPage.SCROLL_TO_INVEST_EXPLORE_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(GoldPage.PRECIOUS_METALS_DASHBOARD_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(GoldPage.GOLD_GET_STARTED_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(GoldPage.GOLD_DASHBOARD_BUTTON)).click()

@when(u'I move to the silver dashboard from the homescreen')
def move_to_silver_dashboard(context):

    driver,wait = (context.driver, context.wait)

    wait.until(EC.element_to_be_clickable(GoldPage.SCROLL_TO_INVEST_EXPLORE_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(GoldPage.PRECIOUS_METALS_DASHBOARD_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(GoldPage.SILVER_GET_STARTED_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(GoldPage.SILVER_DASHBOARD_BUTTON)).click()

@when(u'I move to the platinum dashboard from the homescreen')
def move_to_platinum_dashboard(context):

    driver,wait = (context.driver, context.wait)

    wait.until(EC.element_to_be_clickable(GoldPage.SCROLL_TO_INVEST_EXPLORE_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(GoldPage.PRECIOUS_METALS_DASHBOARD_BUTTON)).click()

    driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true).instance(0))'
        '.setAsVerticalList()'
        '.scrollIntoView(new UiSelector().resourceId("metalsCardGetStartedBtnPlatinum"));'
    )
    time.sleep(2)
    wait.until(EC.element_to_be_clickable(GoldPage.PLATINUM_GET_STARTED_BUTTON)).click()

    wait.until(EC.element_to_be_clickable(GoldPage.PLATINUM_DASHBOARD_BUTTON)).click()
