from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By

class ETFs:

    QUIZ_LINK_ON_THE_HOMESCREEN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("defaultQuizButtonTestId")')

    START_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Start")')

    NEWBIE_OPTION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Newbie")')

    AMATEUR_OPTION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Amateur")')

    CONFIDENT_OPTION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Confident")')

    PRO_OPTION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Pro")')

    NEXT_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Next >")')

    LESS_THAN_A_YEAR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Less than a 1 yr")')

    ONE_TO_THREE_YEARS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("1-3 yrs")')

    UPTO_FIVE_YEARS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Up to 5 yrs")')

    FIVE_YEARS_OR_MORE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("5 yrs or more")')

    AVOID_LOOSING_MUCH_MONEY = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("To avoid losing much money")')

    TO_GROW_MONEY = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("To grow money more carefully")')

    TO_GROW_MONEY_AGGRESSIVELY = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("To grow money aggressively")')

    SELL_YOUR_ENTIRE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Sell your entire portfolio")')

    SELL_SOME = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Sell some of your portfolio")')

    BUY_MORE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Buy more")')

    A_LIMITED_LOSS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("A limited loss of 5%")')

    UPTO_TEN_PERCENT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Up to 10%")')

    A_LARGE_LOSS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("A large loss would make no impact")')

    GET_RESULTS_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Get Results")')

    BACK_TO_HOME_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Back to Homescreen")')

    SCROLL_TO_EXPLORE_BUTTON = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true).instance(0))'
        '.scrollIntoView(new UiSelector().resourceId("exploreButton").instance(0))',
    )
    ETFS_DASHBOARD_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("ETF Portfolios Dashboard")')

    MMF_GET_STARTED_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("initialCardBtnMoney Market Fund")')

    MMF_DASHBOARD_BUTTON_ON_LEARNING_SCREEN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("defaultButtonTestId")')

    CAUTIOUS_GET_STARTED_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("initialCardBtnCautious")')

    CAUTIOUS_DASHBOARD_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Cautious Portfolio Dashboard")')

    BALANCED_GET_STARTED_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("initialCardBtnBalanced")')

    BALANCED_DASHBOARD_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Balanced Portfolio Dashboard")')

    GROWTH_GET_STARTED_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("initialCardBtnGrowth")')

    GROWTH_DASHBOARD_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Growth Portfolio Dashboard")')

    AMOUNT_INPUT_FIELD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("etfBuyInput")')





























