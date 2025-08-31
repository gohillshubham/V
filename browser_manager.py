"""
Browser Manager
Handles Selenium WebDriver operations for automated browser sessions
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
from webdriver_manager.firefox import GeckoDriverManager
from config import Config

class BrowserManager:
    def __init__(self):
        self.driver = None
        self.firefox_options = self._setup_firefox_options()
        self.service = None
    
    def _setup_firefox_options(self):
        """Setup Firefox browser options"""
        options = Options()
        
        # Performance optimizations
        options.set_preference('permissions.default.image', 2)  # Disable images
        options.set_preference('javascript.enabled', False)  # Disable JS for faster loading
        
        # Marionette stability improvements
        options.set_preference('marionette.enabled', True)
        options.set_preference('marionette.port', 0)  # Use random port
        options.set_preference('devtools.debugger.remote-enabled', True)
        
        # Window configuration
        options.add_argument('--width=1920')
        options.add_argument('--height=1080')
        
        # User agent to appear more like a regular browser
        options.set_preference('general.useragent.override', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0')
        
        # Optionally run headless for performance
        if Config.HEADLESS_MODE:
            options.add_argument('--headless')
        
        return options
    
    def _setup_firefox_service(self):
        """Setup Firefox service with GeckoDriver - use system driver to avoid rate limits"""
        try:
            # Use system geckodriver directly to avoid GitHub rate limits
            system_geckodriver = "/nix/store/w2y9xl7bnq7b8fhkp0yihmlv3438p4mh-geckodriver-0.36.0/bin/geckodriver"
            
            # Check if system driver exists
            if os.path.exists(system_geckodriver):
                service = Service(system_geckodriver)
                return service
            else:
                # Fallback to default system PATH geckodriver
                service = Service()  # Use system geckodriver from PATH
                return service
                
        except Exception as e:
            print(f"Error setting up GeckoDriver service: {e}")
            print("Please ensure Firefox browser is installed")
            raise
    
    def open_browser(self):
        """Open a new browser session"""
        try:
            if self.driver is not None:
                self.close_browser()
            
            self.service = self._setup_firefox_service()
            self.driver = webdriver.Firefox(service=self.service, options=self.firefox_options)
            
            # Execute script to remove webdriver property (Firefox specific)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return True
            
        except WebDriverException as e:
            print(f"Error opening browser: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error opening browser: {e}")
            return False
    
    def navigate_to_url(self, url):
        """Navigate to specified URL"""
        if self.driver is None:
            raise Exception("Browser not initialized. Call open_browser() first.")
        
        try:
            print(f"Navigating to: {url}")
            self.driver.get(url)
            
            # Wait for page to start loading
            WebDriverWait(self.driver, Config.PAGE_LOAD_TIMEOUT).until(
                lambda driver: driver.execute_script("return document.readyState") != "loading"
            )
            
            # Bring window to focus
            self.driver.switch_to.window(self.driver.current_window_handle)
            
            return True
            
        except TimeoutException:
            print(f"Timeout loading page: {url}")
            return False
        except WebDriverException as e:
            print(f"Error navigating to URL {url}: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error navigating to URL {url}: {e}")
            return False
    
    def close_browser(self):
        """Close current browser session"""
        try:
            if self.driver is not None:
                self.driver.quit()
                self.driver = None
            
            if self.service is not None:
                self.service = None
                
        except Exception as e:
            print(f"Error closing browser: {e}")
    
    def is_browser_open(self):
        """Check if browser is currently open"""
        try:
            if self.driver is None:
                return False
            
            # Try to get current URL to test if browser is responsive
            _ = self.driver.current_url
            return True
            
        except Exception:
            return False
    
    def get_page_title(self):
        """Get current page title"""
        if self.driver is None:
            return None
        
        try:
            return self.driver.title
        except Exception as e:
            print(f"Error getting page title: {e}")
            return None
    
    def get_current_url(self):
        """Get current page URL"""
        if self.driver is None:
            return None
        
        try:
            return self.driver.current_url
        except Exception as e:
            print(f"Error getting current URL: {e}")
            return None
    
    def take_screenshot(self, filename=None):
        """Take screenshot of current page"""
        if self.driver is None:
            return False
        
        try:
            if filename is None:
                timestamp = int(time.time())
                filename = f"screenshot_{timestamp}.png"
            
            return self.driver.save_screenshot(filename)
            
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return False
    
    def check_for_success_screen(self):
        """Check if the current page shows the coupon success screen"""
        if self.driver is None:
            return False
        
        try:
            # Check for specific text elements that indicate success
            success_indicators = [
                "Use Coupon Code given below",
                "Flat Rs. 100 Off",
                "Copy Code",
                "Start shopping on JioMart"
            ]
            
            page_source = self.driver.page_source.lower()
            
            # Check if at least 2 success indicators are present
            found_indicators = 0
            for indicator in success_indicators:
                if indicator.lower() in page_source:
                    found_indicators += 1
            
            return found_indicators >= 2
            
        except Exception as e:
            print(f"Error checking for success screen: {e}")
            return False
    
    def extract_coupon_from_page(self):
        """Extract coupon code from the success page"""
        if self.driver is None:
            return None
        
        try:
            # Look for the coupon code element - it's usually in a specific format
            # Based on the screenshot, it appears in a box/container
            potential_elements = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'coupon') or contains(text(), 'Copy Code')]/../*")
            
            for element in potential_elements:
                text = element.text.strip()
                # Coupon codes are typically alphanumeric and of certain length
                if text and len(text) >= 8 and len(text) <= 15 and text.replace(' ', '').isalnum():
                    return text.replace(' ', '').upper()
            
            return None
            
        except Exception as e:
            print(f"Error extracting coupon from page: {e}")
            return None
    
    def wait_for_element(self, by, value, timeout=10):
        """Wait for element to be present"""
        if self.driver is None:
            return None
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
            
        except TimeoutException:
            print(f"Timeout waiting for element: {by}={value}")
            return None
        except Exception as e:
            print(f"Error waiting for element: {e}")
            return None
    
    def cleanup(self):
        """Cleanup all browser resources"""
        print("Cleaning up browser resources...")
        self.close_browser()
        print("Browser cleanup completed.")
