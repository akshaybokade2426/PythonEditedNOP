"""
WebDriver manager utility.
Handles WebDriver initialization and configuration.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from utils.logger import get_logger
from config.environment import Environment


class DriverManager:
    """
    WebDriver manager class for handling browser initialization and configuration.
    """
    
    def __init__(self):
        """
        Initialize DriverManager with environment configuration.
        """
        self.logger = get_logger()
        self.env = Environment()
        self.browser_config = self.env.get_browser_config()
    
    def get_driver(self):
        """
        Get configured WebDriver instance.
        
        Returns:
            WebDriver: Configured WebDriver instance
        """
        browser = self.browser_config['default'].lower()
        headless = self.browser_config['headless']
        
        if browser == 'chrome':
            return self._setup_chrome_driver(headless)
        elif browser == 'firefox':
            return self._setup_firefox_driver(headless)
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    
    def _setup_chrome_driver(self, headless=False):
        """
        Setup Chrome WebDriver with options.
        
        Args:
            headless: Whether to run in headless mode
            
        Returns:
            WebDriver: Chrome WebDriver instance
        """
        try:
            options = ChromeOptions()
            
            if headless:
                options.add_argument('--headless')
            
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-web-security')
            options.add_argument('--allow-running-insecure-content')
            
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
            self._configure_driver(driver)
            self.logger.info("Chrome WebDriver initialized successfully")
            return driver
            
        except Exception as e:
            self.logger.error(f"Error initializing Chrome WebDriver: {str(e)}")
            raise
    
    def _setup_firefox_driver(self, headless=False):
        """
        Setup Firefox WebDriver with options.
        
        Args:
            headless: Whether to run in headless mode
            
        Returns:
            WebDriver: Firefox WebDriver instance
        """
        try:
            options = FirefoxOptions()
            
            if headless:
                options.add_argument('--headless')
            
            options.add_argument('--width=1920')
            options.add_argument('--height=1080')
            
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
            
            self._configure_driver(driver)
            self.logger.info("Firefox WebDriver initialized successfully")
            return driver
            
        except Exception as e:
            self.logger.error(f"Error initializing Firefox WebDriver: {str(e)}")
            raise
    
    def _configure_driver(self, driver):
        """
        Configure WebDriver with common settings.
        
        Args:
            driver: WebDriver instance to configure
        """
        try:
            driver.maximize_window()
            driver.implicitly_wait(self.browser_config['implicit_wait'])
            driver.set_page_load_timeout(self.browser_config['page_load_timeout'])
            self.logger.info("WebDriver configured with common settings")
        except Exception as e:
            self.logger.error(f"Error configuring WebDriver: {str(e)}")
            raise 