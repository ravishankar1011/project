import random
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from tests.ui.hugobank_automation.pages.signuplocators import SignUpLocators
import re
import random
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from tests.ui.hugobank_automation.pages.signuplocators import SignUpLocators
import re
import time
from tests.ui.hugobank_automation.pages.savings_pot_locators import SavingsPotLocator
from appium.webdriver.common.appiumby import AppiumBy

class Testing:
    @staticmethod
    def generate_random_number(prefix, digits_count=8):
        random_digits = ''.join(random.choices('0123456789', k=digits_count))
        return prefix + random_digits

    @staticmethod
    def enter_otp(driver, wait, otp):
        wait.until(EC.presence_of_element_located(SignUpLocators.ENTER_OTP_TEXT))
        actions = ActionChains(driver)
        for digit in otp:
            actions.send_keys(digit)
        actions.perform()

    def get_scrollable_locator(text):
        return (AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("{text}"))')

def valid_pot_name(name):
    if not name or name.isspace():
        return False
    return bool(re.fullmatch(r"[A-Za-z0-9 ]+", name))

def pull_to_refresh_from_middle(driver, n_times=None):
    size = driver.get_window_size()
    start_x = size["width"] // 2
    start_y = size["height"] // 2
    end_y = int(size["height"] * 0.9)
    driver.swipe(start_x, start_y, start_x, end_y, 1000)  # 1000ms duration
    if n_times and int(n_times) > 1:
        for _ in range(int(n_times) - 1):
            time.sleep(2)
            driver.swipe(start_x, start_y, start_x, end_y, 1000)

def pull_to_refresh(driver, n_times=1):
    size = driver.get_window_size()
    width = size["width"]
    height = size["height"]

    start_x = width // 2
    start_y = int(height * 0.25)
    end_y = int(height * 0.75)

    for i in range(int(n_times)):
        driver.swipe(start_x, start_y, start_x, end_y, 1000)
        time.sleep(1)
        print(f"Pull-to-refresh swipe #{i + 1} performed")


frequency_map = {
    "Daily": SavingsPotLocator.DAILY_SCHEDULE_BUTTON,
    "Weekly": SavingsPotLocator.WEEKLY_SCHEDULE_BUTTON,
    "Monthly": SavingsPotLocator.MONTHLY_SCHEDULE_BUTTON,
    "Quarterly": SavingsPotLocator.QUARTERLY_SCHEDULE_BUTTON
}

payment_map = {
    "Once": SavingsPotLocator.ONCE,
    "Twice": SavingsPotLocator.TWICE
}
def scroll_to_top(driver):
    size = driver.get_window_size()
    start_x = size['width'] / 2
    start_y = size['height'] * 0.2   # near top
    end_y = size['height'] * 0.8     # near bottom

    # swipe from bottom to top multiple times
    for _ in range(3):  # adjust depending on how much content to scroll
        driver.swipe(start_x, start_y, start_x, end_y, 800)
    time.sleep(2)

class DataStore:
   internal_account_number = None
   internal_raast_id = None
   internal_IBAN_number = None