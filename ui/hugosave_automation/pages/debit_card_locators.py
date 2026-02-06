from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By  # If you need By locators


class DebitCardLocators:

    # spend account dashboard
    DEBIT_CARD_ORDER_CARD = (AppiumBy.ANDROID_UIAUTOMATOR,
                                       'new UiSelector().text("Visa Platinum Debit Card")')

    # learning screen
    ORDER_DEBIT_CARD_DASHBOARD_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Order Debit Card')

    # order card screen
    ORDER_DEBIT_CARD_HEADER = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("orderCardHeader")')

    NAME_ON_CARD = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("nameOnCardDropdown")')

    CONFIRM_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Confirm')

    # card dashboard
    ACTIVATE_IT_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Activate it")')

    CARD_TOKEN_INPUT_FIELD = (AppiumBy.CLASS_NAME, 'android.widget.EditText')

    ACTIVATE_DEBIT_CARD_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Activate Debit Card')

    # card activation success screen
    GO_TO_CARD_DASHBOARD_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Go to Card Dashboard')

    # card dashboard
    EXPIRY_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("expiryTitle")')

    CVV_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cvvTitle")')

    BACK_BUTTON_ON_CARD_DASHBOARD = (AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/com.horcrux.svg.SvgView/com.horcrux.svg.GroupView/com.horcrux.svg.PathView')

    BACK_BUTTON_ON_SPEND_ACCOUNT = (AppiumBy.XPATH, '//android.view.ViewGroup[@resource-id="backButton"]/android.view.ViewGroup/com.horcrux.svg.SvgView/com.horcrux.svg.GroupView/com.horcrux.svg.PathView')

    BACK_BUTTON_ON_SPEND_ACCOUNT_LEARNING_SCREEN = (AppiumBy.XPATH, '//android.view.ViewGroup[@resource-id="backButton"]/android.view.ViewGroup/com.horcrux.svg.SvgView/com.horcrux.svg.GroupView/com.horcrux.svg.PathView')
