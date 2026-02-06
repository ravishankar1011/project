from appium.webdriver.common.appiumby import AppiumBy
class plus_onboarding_locators:
    UNLOCK_MORE = (AppiumBy.ACCESSIBILITY_ID, 'Unlock more')

    COMPARE_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Compare")')

    UPGRADE_TO_PLUS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.ViewGroup").instance(58)')

    INCOMING_RANGE_DROPDOWN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.PathView").instance(5)')

    INCOMING_PKR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("undefined4")')

    RANGE_PKR = (AppiumBy.ACCESSIBILITY_ID, 'PKR 0 - 50K')

    OUTGOING_RANGE_DROPDOWN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.PathView").instance(8)')

    DECLARATION_CHECKBOX = (AppiumBy.XPATH, '//android.widget.TextView[@text="I hereby declare that I am a tax resident of Pakistan and the information provided by me regarding my source of income / funds in this application is true."]')

    SOURCE_OF_YOUR_INCOMING_FUNDS_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("What is the source of your incoming funds?")')

    CONTINUE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Continue")

    OCCUPATION_DROPDOWN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Architect, Engineer...")')

    AIRLINE_OPTION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Airline")')

    ACCOUNTS_OPTION = (AppiumBy.ACCESSIBILITY_ID, 'Accounts')

    START_UPLOADING_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Start Uploading")')

    UPLOAD_SCREEN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Upload Proof of Work *")')

    UPLOAD_DOCUMENT = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Attach at least 1 document .pdf/.doc/.png - less than X kb")')

    I_EARN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.RectView").instance(0)')

    SOURCE_OF_FUNDS_OPTIONS = {
        'SALARY' : (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.RectView").instance(0)'),
        'FREELANCE' : (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.RectView").instance(1)'),
        'PENSION': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.RectView").instance(2)'),
        'INHERITANCE': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.RectView").instance(3)'),
        'INVESTMENT_IN_SHARES': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.RectView").instance(4)'),
        'AGRICULTURAL_INCOME': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.RectView").instance(5)'),
        'RENTAL_INCOME': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.RectView").instance(6)'),
        'INTEREST_INCOME': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.RectView").instance(7)')
    }

    NAME_OF_EMPLOYER = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)')

    LINE1 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(1)')

    LINE2 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(2)')

    CITY = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(3)')

    POSTAL_CODE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(4)')

    PROVINCE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Select province...")')

    PUNJAB = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("undefined0")')

    FUNDED_BY_SPONSOR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.RectView").instance(1)')

    SALARY_CHECKBOX = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.RectView").instance(1)')

    SCROLLABLE_LOCATOR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Choose province"))')

    EXPECTED_TURNOVER_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Expected Turnover")')

    STUDENT_OPTION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.RectView").instance(2)')

    UNEMPLOYED_OPTION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.RectView").instance(3)')

    SPONSOR_NAME_FIELD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)')

    SPONSOR_DROPDOWN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Choose Relationship with Sponsor")')

    TEXT_SISTER = (AppiumBy.ACCESSIBILITY_ID, 'Sister')

    ELIGIBLE_DOCUMENTS_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Eligible Documents")')

    NAME_OF_SPONSOR_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Name of Sponsor’s Employer *")')

    RELATIONSHIP_WITH_SPONSOR_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Your relationship with Sponsor *")')

    BACK_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("com.horcrux.svg.PathView").instance(0)')

    ERROR_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("You cannot include symbols or numbers")')

    WHAT_DO_YOU_DO_TEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("What do you do? *")')

    LINE1_FIELD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("street 5")')

    LINE2_FIELD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Apartment 4B")')

    CITY_FIELD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("sydney")')

    POSTAL_CODE_FIELD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("12345")')

    CONFIRMATION_MODAL_FOR_UPLOAD_DOCUMENTS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Ensure your income documents are up-to-date and accurate")')
