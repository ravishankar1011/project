from appium import webdriver
from tests.ui.hugobank_automation.caps.capabilities import dcaps
from selenium.webdriver.support.ui import WebDriverWait
import os, time
import allure
from allure_commons.types import AttachmentType

def before_scenario(context, scenario):
    # Disabling the autofill OTP
    os.system("adb shell settings put secure autofill_service null")
    os.system("adb shell settings put secure autofill_enabled 0")
    os.system("adb shell settings get secure autofill_enabled")
    url = "http://localhost:4444/wd/hub"
    options = dcaps().get_options()
    context.driver = webdriver.Remote(
        command_executor=url,
        options=options
    )
    context.wait = WebDriverWait(context.driver, 60)


def after_scenario(context, scenario):
    if hasattr(context, "driver"):
        context.driver.quit()


def after_step(context, step):
    if step.status == "failed":
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        step_name = step.name.replace(" ", "_")
        screenshot_dir = os.path.join("tests", "ui", "hugobank_automation", "reports", "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)

        screenshot_path = os.path.join(
            screenshot_dir,
            f"{step_name}_{timestamp}.png"
        )

        context.driver.save_screenshot(screenshot_path)

        with open(screenshot_path, "rb") as image:
            allure.attach(
                image.read(),
                name="Failure Screenshot",
                attachment_type=AttachmentType.PNG
            )

        error_msg = str(step.exception)
        allure.attach(
            error_msg,
            name="Failure Reason",
            attachment_type=AttachmentType.TEXT
        )
