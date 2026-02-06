from appium.webdriver.common.appiumby import AppiumBy

class SignUpLocators:
    MOBILE_INPUT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("mobileNumberInputField")')

    MOBILE_INPUT_ERROR_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("mobileNumberErrorText")')

    INVALID_OTP_ERROR_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("moduleEnterOtpErrorText")')

    MAX_ATTEMPTS_ERROR_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("moduleEnterOtpErrorText")')

    RESEND_OTP_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("moduleEnterOtpResendOtpButton")')

    OTP_SENT_SNACKBAR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("snackBar")')

    WARNING_ICON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.SvgView").instance(2)')

    ENTER_OTP_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("moduleEnterOtpEnterSixDigitOtp")')

    CREATE_ACC_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("enterDetails2CreateAccountText")')

    CASUAL_NAME_FIELD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("enterDetails2CasualNameInputField")')

    TERMS_CHECKBOX = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.RectView")')

    CASUAL_NAME_ERROR_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("enterDetails2CasualNameErrorText")')

    GET_OTP_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Get OTP')

    CONTINUE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Continue')

    ACCOUNT_OPTIONS_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("accountOptionsQuestionText")')

    TRANSACTIONS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Transactions")')

    USAGE_OPTIONS = {
        'TRANSACTIONS_CHECKBOX': (AppiumBy.ACCESSIBILITY_ID, 'Transactions'),
        'SAVINGS_CHECKBOX': (AppiumBy.ACCESSIBILITY_ID, 'Savings'),
        'INVESTMENTS_CHECKBOX': (AppiumBy.ACCESSIBILITY_ID, 'Investments'),
        'CARDS_CHECKBOX': (AppiumBy.ACCESSIBILITY_ID, 'Cards'),
        'FINANCING_CHECKBOX': (AppiumBy.ACCESSIBILITY_ID, 'Financing')
    }

    SET_PASSWORD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("setPasscodeText")')

    CONFIRM_PASSWORD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("setPasscodeConfirmText")')

    PASSCODE_ERROR_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("setPasscodeErrorText")')

    PASSCODE_CONTINUE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("setPasscodeContinueButton")')

    SECURITY_QUESTIONS_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("securityQuestionsAnsSecurityText")')

    SECURITY_QUE_ERROR_TEXT = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="securityQuestionsMothersMaidenNameErrorText"]')

    PLACE_OF_BIRTH = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("securityQuestionsPlaceOfBirthInputField")')

    MAIDEN_NAME = (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="securityQuestionsMothersMaidenNameInputField"]')

    SECURITY_MISSING = (AppiumBy.ACCESSIBILITY_ID, 'Hardware Security Missing')

    STAY_ON_HUGOLITE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Stay on HugoLite")')

    HOME_PAGE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Home")')

    SELECT_COUNTRY_OF_BIRTH_DROPDOWN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Select")')

    COUNTRY_OF_BIRTH = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Pakistan")')

    CONTINUE_ONBOARDING_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Continue Onboarding")')
