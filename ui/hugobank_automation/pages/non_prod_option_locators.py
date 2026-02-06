from appium.webdriver.common.appiumby import AppiumBy


class NonProd:
    PROFILE_ICON_HOMESCREEN = (AppiumBy.ANDROID_UIAUTOMATOR,
                               'new UiSelector().className("com.horcrux.svg.SvgView").instance(0)')

    CURRENT_VERSION_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Current Version:")')

    NON_PROD_OPTIONS_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Nonprod Options')

    TRANSACTION_ACTIVITIES = (AppiumBy.ACCESSIBILITY_ID, 'Transaction Activities')

    INPUT_AMOUNT_FIELD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("inputAmount")')

    DEPOSIT_TO_YOUR_ACCOUNT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Deposit to your account')

    NON_PROD_BACK_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("nonProdBackButton")')

    NON_PROD_TO_HOME_BUTTON = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("com.horcrux.svg.GroupView").instance(3)'
    )

    SCHEDULE_ACTIVITIES = (AppiumBy.ACCESSIBILITY_ID, 'Schedule Activities')

    SELECT = (AppiumBy.ACCESSIBILITY_ID, 'Select')

    CURRENT_ACCOUNT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Current A/C")')

    SCHEDULE_DROP_DOWN = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("scheduleSelectDropdown0")')

    TICKLE_SCHEDULE = (AppiumBy.ACCESSIBILITY_ID, 'Tickle Schedule')

    CARD_ACTIVITIES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cardButton")')

    SELECT_DROPDOWN_1 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Select").instance(0)')

    SELECT_DROPDOWN_2 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Select")')

    CURRENT_ACC_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Current A/C")')

    FIRST_VIRTUAL_CARD = (AppiumBy.ANDROID_UIAUTOMATOR,
                          'new UiSelector().className("android.widget.TextView").instance(1)')

    ENTER_AMOUNT_FIELD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Enter amount")')

    SELECT_DROPDOWN_3 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Select")')

    AUTH_CLEAR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("undefined1")')

    CHANNEL_DROPDOWN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Channel")')

    E_COMMERCE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("undefined1")')

    MAKE_CARD_TRANSACTION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Make Card Transaction")')

    TRANSACTIONS_TEXT_ON_HOMESCREEN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Transactions")')
