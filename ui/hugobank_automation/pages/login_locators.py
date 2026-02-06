from appium.webdriver.common.appiumby import AppiumBy

class LoginLocators:
   MOBILE_INPUT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("mobileNumberInputField")')

   ENTER_PASSCODE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("enterPasscodeText")')

   ALLOW_NOTIFICATIONS_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("enableNotificationsAllowButton")')

   NOT_NOW_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Not Now")')

   HOME_PAGE = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Home")')

   PROFILE_ICON = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().className("com.horcrux.svg.SvgView").instance(0)')

   MENU_LOGOUT = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Logout")')

   PASSCODE_ERROR_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("enterPasscodeErrorText")')

   FORGOT_PASSCODE = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Forgot Passcode")')

   CONTINUE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Continue")

   SET_PASSWORD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("setPasscodeText")')

   ENTER_OTP_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("moduleEnterOtpEnterSixDigitOtp")')

   AUTHENTICATION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("pinAuthenticationEnterPasscodeText")')

   OTP_FOR_PASSCODE_RESET = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("enterOTPText")')

   ID_VERIFIED_SNACKBAR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Identity verified successfully!")')

   PASSCODE_RESET_SUCCESS_SNACKBAR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Passcode reset successfully!")')

   PASSCODE_FIELD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.ViewGroup").instance(21)')
