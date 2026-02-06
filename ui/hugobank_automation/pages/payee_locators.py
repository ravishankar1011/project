from appium.webdriver.common.appiumby import AppiumBy


class PayeeLocator:

   ADD_NEW_PAYEE_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("addPayeeText")')

   IHAVE_PAYEE_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("addPayeeSubText")')

   OTHERBANK_ACCOUNT_DETAILS_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Other bank A/c Details")')

   HUGOBANK_ACCOUNT_DETAILS_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("HugoBank A/c Details")')

   RAAST_ID_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("RAAST ID")')

   ACCOUNT_INPUT_FIELD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("inputField")')

   NO_ACCOUNT_FOUND_ERROR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("No account found")')

   SUBMIT_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("submitButton")')

   GET_OTP_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("otpButton")')

   CANCEL_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cancelButton")')

   BANK_NAME_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Bank Name")')

   OTP_SCREEN_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("enterOTPText")')

   INCORRECT_OTP_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("incorrectOtpText")')

   ENTER_PASSCODE_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("enterPasscodeText")')

   PASSCODE_CONTINUE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("enterPasscodeContinueButton")')

   INCORRECT_PASSCODE_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("enterPasscodeErrorText")')

   PAYEENAME_NEW_PAYEESCREEN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("payeeName")')

   BANKDETAIL_NEW_PAYEESCREEN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("bankDetail")')

   PAYBUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("payButton")')

   PAYEE_NAME = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("payeeName")')

   BACK_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("backButton")')

   FUNDTRANSFER_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Fund Transfer')

   FUNDTRANSFER_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Fund Transfer")')

   ADD_PAYEE_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Add Payee")')

   ADD_PAYEE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("addPayeeIcon")')

   TEST_BANK_RAAST_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Test Bank Raast")')

   BANK_NAME_BOX = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Bank Name")')

   BANK_ACCOUNT_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Bank A/c Number or IBAN Number")')

   BANK_VERIFIED_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Bank Verified Title")')

   FAVOURITE_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("favoriteText")')

   VERIFIED_ACC_NO_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Verified Account Number")')

   PAYEE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("PT")')

   PAYMENT_INPUT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("paymentInput")')

   PURPOSE_OF_TRANSACTION_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Purpose of Transaction*")')

   PURPOSE_OF_TRANSACTION_OPTION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("undefined0")')

   BILLS_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Bills & Recharges")')

   NO_UPCOMING_SCHEDULES_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("No Upcoming Schedules")')

   PROCEED_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("save")')

   NEW_PAYMENT_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("newPaymentButton")')

   SETTLED_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("statusComponentMainDescriptionTestID")')

   TOTAL_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Total")')

   AMOUNT_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("100.00").instance(1)')

   HOMESCREEN_PROFILE_ICON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("homeSideDrawerPressable")')

   HOMESCREEN_NOTIFICATIONS_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'homeNavigateToNotificationsPressable')

   HUGOBANK_ACCOUNT_DASHBOARD_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cashDashboardButton")')

   HUGOBANK_ACCOUNT_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cashAccountText")')

   RAAST_ID_INPUT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText")')

   ACCOUNT_CARD_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("accountCardText")')

   ACCOUNT_DETAILS_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Account Details")')

   ACCOUNT_NUMBER_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Account Number")')

   ACCOUNT_NUMBER_VALUE = (AppiumBy.XPATH, '//android.widget.TextView[@text="Account Number"]/following-sibling::android.widget.TextView[1]')

   IBAN_NUMBER_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("IBAN Number")')

   IBAN_NUMBER_VALUE = (AppiumBy.XPATH, '//android.widget.TextView[@text="IBAN Number"]/following-sibling::android.widget.TextView[1]')

   RAAST_MANAGEMENT_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("raastManagementText")')

   CREATE_RAASTID_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("createRaastIdButton")')

   PHONE_NUMBER = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("phoneNumber")')

   LINK_RAASTID_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("linkRaastButton")')

   RAASTID_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("raastIdText")')

   RAASTID_VALUE = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="raastIdText"]/following-sibling::android.widget.TextView[1]')

   TRANSACTIONS_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Transactions")')

   INSUFFICIENT_ACCOUNT_BALANCE_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Insufficient account balance")')

   REACHED_ACCOUNT_TRANSFER_LIMIT_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Reached the account transfer limit")')

   TRANSACTION_LIMITS_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("transactionLimitsTexts")')

   DAILY_TRANSACTION_LIMITS_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("titleText")')

   LIMITS_EDIT_ICON = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="titleText"]/following-sibling::android.view.ViewGroup[1]')

   YOUR_LIMIT_OTHER_BANK_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Your limit").instance(2)')

   TO_OTHER_BANK_ACCOUNT_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("To other bank A/c")')

   OTHERBANK_LIMIT_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("50,000").instance(2)')

   OTHERBANK_LIMIT_INPUT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(2)')

   TO_OTHER_HUGOBANK_ACCOUNT_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("To other HugoBank A/c")')

   OTHER_HUGOBANK_LIMIT_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("50,000").instance(3)')

   OTHER_HUGOBANK_LIMIT_INPUT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(3)')

   SAVE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("saveButton")')

   SAVE_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Save")')

   GO_TO_DASHBOARD_BUTTON_LIMITS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("confirmationButton")')

   ACCOUNT_MANAGEMENT_ACTIVITIES_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Account Management Activities")')

   REMOVE_COOL_OFF_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Remove Cool Off")')

   NON_PROD_OPTIONS_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("nonprodOptionsText")')

   NON_PROD_BACK_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("nonProdBackButton")')

   RIGHT_ICON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("rightIcon")')

   HOMESCREEN_SUPPORT_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("homeNavigateToSupportPressable")')

   OTP_INPUT_BOX = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("otpInputBox")')

   HOME_TAB = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("homeTabBarButton")')

   ROUNDUPS_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Roundups")')

   EDIT_PAYEE_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Edit Payee")')

   PAYEE_NICKNAME = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Payee Name/Nickname")')

   VIEW_TRANSACTION_DETAILS_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("payToPayeeNavigateToTransactionButton")')

   OUTGOING_PAYMENT_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Outgoing Payment")')

   BACK_TO_DASHBOARD_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("payToPayeeNavigateToDashBoardButton")')

   PAYEE_DETAILS_UPDATED_SUCCESSFULLY_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Payee details updated successfully")')

   DELETE_PAYEE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Delete Payee")')

   PAYEE_TRANSACTION_SCREEN_BACK_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("newPayment2BackButton")')

   PAYEE_DELETED_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Payee Deleted Successfully")')

   PAYEE_SCHEDULE_DELETED_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Payee and the active scheduled linked to it has been Deleted Successfully")')

   YES_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("yes")')

   #schedules
   CREATE_PAYMENT_SCHEDULE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Create Payment Schedule")')

   SCHEDULE_PREVIEW = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Preview")')

   SCHEDULE_PAYMENT_PAYEE_SCREEN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("defaultScheduledPaymentTestId")')

   FUND_TRANSFER_TEXT_ON_NEW_SCHEDULE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("defaultMiddleTextFundTestId")')

   CURRENCY_TEXT_ON_NEW_SCHEDULE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("defaultTopTextCurrencyViewerTestId")')

   FREQUENCY_SELECTION_ON_NEW_SCHEDULE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("defaultTopTextValidityTestId")')

   START_DATE_ON_NEW_SCHEDULE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("defaultBottomTextNextOnTestId")')

   SCHEDULE_DELETION_MENU = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.SvgView").instance(1)')

   DELETE_SCHEDULE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Delete")')

   SCHEDULE_YES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Yes")')

   SCHEDULE_DELETED_SUCCESSFULLY_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Schedule deleted successfully")')

   SCHEDULE_EDITED_SUCCESSFULLY_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Schedule edited successfully")')

   VIEW_SCHEDULE_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("View Schedule")')

   STOP_SCHEDULE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Stop")')

   SCHEDULE_STOPPED_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Stopped")')

   RESUME_SCHEDULE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Resume")')

   SCHEDULE_ACTIVE_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Active")')

   VIEW_PAYEE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("viewPayeeButton")')

   SCHEDULE_PAY_PAYEE_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Schedule Pay Payee")')

   SCHEDULE_TRIGGER_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("scheduleButton")')

   SCHEDULE_SELECT_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Select")')

   SCHEDULE_CURRENT_ACC_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Current A/C")')

   SCHEDULE_DROPDOWN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("scheduleDropdown")')

   SCHEDULE_PAYEE_TRIGGER = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("scheduleSelectDropdown0")')

   TICKLE_SCHEDULE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("TickleSchedule")')
