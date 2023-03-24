from numpy import int32
from random import random
from typing import Any, List
from warnings import simplefilter
simplefilter("ignore", RuntimeWarning)

from .exceptions import InvalidSeedInputException

class KeyGenerator:
    """Generate key for encryption and decryption."""

    @staticmethod
    def generate_seed() -> int:
        """Generate seed for key generation.

        Returns:
            int: Seed for key generation.
        """
        return int(random() * 1073741824)
    
    def __init__(self, seed=None):
        if seed is None:
            seed = KeyGenerator.generate_seed()
        self.seed = seed

    def _xorshift_generator(self, key: int, shift: int) -> Any:
        """Generate xorshift function."""
        def inner_function():
            nonlocal key, shift
            temp_key = int32(key)
            temp_key ^= int32(temp_key << 23)
            temp_key ^= int32(temp_key >> 17)
            temp_key ^= int32(shift)
            temp_key ^= int32(shift >> 26)
            key, shift = shift, temp_key
            return (key + shift) % 0x100000000 
        return inner_function

    def create_key(self, base: int, length: int=12) -> List[int]:
        """Create key for encryption and decryption.

        Args:
            base (int): Base for key generation.
            length (int): Length of key. Default is 12.

        Returns:
            List[int]: Key for encryption and decryption.
        
        Raises:
            InvalidSeedInputException: If invalid seed input.
        """
        try:
            xorshift = self._xorshift_generator(base, self.seed)
            return [xorshift() & 255 for _ in range(length)]
        except Exception:
            raise InvalidSeedInputException("Invalid seed input")

if __name__ == '__main__':
    expected = [14, 236, 95, 36, 157, 37, 161, 162, 255, 38, 205, 36]
    keygen = KeyGenerator(123123123)
    key = keygen.create_key(9797987, 12)
    print(key == expected)
