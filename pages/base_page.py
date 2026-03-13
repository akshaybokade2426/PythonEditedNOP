from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import allure
from selenium.common.exceptions import TimeoutException
from utils.logger import get_logger

class BasePage:
    def __init__(self, driver):
        """
        Initialize BasePage with the WebDriver instance and our central logger.
        """
        self.driver = driver
        # Explicit wait timeout can be configured here

        self.wait = WebDriverWait(driver, 10)
        # Use our central logger, already configured in conftest.py
        self.logger = get_logger()

    @allure.step("Clicking Element: {locator}")
    def click_element(self, locator):
        try:
            element = WebDriverWait(self.driver,15).until(EC.visibility_of_element_located(locator))
            self.driver.execute_script("arguments[0].click();", element)
            self.logger.info(f"Successfully clicked element: {locator}")
        except TimeoutException:
            self.logger.error(f"Timeout: Element not clickable: {locator}")
            # Re-raise the exception to fail the test and trigger failure evidence capture
            raise


    def move_to_element(self, locator):
        element = WebDriverWait(self.driver,15).until(EC.visibility_of_element_located(locator))
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

    @allure.step("Entering text '{text}' into Element: {locator}")
    def find_element(self, locator,text,clear_first=True):
        try:
            element=WebDriverWait(self.driver,15).until(EC.visibility_of_element_located(locator))
            if clear_first:
                element.clear()
            element.send_keys(text)
            self.logger.info(f"Successfully entered text into element: {locator}")
        except TimeoutException:
            self.logger.error(f"Timeout: Element not visible for text entry: {locator}")
            raise

    def select_by_value(self,locator,value):
        element=WebDriverWait(self.driver,15).until((EC.presence_of_element_located(locator)))
        element.click()
        filter_obj=Select(element)
        filter_obj.select_by_visible_text(value)

    def just_select_by_value(self,locator,value):
        element =WebDriverWait(self.driver,15).until(EC.presence_of_element_located(locator))
        filter_obj = Select(element)
        # WebDriverWait(self.driver,15)
        filter_obj.select_by_value(value)
        element.click()

    @allure.step("Getting text from Element: {locator}")
    def element_present(self,locator):
        """
                Gets text from an element. Fails test if element not found.
                """
        try:
            element = WebDriverWait(self.driver,15).until(EC.presence_of_element_located(locator))
            value=element.text
            self.logger.info(f"Retrieved text '{value}' from element: {locator}")
            return
        except TimeoutException:
            self.logger.error(f"Timeout: Could not get text from element as it was not visible: {locator}")
            raise

    # def move_above_element(self,locator):
    #     element = self.wait.until(EC.element_to_be_clickable(locator))





    # def visiblity_of_ele(self,locator):
    #     element = WebDriverWait(self.driver,15).until(EC.visibility_of_element_located(locator))
    # #
    # def send_keys(self, locator, text, clear_first=True):
    #     """
    #     Sends keys to an element after waiting for it to be visible.
    #     Fails the test immediately if the element is not found within the timeout.
    #     """
    #     try:
    #         element = self.wait.until(EC.visibility_of_element_located(locator))
    #         if clear_first:
    #             element.clear()
    #         element.send_keys(text)
    #     finally:
    #         pass



#################################################################################added a line
