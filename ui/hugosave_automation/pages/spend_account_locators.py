from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By


class SpendAccountLocators:
    """Locators for the Spend Account page."""

    # locators for spend account banner
    SPEND_ACCOUNT_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("cardAccountText")')

    SPEND_ACCOUNT_DASHBOARD_BUTTON = (AppiumBy.ACCESSIBILITY_ID,'Spend Account Dashboard')

    NEXT_BUTTON_ANNOUNCEMENT_MODAL = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Next")')

    DONE_BUTTON_ANNOUNCEMENT_MODAL = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Done")')

    TOP_UP_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().className("android.view.ViewGroup").instance(29)')

    TOP_UP_INPUT_FIELD = (AppiumBy.CLASS_NAME,'android.widget.EditText')

    TOP_UP_PREVIEW_BUTTON = (AppiumBy.ACCESSIBILITY_ID,'Preview')

    PREVIEW_TOP_UP_BUTTON = (AppiumBy.ACCESSIBILITY_ID,'Top-up')

    GO_TO_DASHBOARD_BUTTON = (AppiumBy.ACCESSIBILITY_ID,'Go to Dashboard')

    TOP_UP_FROM_SAVE_ACCOUNT_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Top-up from Save Acc.")')

    WITHDRAW_BUTTON = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="Withdraw to Save Acc."]//com.horcrux.svg.PathView')

    LOCK_ACC_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Lock Acc.")')

    PREVIEW_WITHDRAW_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Withdraw')

    LOCK_SPEND_ACCOUNT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Lock Spend Account')
