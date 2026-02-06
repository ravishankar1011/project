from appium.webdriver.common.appiumby import AppiumBy


class SavingsPotLocator:
    """locators for saving pot module"""

    EXPLORE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Explore')

    SAVINGS_POT_DASHBOARD_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Savings Pot")')

    SAVINGS_POT_LEARNING_DASHBOARD = (AppiumBy.ANDROID_UIAUTOMATOR,
                                      'new UiSelector().resourceId("overviewLearningScreenBtn")')

    SAVINGS_POT_NAME_INPUT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("createPotNameInput")')

    CREATE_POT_NEXT_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("createPotNextBtn")')

    POST_POT_CREATE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("potsPreviewcreatePotBtn")')

    ADD_MONEY_LATER_BUTTON = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="I’ll do it later"]')

    NEW_POT_NAME_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("newPotText")')

    NEW_POT_ICON_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("addPotBtn")')

    POT_NAME_INPUT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("createPotNameInput")')

    GOAL_AMOUNT_INPUT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("createPotGoalAmountInput")')

    POT_GOAL_DATE_INPUT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("createPotCalenderIcon")')

    GOAL_DATE_OK = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("android:id/button1")')

    NEXT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Next')

    NEXT_MONTH = (AppiumBy.ACCESSIBILITY_ID, 'Next month')

    CREATE_POT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Create Pot')

    POT_CLICK_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("potNameText")')

    ADD_MONEY_TO_POT = (AppiumBy.ACCESSIBILITY_ID, 'Add to Pot')

    ENTER_PKR_AMOUNT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("addToPotInputField")')

    PREVIEW_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Preview')

    ADD = (AppiumBy.ACCESSIBILITY_ID, 'Add')

    DASHBOARD_POT_NAME = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("dashboardPotName")')

    DASHBOARD_POT_GOAL_DATE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("dashboardPotGoalDate")')

    DASHBOARD_FAV_POT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("dashboardFavPot")')

    DASHBOARD_CARD_CURRENCY = (AppiumBy.ANDROID_UIAUTOMATOR,
                               'new UiSelector().resourceId("dashboardDetailCardCurrencyVal")')

    DASHBOARD_CURRENCY_VALUE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("dashboardCurrencyValue")')

    WITHDRAW_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Withdraw')

    POT_ONE_CLICK_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("potNameText")')

    ENTER_WITHDRAW_AMOUNT_BUTTON = (AppiumBy.CLASS_NAME, 'android.widget.EditText')

    POT_SCHEDULE_DASHBOARD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("dashboardScheduleButton")')

    DAILY_SCHEDULE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR,
                             'new UiSelector().className("com.horcrux.svg.RectView").instance(0)')

    WEEKLY_SCHEDULE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR,
                              'new UiSelector().className("com.horcrux.svg.RectView").instance(1)')

    MONTHLY_SCHEDULE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR,
                               'new UiSelector().className("com.horcrux.svg.RectView").instance(2)')

    QUARTERLY_SCHEDULE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR,
                                 'new UiSelector().className("com.horcrux.svg.RectView").instance(3)')

    ENTER_SCHEDULE_AMOUNT_BUTTON = (AppiumBy.XPATH,'//android.widget.EditText[@hint="00.00"]')

    SCHEDULE_START_DATE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("calendarIcon")')

    SCHEDULE_PREVIEW = (AppiumBy.ACCESSIBILITY_ID, 'Preview')

    SCHEDULE_DATE_CONFIRM_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("android:id/button1")')

    CONFIRM_SCHEDULE = (AppiumBy.ACCESSIBILITY_ID, 'Confirm Schedule')

    EDIT_CLOSE_POT_MENU = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("dashboardMenuBtn")')

    EDIT_POT_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("dashboardMenuEditBtn")')

    EDIT_POT_ICON_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR,
                            'new UiSelector().className("com.horcrux.svg.PathView").instance(7)')

    EDIT_POT_SAVE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Save')

    EDIT_POT_INPUT_BUTTON = (AppiumBy.CLASS_NAME, 'android.widget.EditText')

    CLOSE_POT_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("dashboardMenuCloseBtn")')

    POT_CLOSE_CONFIRMATION_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("dashboardYesBtn")')

    CLOSE_SAVINGS_POT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Close Savings Pot')

    GO_BACK_POT_HOME_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("imageHeaderBtn")')

    POT_BACK_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("potsBackButton")')

    SCHEDULE_DELETE_MENU = (AppiumBy.XPATH,
                            '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup[2]')

    DELETE_SCHEDULE = (AppiumBy.ACCESSIBILITY_ID, 'Delete')

    YES_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Yes')

    EDIT_SCHEDULE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Edit")')

    SCHEDULE_BACK = (AppiumBy.CLASS_NAME, 'com.horcrux.svg.SvgView')

    EDIT_SCHEDULE_AMOUNT = (AppiumBy.CLASS_NAME, 'android.widget.EditText')

    BACK_TO_SAVINGS_POT = (AppiumBy.ACCESSIBILITY_ID, 'Back to Savings Pot')

    YES_ADD_PKR_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Yes, Add PKR 1')

    ADD_MONEY_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'Add Money')

    VIEW_CLOSED_POTS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("View Closed Pots")')

    MAKE_PAYMENT_DROPDOWN = (AppiumBy.ANDROID_UIAUTOMATOR,
                         'new UiSelector().resourceId("scheduleUntilDropdownIcon")')

    ONCE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Once")')

    TWICE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Twice")')

    THRICE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Thrice")')

    UNTIL_STOPPED = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Until Stopped")')

    AMOUNT_SCHEDULE_DASHBOARD = (AppiumBy.ANDROID_UIAUTOMATOR,
                                 'new UiSelector().resourceId("topTextCurrencyViewerTestId")')

    FREQUENCY_SCHEDULE_DASHBOARD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("topTextFreqTestId")')

    STARTING_DATE_SCHEDULE_DASHBOARD = (AppiumBy.ANDROID_UIAUTOMATOR,
                                        'new UiSelector().resourceId("bottomTextNextOnTestId")')

    YES_SKIP_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Yes, Skip")')

    NO_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("No")')

    CREATE_SCHEDULE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("topTextCreateTestId")')

    CREATE_POT_NAME_WARNING = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("createPotNameWarning")')

    STOP = (AppiumBy.ACCESSIBILITY_ID, 'Stop')

    STOPPED = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Stopped")')

    LIMIT_REACHED = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("limitReachedTxt")')

    CANCEL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("createPotCancelBtn")')

    POTS_PREVIEW_NAME_ICON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("potsPreviewNameEditIcon")')

    POTS_PREVIEW_NAME_INPUT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("potsPreviewNameInput")')

    POTS_PREVIEW_GOAL_ICON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("potsPreviewGoalAmtEditIcon")')

    POTS_PREVIEW_GOAL_INPUT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("potsPreviewGoalAmtInput")')

    POTS_PREVIEW_GOAL_DATE = (AppiumBy.ANDROID_UIAUTOMATOR,
                              'new UiSelector().resourceId("potsPreviewGoalDateEditIcon")')

    POTS_PREVIEW_GOAL_CALENDAR = (AppiumBy.ANDROID_UIAUTOMATOR,
                                  'new UiSelector().resourceId("potsPerviewGoalDateCalenderIcon")')

    INSUFFICIENT_BALANCE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("addToPotInsufficientBalance")')

    STAR_FILLED_ICON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("starFilledMediumIcon")')

    ACTIVE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Active")')

    RESUME = (AppiumBy.ACCESSIBILITY_ID, 'Resume')

    SKIP = (AppiumBy.ACCESSIBILITY_ID, 'Skip')

    GOAL_REACHED = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Goal Reached")')
#
