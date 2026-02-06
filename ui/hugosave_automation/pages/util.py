import random
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.actions import interaction
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

class Util:
    def __init__(self, prefix="+373"):
        self.prefix = prefix
        self.current_version = "Current Version: 2.1.187"

    @staticmethod
    def step_scroll_up(driver, distance):
        actions = ActionChains(driver)
        window_size = driver.get_window_size()
        x, y = window_size['width'] / 6, window_size['height'] / 2
        # override as 'touch' pointer action
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(x, y)
        actions.w3c_actions.pointer_action.click_and_hold()
        actions.w3c_actions.pointer_action.move_to_location(x, y - distance)
        actions.w3c_actions.pointer_action.release()
        actions.w3c_actions.perform()

    @staticmethod
    def generate_phone_number(prefix="+373", length=8):
        """
        Generates a phone number by combining a prefix with random digits.

        :param prefix: The prefix for the phone number (default is '+373').
        :param length: Total length of the phone number (default is 10).
        :return: A phone number as a string.
        """
        random_digits = ''.join(random.choices('0123456789', k=length))
        return prefix + random_digits

    @staticmethod
    def is_valid_casual_or_legal_name(name):
        if not name:  # Handles None and empty strings
            return False

        return bool(re.fullmatch(r"^[A-Za-z ]+$", name))

    @staticmethod
    def is_valid_email(email):
        if not email:  # Handles None and empty strings
            return False
        return bool(re.fullmatch(r"^[A-Za-z0-9]+@[A-Za-z]+\.[A-Za-z]+$", email))

    @staticmethod
    def dummy_name():
        alphabets = [chr(i) for i in range(97, 123)]  # Create a list of alphabets
        random.shuffle(alphabets)  # Shuffle the list in place
        name = ''.join(random.choices(alphabets, k=5))  # Pick 5 random letters
        return name

    @staticmethod
    def pull_to_refresh(driver,n_times=None):
        size = driver.get_window_size()
        start_x = size["width"] // 2  # center horizontally
        start_y = size["height"] // 4  # start from the top screen
        end_y = size["height"] // 2  # Swipe down to the middle of the screen

        # Perform the swipe down gesture
        driver.swipe(start_x, start_y, start_x, end_y, 1000)  # 1000ms duration
        if n_times and int(n_times) > 1:
            for _ in range(int(n_times)-1):
                time.sleep(2)
                driver.swipe(start_x, start_y, start_x, end_y, 1000)
                print('pulled ',_)

    @staticmethod
    def close_keyboard_if_shown(driver):
        try:
            # Check if the keyboard is shown (Appium 2+)
            if driver.is_keyboard_shown():
                print("Keyboard is visible. Hiding it now...")
                driver.hide_keyboard()
            else:
                print("Keyboard is already hidden.")
        except Exception as e:
            print(f"Error checking keyboard state: {e}")

    @staticmethod
    def perform_touch_action(driver, x, y):
        """
        Perform a touch action at the given x, y coordinates.

        :param driver: The WebDriver instance.
        :param x: The x-coordinate where the touch should occur.
        :param y: The y-coordinate where the touch should occur.
        """
        actions = ActionChains(driver)
        # override as 'touch' pointer action
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(x, y)
        actions.w3c_actions.pointer_action.click()
        actions.perform()

    @staticmethod
    def valid_OTP(driver):
        c = 8
        for i in range(6):
            driver.press_keycode(c)
            c += 1
        return '123456'

    @staticmethod
    def mismatch_passcode(driver):
        for i in range(11):
            driver.press_keycode(7)
        driver.press_keycode(8)
        return '111111,111112'

    @staticmethod
    def backspace(driver):
        c = 4
        for i in range(6):
            driver.press_keycode(c)
        return None

    @staticmethod
    def transform_passcode(driver, passcode: str) -> None:
        mapping = {
            "0": "7", "1": "8", "2": "9", "3": "10", "4": "11",
            "5": "12", "6": "13", "7": "14", "8": "15", "9": "16", "backspace": "67"
        }

        transformed_passcode = [int(mapping[digit]) for digit in passcode]

        # Using a lambda function for minimal overhead
        _ = list(map(driver.press_keycode, transformed_passcode))

    @staticmethod
    def is_valid_payee_name(name):
        if not name:  # Handles None and empty strings
            return False
        return bool(re.fullmatch(r"^[A-Za-z]+(?: [A-Za-z]+)*$", name))

    @staticmethod
    def int_or_ext_payee(bank_name, driver):
        if bank_name is not None and bank_name != 'DBS Bank Ltd':
            ext_bank_list = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((AppiumBy.ACCESSIBILITY_ID,
                                                                                                 'Citibank NA Singapore Branch')))
            if ext_bank_list:
                ext_bank_list[0].click()
            else:
                # Scroll only if the element isn't found initially
                external_bank = WebDriverWait(driver, 60).until(EC.presence_of_element_located((
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().description("Citibank NA Singapore Branch"))'
                )))
                external_bank.click()

        elif bank_name == 'DBS Bank Ltd':
                # Check if DBS Bank is already visible
            dbs_bank = WebDriverWait(driver, 60).until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().className("android.widget.TextView").text("DBS Bank Ltd"))'
                )))
            dbs_bank.click()

        else:
            print("Invalid bank name entered. Please provide a valid bank name.")
            assert False
