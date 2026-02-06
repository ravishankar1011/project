import os
import subprocess

import allure
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from tests.ui.hugosave_automation.caps.capabilities import dcaps

# Get base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLURE_RAW_DIR = os.path.join(BASE_DIR, "reports", "allure_raw")
ALLURE_REPORT_DIR = os.path.join(BASE_DIR, "reports", "allure_report")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")

def before_scenario(context, scenario):
    """Called before each scenario."""
    url = "http://127.0.0.1:4723"
    context.driver = webdriver.Remote(url, options=dcaps().get_options())
    context.wait = WebDriverWait(context.driver, 120)
    # Clean up raw allure results from last run
    os.makedirs(ALLURE_RAW_DIR, exist_ok=True)
    for f in os.listdir(ALLURE_RAW_DIR):
        if f.endswith(".json"):
            os.remove(os.path.join(ALLURE_RAW_DIR, f))

def after_scenario(context, scenario):
    context.driver.quit()
