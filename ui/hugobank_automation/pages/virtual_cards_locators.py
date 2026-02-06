from appium.webdriver.common.appiumby import AppiumBy

class VirtualCards:

    CARDS_TAB_ON_HOMESCREEN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tabBarButtonTestId")')

    CARDS_DASHBOARD_ON_LEARNING_SCREEN = (AppiumBy.ACCESSIBILITY_ID, 'Cards Dashboard')

    NEW_CARD_BUTTON_ON_CARDS_DASHBOARD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("addCardButtonTestID")')

    VIRTUAL_TAB = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Virtual")')

    ORDER_VIRTUAL_CARD_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("orderCardButtonTestId")')

    YOUR_NAME_ON_CARD_DROPDOWN = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="Ria"]/android.view.ViewGroup/com.horcrux.svg.SvgView')

    CARD_NAME_INPUT_FIELD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText")')

    SHOPPING_LABEL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Shopping")')

    GROCERY_LABEL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Grocery")')

    SUBSCRIPTION_LABEL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Subscription")')

    EDUCATION_LABEL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Education")')

    CONTINUE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("continueButtonTestID")')

    FORGOT_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("enterPasscodeForgetButton")')

    ENTER_PIN_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("enterPasscodeText")')

    PLACE_ORDER_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Place Order")')

    CARD_UI = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("card")')

    UNHIDE_ICON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("toggleVisibility")')

    COPY_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("copyBtn")')

    COPIED_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("copyFeedback")')

    CARD_NUMBER_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("pan")')

    EXP_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("expiry")')

    CVV_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cvv")')

    MANAGE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Manage")')

    LOCK_BUTTON = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="Lock"]/android.view.ViewGroup')

    UNLOCK_SNACKBAR_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("snackBar")')

    BACK_BUTTON_VIRTUAL_CARD_DASHBOARD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("backButtonTestId")')

    FIRST_VIRTUAL_CARD_ON_CARDS_DASHBOARD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("virtualCardActiveCardNumberTextTestID")')

    HOME_TAB = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("homeTabBarButton")')

    CURRENT_ACC_BALANCE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("currencyValue")')

    FIRST_TRNX_RECORD_OF_VIRTUAL_CARD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Card Transaction")')

    TRANSACTION_AMOUNT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("defaultCurrencyValueTestId")')

    CLOSED_TEXT_ON_TRNX_RECORD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("statusComponentMainDescriptionTestID")')

    BACK_BUTTON_ON_TRNX_RECORD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("networthOverview2GoBackButton")')

    BACK_BUTTON_ON_CARDS_DASHBOARD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.SvgView").instance(0)')

    DO_NOT_SHOW_AGAIN_CHECKBOX = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.RectView")')

    YES_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Yes")')

    NO_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("No")')

    CARD_LOCKED_SUCCESSFULLY_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Card locked Successfully")')

    CARD_IS_LOCKED_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Card is locked")')

    CARD_DASHBOARD_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("orderCardBtnTestId")')

    CARD_LOCKED_ON_CARDS_DASHBOARD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("virtualCardLockedInfoTextTestID")')

    YOU_CANNOT_SPEND_TEXT_ON_THE_CARD_DASHBOARD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("You cannot spend using card whilst it is locked.")')

    UNLOCK_ICON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("disableLockCardTestId")')

    E_COMMERCE_BUTTON_ON_MANAGE_CARD_SCREEN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("E_COMMERCEtextLabelTestId")')

    LIMIT_EDIT_ICON = (AppiumBy.XPATH, '//android.view.ViewGroup[@resource-id="channelHeaderRightIcon"]/com.horcrux.svg.SvgView')

    LOCAL_TOGGLE_ICON = (AppiumBy.XPATH, '//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[2]')

    LIMIT_AMOUNT_FIELD = (AppiumBy.CLASS_NAME, 'android.widget.EditText')

    LIMIT_AMOUNT_FIELD_AFTER = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("0")')

    OFF_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("statusBadgeOFFTextId")')

    SAVE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Save")')

    CANCEL_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Cancel")')

    CANCEL_CARD_TAB_ON_THE_MANAGE_CARD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cancelCardBtnTestID")')

    CANCEL_CARD_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("closeCardButtonTestID")')

    ORDER_NEW_VIRTUAL_CARD_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("orderNewCardNudgeTitleTestID")')

    SKIP_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("orderNewCardNudgeSkipButtonTestID")')

    CARD_IS_CANCELLED_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Card is cancelled")')

    LOCAL_TOGGLE_OFF = (AppiumBy.XPATH, '//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup')

    LOCAL_TOGGLE_ON = (AppiumBy.XPATH, '//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup')

    BACK_BUTTON_ON_E_COMMERCE_SCREEN = (AppiumBy.XPATH, '//android.view.ViewGroup[@resource-id="backButtonTestId"]/com.horcrux.svg.SvgView/com.horcrux.svg.GroupView/com.horcrux.svg.PathView')

    BACK_BUTTON_ON_MANAGE_CARD_SCREEN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("backIconTestID")')

    E_COMMERCE_DAILY_LIMIT_REACHING_SOON_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("E-commerce Daily Spend Limit reaching soon!")')

    E_COMMERCE_DAILY_LIMIT_EXHAUSTED_TEXT = (AppiumBy.XPATH, '//android.widget.TextView[@text="E-commerce Daily Spend Limit exhausted!"]')

    DAILY_LIMIT_REACHING_SOON_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Daily limit reaching soon!")')

    DAILY_LIMIT_EXHAUSTED_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Daily limit exhausted!")')

    LIMIT_ALERT_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Limit alert")')

    VIEW_EDIT_HISTORY_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("View Edit History")')

    EDIT_CARD_LABEL_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cardLabelTextTestID")')

    ROUNDUPS_TEXT_ON_CARDS_DASHBOARD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Roundups")')

    FIRST_FIELD_IN_PASSCODE_FIELD = (AppiumBy.XPATH, '//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]')

