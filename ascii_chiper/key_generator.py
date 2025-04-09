from random import random, randint
from typing import Any, List
from warnings import simplefilter
simplefilter("ignore", RuntimeWarning)

from .exceptions import InvalidSeedInputException
from .helpers import GeneratorHelper

class KeyGenerator:
    """Generate key for encryption and decryption."""

    @staticmethod
    def generate_seed() -> int:
        """Generate seed for key generation.

        Returns:
            int: Seed for key generation.
        """
        return GeneratorHelper.generate_seed()
    
    def __init__(self, seed: int=None):
        if seed is None:
            seed = KeyGenerator.generate_seed()
        self.seed = seed

    def _xorshift_generator(self, initial_key: int, initial_shift: int) -> Any:
        """Generate xorshift function.
        
        Args:
            initial_key: The initial key value for the generator
            initial_shift: The initial shift value for the generator
            
        Returns:
            A function that generates the next number in the sequence
        """
        def inner_function():
            nonlocal initial_key, initial_shift
            
            # Convert to signed 32-bit integers (like JavaScript)
            current_key = initial_key & 0xFFFFFFFF
            if current_key & 0x80000000:
                current_key = current_key - 0x100000000
            
            current_shift = initial_shift & 0xFFFFFFFF
            if current_shift & 0x80000000:
                current_shift = current_shift - 0x100000000

            # Store shift value for later use
            shift_value = current_shift
            # Start with the current key value
            result_value = current_key

            # Perform operations maintaining signed 32-bit arithmetic
            result_value = (result_value ^ ((result_value << 23) & 0xFFFFFFFF)) & 0xFFFFFFFF
            if result_value & 0x80000000:
                result_value = result_value - 0x100000000

            result_value = (result_value ^ ((result_value >> 17) & 0xFFFFFFFF)) & 0xFFFFFFFF
            if result_value & 0x80000000:
                result_value = result_value - 0x100000000

            result_value = (result_value ^ shift_value) & 0xFFFFFFFF
            if result_value & 0x80000000:
                result_value = result_value - 0x100000000

            result_value = (result_value ^ ((shift_value >> 26) & 0xFFFFFFFF)) & 0xFFFFFFFF
            if result_value & 0x80000000:
                result_value = result_value - 0x100000000

            # Update state for next iteration
            initial_shift = result_value
            initial_key = shift_value

            # Calculate final value
            final_value = (shift_value + result_value) & 0xFFFFFFFF
            if final_value & 0x80000000:
                final_value = final_value - 0x100000000
            return final_value & 0xFFFFFFFF
        return inner_function

    def create_key(self, base: int, length: int = 12) -> List[int]:
        try:
            xorshift = self._xorshift_generator(base, self.seed)
            return [xorshift() & 0xFF for _ in range(length)]
        except Exception:
            raise InvalidSeedInputException("Invalid seed input")
if __name__ == '__main__':
    expected = [14, 236, 95, 36, 157, 37, 161, 162, 255, 38, 205, 36]
    keygen = KeyGenerator(123123123)
    key = keygen.create_key(9797987, 12)
    print(key == expected)
