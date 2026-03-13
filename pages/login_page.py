# pages/login_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage # Import the BasePage

class LoginPage(BasePage): # Make LoginPage inherit from BasePage
    """
    Page Object for the Sauce Labs Demo login page (saucedemo.com).
    """
    # --- Element Locators for saucedemo.com ---
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE_CONTAINER = (By.CSS_SELECTOR, "h3[data-test='error']")
    INVENTORY_PAGE_HEADER = (By.CLASS_NAME, "app_logo") # Element on the page after successful login

    def __init__(self, driver):
        # This calls the constructor of the BasePage to set up the driver, logger, etc.
        super().__init__(driver)

    def login(self, username, password):
        """
        Performs a full login action using methods inherited from BasePage.
        """
        self.logger.info(f"Attempting to log in with username: {username}")
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        # Note: We don't need to return True/False. If any step fails, an exception will be raised.

    def is_login_successful(self):
        """
        Checks if login was successful by looking for an element on the inventory page.
        Uses the is_visible method inherited from BasePage.
        """
        return self.is_visible(self.INVENTORY_PAGE_HEADER, timeout=5)

    def get_error_message(self):
        """Gets the text of the login error message."""
        if self.is_visible(self.ERROR_MESSAGE_CONTAINER, timeout=5):
            # Uses the get_text method inherited from BasePage
            return self.get_text(self.ERROR_MESSAGE_CONTAINER)
        return "No error message found."