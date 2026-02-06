from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By

class Pots:

    GET_STARTED_BUTTON_ON_HOMESCREEN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Get Started")')

    GET_STARTED_BUTTON_ON_LEARNING_SCREEN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("overviewLearningScreenBtn")')

    POT_NAME_FIELD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("createPotNameInput")')

    GOAL_AMOUNT_FIELD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("createPotGoalAmountInput")')

    CALENDER_ICON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("createPotCalenderIcon")')

    OK_BUTTON_ON_CALENDER = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("android:id/button1")')

    CANCEL_BUTTON_ON_CALENDER = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("android:id/button2")')

    NEXT_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("createPotNextBtn")')

    CREATE_POT_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Create Pot")')

    SUCCESS_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("createPotConfirmationText")')

    ADD_ONE_DOLLAR_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Yes, Add S$ 1")')

    I_WILL_DO_IT_LATER_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("I’ll do it later")')

    POT_NAME_ON_DASHBOARD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("dashboardPotName")')

    ADD_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("addToPotAddBtn")')

    CURRENT_VALUE_ON_POT_DASHBOARD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("dashboardCurrencyValue")')

    TRNX_RECORD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("From Save Account")')

    BACK_BUTTON = (AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/com.horcrux.svg.SvgView/com.horcrux.svg.GroupView/com.horcrux.svg.PathView')

    ADD_TO_POT_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("dashboardFooterAddBtn")')

    AMOUNT_ADDED_SUCCESSFULLY_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("addMoneyConfirmText")')

    WITHDRAW_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("dashboardFooterWithrawBtn")')

    WITHDRAW_BUTTON_ON_PREVIEW = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Withdraw")')

    WITHDRAWN_SUCCESSFULLY_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("successText")')


















