from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By  # If you need By locators


class Signup:

    # Mobile Input screen locators

    WELCOME_TEXT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("mobileNumberWelcomeText")',
    )

    JOURNEY_TEXT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("mobileNumberJourneyText")',
    )

    GET_OTP_BUTTON = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("mobileNumberContinue")',
    )

    MOBILE_INPUT_FIELD = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("mobileNumberInputField")',
    )

    ERROR_TEXT_MOBILE_INPUT_FIELD = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("mobileNumberErrorText")',
    )

    # OTP screen loactors

    WELCOME_TEXT_ON_OTP_SCREEN = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("moduleEnterOtpPageTitle")',
    )

    ENTER_6_DIGIT_OTP_TEXT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("moduleEnterOtpEnterSixDigitOtp")',
    )

    RESEND_OTP_BUTTON = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("moduleEnterOtpResendOtpButton")',
    )

    ERROR_TEXT_ON_OTP_SCREEN = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("moduleEnterOtpErrorText")',
    )

    NEW_OTP_SENT_TEXT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("New OTP sent via SMS")',
    )

    # Create Account screen

    CREATE_ACCOUNT_TEXT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("enterDetails1CreateAccountText")',
    )

    CASUAL_NAME_TEXT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("enterDetails1CasualNameText")',
    )

    FULL_NAME_TEXT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("enterDetails1LegalNameText")',
    )

    EMAIL = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("enterDetails1EmailText")',
    )

    TERMS_AND_CONDITIONS_LINK = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Terms")',
    )

    CONTINUE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Continue")')

    ERROR_TEXT_CASUAL_NAME = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("enterDetails1CasualNameErrorText")',
    )

    ERROR_TEXT_FULL_NAME = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("enterDetails1LegalNameErrorText")',
    )

    ERROR_TEXT_EMAIL = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("enterDetails1EmailErrorText")',
    )

    CASUAL_NAME_FIELD = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("enterDetails1CasualNameInputField")',
    )

    FULL_NAME_FIELD = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("enterDetails1LegalNameInputField")',
    )

    EMAIL_FIELD = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("enterDetails1EmailInputField")',
    )

    CHECKBOX = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("com.horcrux.svg.RectView")',
    )

    SET_YOUR_PASSCODE_TEXT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("setPasscodeText")',
    )

    PASSCODES_DO_NOT_MATCH_TEXT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("setPasscodeErrorText")',
    )

    PASSCODES_MATCH_TEXT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("setPasscodeMatchedText")',
    )

    CREATE_ACCOUNT_BUTTON = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("setPasscodeContinueButton")',
    )

    BACK_BUTTON_ON_SET_PASSCODE_SCREEN = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("com.horcrux.svg.PathView")',
    )

    # Allow Notifications screen locators

    ENABLE_NOTIFICATIONS_DESC = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("enableNotificationsDescriptionText")',
    )

    BELL_ICON = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("enableNotificationsIllustration")',
    )

    TURN_OFF_TEXT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("enableNotificationsTurnOffAnytimeText")',
    )

    ALLOW_NOTIFICATIONS_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Allow Notifications")

    NOT_NOW_BUTTON = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("enableNotificationsNotNowButton")',
    )

    WELCOME_TEXT_ON_HOMESCREEN = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Welcome to Hugosave Lite!")',
    )

    SHOW_ME_AROUND_TEXT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Show me around >")',
    )

    CLOSE_SHOW_ME_AROUND = (AppiumBy.XPATH,'//android.view.ViewGroup[@resource-id="homeShowMeAroundOverlayClose"]/android.view.ViewGroup/com.horcrux.svg.SvgView/com.horcrux.svg.GroupView/com.horcrux.svg.GroupView/com.horcrux.svg.PathView')

    LOW_BALANCE_ICON_OF_SPEND_ACCOUNT = (AppiumBy.XPATH,'//android.widget.ScrollView[@resource-id="homeScreenScroll"]/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup[6]/android.view.ViewGroup/android.view.ViewGroup/com.horcrux.svg.SvgView')






