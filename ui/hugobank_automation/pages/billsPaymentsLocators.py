from appium.webdriver.common.appiumby import AppiumBy



class BillsPaymentsLocators:
    BILLS_AND_RECHARGES = (AppiumBy.ACCESSIBILITY_ID, 'Bills & Recharges')

    NEW_PAYMENT_ICON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("dashboardViewPaymentCategoriesFabButton")')

    PAYMENT_CATEGORIES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Payment Categories")')

    # 'new UiSelector().className("android.widget.ImageView").instance(0)'
    CATEGORY_LIST = {
    "Mobile" : {'locator':(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("paymentCategoriesSelectCategoryButton0").instance(0)'),
                'Test Mobilink Prepaid': "Test Mobilink Prepaid",
                'Test Mobilink Postpaid': "Test Mobilink Postpaid",
                'Test Telenor Prepaid': "Test Telenor Prepaid",
                'Test Telenor Postpaid': "Test Telenor Postpaid",
                'Test Bundle 70': "Test Bundle 70",
                'Test Bundle 349': "Test Bundle 349",},

    "Electricity": {'locator': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("paymentCategoriesSelectCategoryButton0").instance(1)'),
                    'Test-Electric': 'Test-Electric',
                    'Test-Elec Connection': 'Test-Elec Connection'},

    "Gas": {'locator':(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("paymentCategoriesSelectCategoryButton1").instance(0)'),
            'TEST-SSGC': 'TEST-SSGC',
            'TEST-SNGPL': 'TEST-SNGPL'}
    }

    RECHARGE_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Recharge")')

    UTILITY_BILLS_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Utility Bills")')

    ADD_CONSUMER_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Add Consumer")')

    ADD_CONSUMER = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("operatorDashboardFabButton")')

    DISABLED_ADD_CONSUMER = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("operatorDashboardDisabledFab")')

    INPUT_FIELD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText")')

    CONFIRM_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Confirm')

    INVALID_ID_MESSAGE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Invalid Mobile Number")')

    GET_OTP = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Get OTP")')

    CONFIRM_SCHEDULE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Confirm Schedule")')

    NICK_NAME_FIELD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(1)')

    OTP_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("enterOTPText")')

    INCORRECT_OTP_MESSAGE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("incorrectOtpText")')

    PASSCODE_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("enterPasscodeText")')

    INCORRECT_PASSCODE_MESSAGE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("enterPasscodeErrorText")')

    TOP_UP_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Top-up")')

    PAY_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("consumerDashboardAfterPayButton")')

    SELECT_BUNDLE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("consumerDashboardChooseBundleButton")')

    # INDIVIDUAL BILLER DASHBOARD BACK BUTTON
    BACK_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("backButton")')

    # INDIVIDUAL OPERATOR DASHBOARD BACK BUTTON
    BACK_BUTTON_OPERATOR_SCREEN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("operatorDashboardBackButton")')

    # SELECT SERVICE OPERATOR OPERATOR DASHBOARD BACK BUTTON
    BACK_BUTTON_SERVICE_SCREEN = (AppiumBy.ANDROID_UIAUTOMATOR,
                                   'new UiSelector().resourceId("allOperatorsBackButton")')

    # PAYMENT CATEGORIES DASHBOARD BACK BUTTON
    BACK_BUTTON_PAYMENT_CATEGORY_SCREEN = (AppiumBy.ANDROID_UIAUTOMATOR,
                                  'new UiSelector().resourceId("paymentCategoriesBackButton")')

    # BILLS AND RECHARGES  DASHBOARD BACK BUTTON
    BACK_BUTTON_BILLS_AND_RECHARGES_SCREEN = (AppiumBy.ANDROID_UIAUTOMATOR,
                                           'new UiSelector().resourceId("dashboardBackButton")')

    EXITED_BILLER_ERROR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Oops! Another bill already exists with this Mobile Number.")')

    GO_TO_BILL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Go to Bill")')

    EDIT_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.SvgView").instance(1)')

    EDIT_DETAILS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("editConsumerOption")')

    DELETE_CONSUMER = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("deleteConsumerOption")')

    CREATE_PAYMENT_SCHEDULE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("createScheduleConsumerOption")')

    DELETE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Delete")')

    MOBILE_NUMBER_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Mobile Number")')

    CANCEL_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Cancel")')

    SAVE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Save")')

    SERVICE_OPERATOR_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Service Operator")')

    SELECT_SERVICE_OPERATOR_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Select Service Operator")')

    ADD_NICKNAME_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Add Nickname")')

    TEXT_ADD_CONSUMER = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Add Consumer")')

#     New payment screen
    NEW_PAYMENT_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("New Payment")')

    PROCEED_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Proceed")')

    BACK_BUTTON_PAYMENT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.PathView")')

    INSUFFICIENT_BALANCE_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Insufficient account balance")')

#     preview screen
    PREVIEW_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Preview")')

    PAY = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("previewPaymentPayBillPayeeButton")')

    TRANSACTION_STATE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("statusComponentMainDescriptionTestID")')

    OUTGOING_PAYMENT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Outgoing Payment")')

    # CREATE SCHEDULE SCREEN
    TEXT_WANT_TO_CREATE_SCHEDULE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("I want to create schedule for")')

    TOP_UP_SCHEDULE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Top-up")')

    BUNDLE_RECHARGE_SCHEDULE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Bundle Recharge")')

    # preview screen
    TOP_UP_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Top-up")')

    # schedule card
    CREATE_SCHEDULE_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Create Schedule")')

    QUARTERLY_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Quarterly")')

    PREVIEW_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Preview")')

    AMOUNT_SCHEDULE_DASHBOARD = (AppiumBy.ANDROID_UIAUTOMATOR,
                                 'new UiSelector().resourceId("defaultTopTextCurrencyViewerTestId")')

    FREQUENCY_SCHEDULE_DASHBOARD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("defaultTopTextValidityTestId")')

    STARTING_DATE_SCHEDULE_DASHBOARD = (AppiumBy.ANDROID_UIAUTOMATOR,
                                        'new UiSelector().resourceId("defaultBottomTextNextOnTestId")')

    SCHEDULE_BILL_PAYMENTS_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Schedule Bill Payments")')

    SCHEDULED_PAYMENT_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("defaultScheduledPaymentTestId")')

    SCHEDULE_EDIT_BUTTON =  (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Edit")')

    VIEW_SCHEDULE_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("View Schedule")')

    EDIT_SAVE_BUTTON =  (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Save")')

    EDIT_SCHEDULE_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Edit Schedule")')

    STOP_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Stop")')

    STOP_YES_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Yes")')

    RESUME_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("resumeButton")')

    RESUME_BUTTON_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("defaultTopTextResumeTestId")')

    SKIP_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Skip")')

    SKIP_YES_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("skipScheduleYesButton")')

    SKIPPED_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Skipped")')

    NEXT_SCHEDULE_SKIPPED_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("defaultBottomTextNextTestId")')

    CURRENT_ACCOUNT_CARD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("accountCardText")')

    HUGOBANK_ACCOUNT_DASHBOARD_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cashDashboardButton")')

    ADD_MONEY_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("navigateToAddMoneyFlowIconButton")')
