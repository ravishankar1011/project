from appium.webdriver.common.appiumby import AppiumBy


class Homescreen:

    CURRENCY = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("currencyValue")')

    TRANSACTIONS = (AppiumBy.ACCESSIBILITY_ID,'Transactions')

    HOME_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("homeTabBarButton")')

    NOTIFICATIONS_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("homeNavigateToNotificationsPressable")')
