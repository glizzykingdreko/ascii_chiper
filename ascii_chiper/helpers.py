from random import randint, random
from numpy import int32

is_raspi = False
try:
    import RPi.GPIO as GPIO
    is_raspi = True
except ImportError:
    pass

class GeneratorHelper:

    @staticmethod
    def generate_seed() -> int:
        """Generate seed for key generation.

        Returns:
            int: Seed for key generation.
        """
        return int(random() * 1073741824) if is_raspi else randint(0, 1073741824 - 1)
    
    @staticmethod
    def _int32_raspi(value):
        value = int(value)
        value = value % (2**32)
        if value >= 2**31:
            value -= 2**32
        return value
    
    @staticmethod
    def int32(value):
        if is_raspi:
            return GeneratorHelper._int32_raspi(value)
        return int32(value)