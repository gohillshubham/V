"""
Coupon Code Generator
Generates random coupon codes based on pattern: 881a0eb9570ae493b60b39e71eeaa03a
Uses visited tracking to avoid duplicates
"""

import random
import string
import os
from config import Config

class CouponGenerator:
    def __init__(self):
        self.base_pattern = Config.BASE_PATTERN
        self.positions = self._identify_changeable_positions()
        self.generated_coupons = []
        self.visited_file = "visited.txt"
        self.visited_coupons = self._load_visited_coupons()
    
    def _identify_changeable_positions(self):
        """Identify positions of digits and letters that can be changed"""
        positions = []
        for i, char in enumerate(self.base_pattern):
            if char.isdigit() or char.islower():
                positions.append({
                    'index': i,
                    'type': 'digit' if char.isdigit() else 'letter',
                    'original': char
                })
        return positions
    
    def _load_visited_coupons(self):
        """Load previously visited coupons from file"""
        visited = set()
        if os.path.exists(self.visited_file):
            try:
                with open(self.visited_file, 'r') as f:
                    for line in f:
                        coupon = line.strip()
                        if coupon:
                            visited.add(coupon)
                print(f"Loaded {len(visited)} previously visited coupons")
            except Exception as e:
                print(f"Error loading visited coupons: {e}")
        return visited
    
    def _save_visited_coupon(self, coupon):
        """Save a visited coupon to file"""
        try:
            with open(self.visited_file, 'a') as f:
                f.write(f"{coupon}\n")
            self.visited_coupons.add(coupon)
        except Exception as e:
            print(f"Error saving visited coupon: {e}")
    
    def _generate_random_character(self, char_type):
        """Generate a random character based on type"""
        if char_type == 'digit':
            return random.choice(string.digits)  # 0-9
        elif char_type == 'letter':
            return random.choice(string.ascii_lowercase)  # a-z
        return None
    
    def _generate_random_coupon(self):
        """Generate a random coupon based on the pattern - COMMENTED OUT FOR NEW APPROACH"""
        # coupon_chars = list(self.base_pattern)
        # 
        # # Replace changeable positions with random values
        # for pos_info in self.positions:
        #     random_char = self._generate_random_character(pos_info['type'])
        #     if random_char:  # Ensure we have a valid character
        #         coupon_chars[pos_info['index']] = random_char
        # 
        # return ''.join(coupon_chars)
        
        # NEW APPROACH: Generate systematic patterns with same character distribution
        return self._generate_systematic_coupon()
    
    def get_next_coupon(self):
        """Generate and return the next random coupon code that hasn't been visited"""
        max_attempts = 10000  # Prevent infinite loops
        attempts = 0
        
        while attempts < max_attempts:
            # Generate a random coupon
            coupon = self._generate_random_coupon()
            
            # Check if it hasn't been visited before
            if coupon not in self.visited_coupons:
                # Save it as visited
                self._save_visited_coupon(coupon)
                self.generated_coupons.append(coupon)
                return coupon
            
            attempts += 1
        
        # If we've tried too many times, return None
        print(f"Warning: Could not generate unique coupon after {max_attempts} attempts")
        return None
    
    def _analyze_base_pattern(self):
        """Analyze the base pattern to understand character distribution"""
        # Base: 881a0eb9570ae493b60b39e71eeaa03a
        digits = []
        letters = []
        
        for i, char in enumerate(self.base_pattern):
            if char.isdigit():
                digits.append((i, char))
            elif char.islower():
                letters.append((i, char))
        
        return digits, letters
    
    def _generate_systematic_coupon(self):
        """Generate coupon with same length/distribution but different systematic approach"""
        # Analyze original pattern
        digits, letters = self._analyze_base_pattern()
        
        # Create different systematic patterns
        patterns = [
            self._pattern_sequential(),
            self._pattern_blocks(),
            self._pattern_alternating(),
            self._pattern_mirrored(),
            self._pattern_fibonacci_like()
        ]
        
        # Choose a random pattern approach
        selected_pattern = random.choice(patterns)
        return selected_pattern
    
    def _pattern_sequential(self):
        """Sequential incremental pattern"""
        coupon = ['0'] * 32  # Start with 32 chars
        
        # Fill digit positions (same count as original)
        digit_positions = [0, 1, 2, 4, 6, 8, 9, 13, 15, 16, 18, 20, 22, 25, 29, 30]
        letter_positions = [3, 5, 7, 10, 11, 12, 14, 17, 19, 21, 23, 24, 26, 27, 28, 31]
        
        # Generate sequential digits
        for i, pos in enumerate(digit_positions):
            coupon[pos] = str(i % 10)
        
        # Generate sequential letters  
        for i, pos in enumerate(letter_positions):
            coupon[pos] = chr(ord('a') + (i % 26))
        
        return ''.join(coupon)
    
    def _pattern_blocks(self):
        """Block-based pattern"""
        coupon = ['0'] * 32
        
        # Create blocks of similar characters
        digit_positions = [0, 1, 2, 4, 6, 8, 9, 13, 15, 16, 18, 20, 22, 25, 29, 30]
        letter_positions = [3, 5, 7, 10, 11, 12, 14, 17, 19, 21, 23, 24, 26, 27, 28, 31]
        
        # Fill with block patterns
        block_digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        block_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']
        
        for i, pos in enumerate(digit_positions):
            coupon[pos] = block_digits[i % len(block_digits)]
        
        for i, pos in enumerate(letter_positions):
            coupon[pos] = block_letters[i % len(block_letters)]
        
        return ''.join(coupon)
    
    def _pattern_alternating(self):
        """Alternating high/low values"""
        coupon = ['0'] * 32
        
        digit_positions = [0, 1, 2, 4, 6, 8, 9, 13, 15, 16, 18, 20, 22, 25, 29, 30]
        letter_positions = [3, 5, 7, 10, 11, 12, 14, 17, 19, 21, 23, 24, 26, 27, 28, 31]
        
        # Alternate between high and low digits
        for i, pos in enumerate(digit_positions):
            coupon[pos] = '9' if i % 2 == 0 else '1'
        
        # Alternate between high and low letters
        for i, pos in enumerate(letter_positions):
            coupon[pos] = 'z' if i % 2 == 0 else 'a'
        
        return ''.join(coupon)
    
    def _pattern_mirrored(self):
        """Mirror pattern around center"""
        coupon = ['0'] * 32
        
        digit_positions = [0, 1, 2, 4, 6, 8, 9, 13, 15, 16, 18, 20, 22, 25, 29, 30]
        letter_positions = [3, 5, 7, 10, 11, 12, 14, 17, 19, 21, 23, 24, 26, 27, 28, 31]
        
        # Create mirror patterns
        mid = len(digit_positions) // 2
        for i, pos in enumerate(digit_positions):
            if i < mid:
                coupon[pos] = str(i % 10)
            else:
                mirror_i = len(digit_positions) - 1 - i
                coupon[pos] = str(mirror_i % 10)
        
        mid = len(letter_positions) // 2
        for i, pos in enumerate(letter_positions):
            if i < mid:
                coupon[pos] = chr(ord('a') + (i % 26))
            else:
                mirror_i = len(letter_positions) - 1 - i
                coupon[pos] = chr(ord('a') + (mirror_i % 26))
        
        return ''.join(coupon)
    
    def _pattern_fibonacci_like(self):
        """Fibonacci-like progression"""
        coupon = ['0'] * 32
        
        digit_positions = [0, 1, 2, 4, 6, 8, 9, 13, 15, 16, 18, 20, 22, 25, 29, 30]
        letter_positions = [3, 5, 7, 10, 11, 12, 14, 17, 19, 21, 23, 24, 26, 27, 28, 31]
        
        # Fibonacci-like sequence for digits
        fib_digits = [1, 1, 2, 3, 5, 8, 3, 1, 4, 5, 9, 4, 3, 7, 0, 7]
        for i, pos in enumerate(digit_positions):
            coupon[pos] = str(fib_digits[i % len(fib_digits)])
        
        # Letter progression
        letter_prog = [0, 1, 1, 2, 3, 5, 8, 13, 21, 8, 3, 11, 14, 25, 13, 12]
        for i, pos in enumerate(letter_positions):
            coupon[pos] = chr(ord('a') + (letter_prog[i % len(letter_prog)] % 26))
        
        return ''.join(coupon)
    
    def get_generated_count(self):
        """Return count of generated coupons in this session"""
        return len(self.generated_coupons)
    
    def get_visited_count(self):
        """Return total count of visited coupons (including from previous sessions)"""
        return len(self.visited_coupons)
    
    def get_all_generated_coupons(self):
        """Return list of all generated coupons in this session"""
        return self.generated_coupons.copy()
    
    def reset_session(self):
        """Reset only the current session (not visited history)"""
        self.generated_coupons = []
    
    def clear_visited_history(self):
        """Clear all visited coupon history (use with caution)"""
        try:
            if os.path.exists(self.visited_file):
                os.remove(self.visited_file)
            self.visited_coupons = set()
            print("Visited coupon history cleared")
        except Exception as e:
            print(f"Error clearing visited history: {e}")
    
    def calculate_total_combinations(self):
        """Calculate total possible combinations"""
        total = 1
        for pos in self.positions:
            if pos['type'] == 'digit':
                total *= 10  # 0-9
            elif pos['type'] == 'letter':
                total *= 26  # a-z
        return total
    
    def get_pattern_info(self):
        """Get information about the coupon pattern"""
        info = {
            'pattern': self.base_pattern,
            'total_length': len(self.base_pattern),
            'changeable_positions': len(self.positions),
            'total_combinations': self.calculate_total_combinations(),
            'visited_count': len(self.visited_coupons),
            'remaining_combinations': self.calculate_total_combinations() - len(self.visited_coupons)
        }
        return info