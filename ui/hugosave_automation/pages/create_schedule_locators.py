from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By  # If you need By locators

class CreateSchedule:

    CREATE_SCHEDULE_TAB_ON_DASHBOARD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("scheduleButtonTestId")')

    DAILY_RADIO_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.RectView").instance(0)')

    WEEKLY_RADIO_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.RectView").instance(1)')

    MONTHLY_RADIO_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.RectView").instance(2)')

    AMOUNT_FIELD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("00.00")')

    SCHEDULE_AMOUNT_CANNOT_BE_ZERO_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Schedule amount cannot be zero or empty.")')

    MONDAY_OPTION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Mon")')

    TUESDAY_OPTION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Tue")')

    WEDNESDAY_OPTION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Wed")')

    THURSDAY_OPTION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Thu")')

    FRIDAY_OPTION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Fri")')

    WEEK_DROPDOWN = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="1st"]/android.view.ViewGroup')

    FIRST_WEEK = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("undefined0")')

    SECOND_WEEK = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("undefined1")')

    THIRD_WEEK = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("undefined2")')

    FOURTH_WEEK = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("undefined3")')

    CONFIRM_SCHEDULE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Confirm Schedule")')

    SCHEDULED_SUCCESSFULLY_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Scheduled Successfully!")')








