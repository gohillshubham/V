"""
Configuration settings for JioMart Coupon Testing Script
"""

class Config:
    # Base coupon patterns to generate variations from
    BASE_PATTERNS = [
        "881a0eb9570ae493b60b39e71eeaa03a",
        "dde61d114db1f0aa2789816f7938f519"
    ]
    BASE_PATTERN = BASE_PATTERNS[0]  # For backward compatibility
    
    # JioMart URL configuration
    JIOMART_BASE_URL = "https://relianceretail.com/JioMart/"
    
    # Timing configuration
    FOCUS_DURATION = 2  # seconds to keep browser focused
    PAGE_LOAD_TIMEOUT = 10  # seconds to wait for page load
    
    # Browser configuration
    HEADLESS_MODE = True  # Set to True to run browser in headless mode
    
    # Performance settings
    MAX_RETRIES = 3  # Maximum retries for failed operations
    RETRY_DELAY = 1  # Delay between retries in seconds
    
    # Logging configuration
    LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
    
    # File paths
    OUTPUT_DIR = "output"
    COUPON_LOG_FILE = "tested_coupons.txt"
    ERROR_LOG_FILE = "errors.log"
    
    @classmethod
    def get_jiomart_url_with_coupon(cls, coupon_code):
        """Generate JioMart URL with coupon parameter"""
        return f"{cls.JIOMART_BASE_URL}?jiocpn={coupon_code}"
    
    @classmethod
    def validate_base_pattern(cls):
        """Validate that base pattern contains changeable characters"""
        has_digit = any(c.isdigit() for c in cls.BASE_PATTERN)
        has_letter = any(c.islower() for c in cls.BASE_PATTERN)
        
        if not (has_digit or has_letter):
            raise ValueError("Base pattern must contain at least one digit (0-9) or lowercase letter (a-z)")
        
        return True
    
    @classmethod
    def print_config(cls):
        """Print current configuration settings"""
        print("Configuration Settings:")
        print(f"  Base Pattern: {cls.BASE_PATTERN}")
        print(f"  JioMart URL: {cls.JIOMART_BASE_URL}")
        print(f"  Focus Duration: {cls.FOCUS_DURATION} seconds")
        print(f"  Page Load Timeout: {cls.PAGE_LOAD_TIMEOUT} seconds")
        print(f"  Headless Mode: {cls.HEADLESS_MODE}")
        print(f"  Max Retries: {cls.MAX_RETRIES}")
        print(f"  Log Level: {cls.LOG_LEVEL}")

# Validate configuration on import
Config.validate_base_pattern()
