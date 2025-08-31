#!/usr/bin/env python3
"""
JioMart Coupon Testing Script - Multi-threaded Version
High-speed concurrent coupon testing with 1000+ coupons per second
"""

import time
import signal
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import random
from coupon_generator import CouponGenerator
from browser_manager import BrowserManager
from config import Config

class JioMartCouponTester:
    def __init__(self, max_threads=20):  # Optimized for system resources
        self.coupon_generator = CouponGenerator()
        self.running = True
        self.tested_coupons = []
        self.successful_coupons = []
        self.total_tested = 0
        self.lock = threading.Lock()
        self.max_threads = max_threads
        self.target_rate = 1000  # Target: 1000 coupons per second
        self.driver_initialized = False
        self.setup_signal_handlers()
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\nReceived signal {signum}. Shutting down gracefully...")
        self.running = False
    
    def test_single_coupon(self, coupon_code):
        """Test a single coupon code on JioMart - thread-safe version"""
        browser_manager = None
        try:
            # Each thread gets its own browser manager
            browser_manager = BrowserManager()
            
            # Construct JioMart URL with coupon parameter
            url = f"{Config.JIOMART_BASE_URL}?jiocpn={coupon_code}"
            
            # Open browser and navigate to URL
            browser_manager.open_browser()
            browser_manager.navigate_to_url(url)
            
            # Wait a moment for page to fully load
            time.sleep(0.5)  # Reduced wait time for speed
            
            # Check if this is a success screen
            is_success = browser_manager.check_for_success_screen()
            
            result = {
                'coupon': coupon_code,
                'success': is_success,
                'displayed_coupon': None,
                'screenshot': None
            }
            
            if is_success:
                # Take screenshot of success
                screenshot_filename = f"success_{coupon_code}.png"
                browser_manager.take_screenshot(screenshot_filename)
                result['screenshot'] = screenshot_filename
                
                # Extract the displayed coupon from the page
                displayed_coupon = browser_manager.extract_coupon_from_page()
                result['displayed_coupon'] = displayed_coupon
                
                # Save to gotit.txt immediately
                self._save_successful_coupon(coupon_code, displayed_coupon)
                
                with self.lock:
                    self.successful_coupons.append(coupon_code)
            
            # Close browser
            browser_manager.close_browser()
            
            # Update counters thread-safely
            with self.lock:
                self.tested_coupons.append(coupon_code)
                self.total_tested += 1
                
                # Print progress every 50 tests
                if self.total_tested % 50 == 0:
                    success_count = len(self.successful_coupons)
                    print(f"Progress: {self.total_tested} tested | {success_count} successful | Latest: {coupon_code}")
            
            return result
            
        except Exception as e:
            print(f"Error testing coupon {coupon_code}: {str(e)}")
            if browser_manager:
                try:
                    browser_manager.close_browser()
                except:
                    pass
            return {'coupon': coupon_code, 'success': False, 'error': str(e)}
    
    def _save_successful_coupon(self, test_coupon, displayed_coupon):
        """Save successful coupon to gotit.txt - thread-safe"""
        try:
            with self.lock:  # Thread-safe file writing
                with open('gotit.txt', 'a') as f:
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                    if displayed_coupon:
                        f.write(f"{timestamp} | Test: {test_coupon} | Displayed: {displayed_coupon}\n")
                    else:
                        f.write(f"{timestamp} | Test: {test_coupon} | Displayed: Not extracted\n")
        except Exception as e:
            print(f"Error saving successful coupon: {e}")
    
    def generate_coupon_batch(self, batch_size):
        """Generate a batch of unique coupon codes"""
        batch = []
        for _ in range(batch_size):
            if not self.running:
                break
            coupon = self.coupon_generator.get_next_coupon()
            if coupon:
                batch.append(coupon)
            else:
                break
        return batch
    
    def run_multithreaded(self):
        """Main execution loop with multi-threading"""
        print("Starting JioMart Coupon Testing Script - MULTI-THREADED")
        print(f"Base pattern: {Config.BASE_PATTERN}")
        print("Generating random coupon variations...")
        
        # Show pattern info
        pattern_info = self.coupon_generator.get_pattern_info()
        print(f"Total possible combinations: {pattern_info['total_combinations']:,}")
        print(f"Previously visited: {pattern_info['visited_count']}")
        print(f"Remaining to test: {pattern_info['remaining_combinations']:,}")
        print(f"Target rate: {self.target_rate} coupons/second")
        print(f"Using {self.max_threads} concurrent threads")
        print("Press Ctrl+C to stop\n")
        
        start_time = time.time()
        
        try:
            with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                while self.running:
                    # Generate batch of coupons for this round
                    batch_size = min(self.max_threads * 2, 500)  # Process in batches
                    coupon_batch = self.generate_coupon_batch(batch_size)
                    
                    if not coupon_batch:
                        print("No more unique coupons to generate.")
                        break
                    
                    # Submit all coupons in batch to thread pool
                    future_to_coupon = {
                        executor.submit(self.test_single_coupon, coupon): coupon 
                        for coupon in coupon_batch
                    }
                    
                    # Process completed futures
                    for future in as_completed(future_to_coupon):
                        if not self.running:
                            break
                        
                        try:
                            result = future.result()
                            if result.get('success'):
                                print(f"🎉 SUCCESS! Coupon {result['coupon']} shows offer page!")
                        except Exception as e:
                            print(f"Thread error: {e}")
                    
                    # Rate limiting - ensure we don't overwhelm the server
                    elapsed = time.time() - start_time
                    if elapsed > 0:
                        current_rate = self.total_tested / elapsed
                        if current_rate > self.target_rate:
                            # Sleep briefly to maintain target rate
                            time.sleep(0.1)
                        
                        # Print rate statistics every 10 seconds
                        if int(elapsed) % 10 == 0 and elapsed > 9:
                            print(f"Rate: {current_rate:.1f} coupons/sec | Total: {self.total_tested} | Successful: {len(self.successful_coupons)}")
                    
        except KeyboardInterrupt:
            print("\nReceived keyboard interrupt. Stopping...")
            self.running = False
        
        finally:
            # Cleanup and print summary
            self.print_summary()
    
    def print_summary(self):
        """Print summary of tested coupons"""
        print(f"\n" + "="*60)
        print(f"FINAL SUMMARY")
        print(f"="*60)
        print(f"Total coupons tested this session: {len(self.tested_coupons)}")
        print(f"Total successful coupons found: {len(self.successful_coupons)}")
        print(f"Total coupons visited overall: {self.coupon_generator.get_visited_count()}")
        print(f"Last coupon tested: {self.tested_coupons[-1] if self.tested_coupons else 'None'}")
        
        if self.successful_coupons:
            print(f"Successful coupons:")
            for coupon in self.successful_coupons:
                print(f"  ✅ {coupon}")
        
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
            print(f"Successful coupons saved to 'gotit.txt'")
    
    def get_tested_coupons(self):
        """Return list of all tested coupons"""
        with self.lock:
            return self.tested_coupons.copy()

def main():
    """Main function"""
    print("JioMart Coupon Testing Script v2.0 - MULTI-THREADED")
    print("=" * 60)
    
    # Create tester with optimized thread count for stability and speed
    tester = JioMartCouponTester(max_threads=20)
    tester.run_multithreaded()

if __name__ == "__main__":
    main()