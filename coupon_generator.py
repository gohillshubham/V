"""
Coupon Code Generator
Generates sequential coupon codes based on pattern: 881a0eb9570ae493b60b39e71eeaa03a
"""

from config import Config

class CouponGenerator:
    def __init__(self):
        self.base_pattern = Config.BASE_PATTERN
        self.current_state = list(self.base_pattern)
        self.positions = self._identify_changeable_positions()
        self.generated_coupons = []
        self.is_exhausted = False
    
    def _identify_changeable_positions(self):
        """Identify positions of digits and letters that can be incremented"""
        positions = []
        for i, char in enumerate(self.base_pattern):
            if char.isdigit() or char.islower():
                positions.append({
                    'index': i,
                    'type': 'digit' if char.isdigit() else 'letter',
                    'current': char
                })
        return positions
    
    def _increment_character(self, char, char_type):
        """Increment a single character based on its type"""
        if char_type == 'digit':
            if char == '9':
                return '0', True  # Wrap around and carry
            else:
                return str(int(char) + 1), False
        
        elif char_type == 'letter':
            if char == 'z':
                return 'a', True  # Wrap around and carry
            else:
                return chr(ord(char) + 1), False
        
        return char, False
    
    def _increment_state(self):
        """Increment the current state to generate next coupon"""
        carry = True
        
        # Start from the rightmost changeable position
        for i in range(len(self.positions) - 1, -1, -1):
            if not carry:
                break
            
            pos_info = self.positions[i]
            current_char = self.current_state[pos_info['index']]
            
            new_char, carry = self._increment_character(current_char, pos_info['type'])
            self.current_state[pos_info['index']] = new_char
            
            # Update position info
            pos_info['current'] = new_char
        
        # If we still have carry after processing all positions, we've exhausted all combinations
        if carry:
            self.is_exhausted = True
    
    def get_next_coupon(self):
        """Generate and return the next coupon code"""
        if self.is_exhausted:
            return None
        
        # Generate current coupon
        current_coupon = ''.join(self.current_state)
        self.generated_coupons.append(current_coupon)
        
        # Increment for next time
        self._increment_state()
        
        return current_coupon
    
    def get_current_coupon(self):
        """Get current coupon without incrementing"""
        return ''.join(self.current_state)
    
    def get_generated_count(self):
        """Return count of generated coupons"""
        return len(self.generated_coupons)
    
    def get_all_generated_coupons(self):
        """Return list of all generated coupons"""
        return self.generated_coupons.copy()
    
    def reset(self):
        """Reset generator to initial state"""
        self.current_state = list(self.base_pattern)
        self.positions = self._identify_changeable_positions()
        self.generated_coupons = []
        self.is_exhausted = False
    
    def preview_next_n_coupons(self, n=5):
        """Preview next n coupons without affecting the generator state"""
        # Create a temporary generator with same state
        temp_generator = CouponGenerator()
        temp_generator.current_state = self.current_state.copy()
        temp_generator.positions = [pos.copy() for pos in self.positions]
        temp_generator.is_exhausted = self.is_exhausted
        
        preview_coupons = []
        for _ in range(n):
            coupon = temp_generator.get_next_coupon()
            if coupon is None:
                break
            preview_coupons.append(coupon)
        
        return preview_coupons
    
    def calculate_total_combinations(self):
        """Calculate total possible combinations"""
        total = 1
        for pos in self.positions:
            if pos['type'] == 'digit':
                total *= 10  # 0-9
            elif pos['type'] == 'letter':
                total *= 26  # a-z
        return total
