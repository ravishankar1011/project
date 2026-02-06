from appium.options.android import UiAutomator2Options

class dcaps:
    def __init__(self):
        self.options = UiAutomator2Options()
        self.options.platform_name = "Android"
        self.options.automation_name = "UiAutomator2"
        self.options.app_package = "pk.hugobank.test"
        self.options.app_activity = "com.hugosave.SplashActivity"
        self.options.auto_grant_permissions = True
        self.options.no_sign = True
        self.options.no_reset = False
        self.options.full_reset = False

    def get_options(self):
        return self.options