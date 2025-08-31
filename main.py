#!/usr/bin/env python3
"""
JioMart Coupon Testing Script
Main entry point for automated coupon code testing
"""

import time
import signal
import sys
from coupon_generator import CouponGenerator
from browser_manager import BrowserManager
from config import Config

class JioMartCouponTester:
    def __init__(self):
        self.coupon_generator = CouponGenerator()
        self.browser_manager = BrowserManager()
        self.running = True
        self.tested_coupons = []
        self.setup_signal_handlers()
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\nReceived signal {signum}. Shutting down gracefully...")
        self.running = False
    
    def test_coupon(self, coupon_code):
        """Test a single coupon code on JioMart"""
        try:
            print(f"Testing coupon: {coupon_code}")
            
            # Construct JioMart URL with coupon parameter
            url = f"{Config.JIOMART_BASE_URL}?jiocpn={coupon_code}"
            
            # Open browser and navigate to URL
            self.browser_manager.open_browser()
            self.browser_manager.navigate_to_url(url)
            
            # Wait a moment for page to fully load
            time.sleep(1)
            
            # Check if this is a success screen
            is_success = self.browser_manager.check_for_success_screen()
            
            if is_success:
                print(f"🎉 SUCCESS! Coupon {coupon_code} shows offer page!")
                
                # Take screenshot of success
                screenshot_filename = f"success_{coupon_code}.png"
                self.browser_manager.take_screenshot(screenshot_filename)
                
                # Extract the displayed coupon from the page
                displayed_coupon = self.browser_manager.extract_coupon_from_page()
                
                # Save to gotit.txt
                self._save_successful_coupon(coupon_code, displayed_coupon)
            
            # Close browser
            self.browser_manager.close_browser()
            
            # Store the tested coupon
            self.tested_coupons.append(coupon_code)
            
            status = "SUCCESS ✅" if is_success else "No offer"
            print(f"Completed testing coupon: {coupon_code} ({status}) (Total tested: {len(self.tested_coupons)})")
            
        except Exception as e:
            print(f"Error testing coupon {coupon_code}: {str(e)}")
            # Ensure browser is closed even on error
            self.browser_manager.close_browser()
    
    def _save_successful_coupon(self, test_coupon, displayed_coupon):
        """Save successful coupon to gotit.txt"""
        try:
            with open('gotit.txt', 'a') as f:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                if displayed_coupon:
                    f.write(f"{timestamp} | Test: {test_coupon} | Displayed: {displayed_coupon}\n")
                else:
                    f.write(f"{timestamp} | Test: {test_coupon} | Displayed: Not extracted\n")
        except Exception as e:
            print(f"Error saving successful coupon: {e}")
    
    def run(self):
        """Main execution loop"""
        print("Starting JioMart Coupon Testing Script")
        print(f"Base pattern: {Config.BASE_PATTERN}")
        print("Generating random coupon variations...")
        
        # Show pattern info
        pattern_info = self.coupon_generator.get_pattern_info()
        print(f"Total possible combinations: {pattern_info['total_combinations']:,}")
        print(f"Previously visited: {pattern_info['visited_count']}")
        print(f"Remaining to test: {pattern_info['remaining_combinations']:,}")
        print("Press Ctrl+C to stop\n")
        
        try:
            while self.running:
                # Generate next coupon code
                coupon_code = self.coupon_generator.get_next_coupon()
                
                if coupon_code is None:
                    print("All possible coupon combinations have been generated.")
                    break
                
                # Test the coupon
                self.test_coupon(coupon_code)
                
        except KeyboardInterrupt:
            print("\nReceived keyboard interrupt. Stopping...")
            self.running = False
        
        finally:
            # Cleanup
            self.browser_manager.cleanup()
            self.print_summary()
    
    def print_summary(self):
        """Print summary of tested coupons"""
        print(f"\nSummary:")
        print(f"Total coupons tested this session: {len(self.tested_coupons)}")
        print(f"Total coupons visited overall: {self.coupon_generator.get_visited_count()}")
        print(f"Last coupon tested: {self.tested_coupons[-1] if self.tested_coupons else 'None'}")
        
        # Get pattern information
        pattern_info = self.coupon_generator.get_pattern_info()
        print(f"Pattern: {pattern_info['pattern']}")
        print(f"Total possible combinations: {pattern_info['total_combinations']:,}")
        print(f"Remaining combinations: {pattern_info['remaining_combinations']:,}")
        
        # Save tested coupons to file for reference
        if self.tested_coupons:
            with open('tested_coupons.txt', 'w') as f:
                for coupon in self.tested_coupons:
                    f.write(f"{coupon}\n")
            print(f"Tested coupons saved to 'tested_coupons.txt'")
            print(f"Visited coupons automatically saved to 'visited.txt'")
            print(f"Successful coupons (if any) saved to 'gotit.txt'")
    
    def get_tested_coupons(self):
        """Return list of all tested coupons"""
        return self.tested_coupons.copy()

def main():
    """Main function"""
    print("JioMart Coupon Testing Script v1.0")
    print("=" * 50)
    
    tester = JioMartCouponTester()
    tester.run()

if __name__ == "__main__":
    main()
