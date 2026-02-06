from appium.options.android import UiAutomator2Options


class dcaps:
    def __init__(self):
        # Initialize the Appium capabilities
        self.options = UiAutomator2Options()
        # Set the desired capabilities for the Appium session
        self.options.platform_name = "Android"
        self.options.automation_name = "UiAutomator2"
        self.options.app_package = "com.hugosave.nonprod"
        self.options.app_activity = "com.hugosave.SplashActivity"
        self.options.auto_grant_permissions = True
        # self.options.app = "/home/developer/automation/tests/ui/ui_automation/nonprod_13052025.apk"  # Read
        self.options.app = "/Users/abhishekkumarsingh/Downloads/nonprod_13052025.apk"  # Read
        # from argument
        self.options.no_sign = True
        self.options.no_reset = False
        self.options.full_reset = False

    def get_options(self):
        return self.options
