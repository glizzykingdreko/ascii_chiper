from typing import Any, Dict, Tuple

from .utils import OPPOSITE_ENCRYPTION_FUNCTIONS
from .exceptions import InvalidModelException

class DecryptionModel:
    """A model for decryption and encryption steps."""

    @staticmethod
    def from_encryption_model(model: Any) -> "DecryptionModel":
        """Creates a decryption model from an encryption model.

        Args:
            model: The encryption model to use.

        Returns:
            DecryptionModel: The decryption model.
        """
        try:
            new_steps = []
            for d in model.encrypt_steps:
                key, value = next(iter(d.items()))
                if not key in list(OPPOSITE_ENCRYPTION_FUNCTIONS): continue
                new_steps.append({OPPOSITE_ENCRYPTION_FUNCTIONS[key].__name__: value})
            return DecryptionModel(model.base, model.lenght, new_steps)
        except Exception as e:
            raise InvalidModelException(f"Invalid model: {e}")

    def __init__(self, base: int, lenght: int, decrypt_steps: Dict[str, Any]):
        self.base = base
        self.lenght = lenght
        self.decrypt_steps = decrypt_steps
    
    def __call__(self) -> Tuple:
        return self.base, self.lenght, self.decrypt_steps

class EncryptionModel:
    """A model for encryption and decryption steps."""

    @staticmethod
    def from_decryption_model(model: Any) -> "EncryptionModel":
        """Creates an encryption model from a decryption model.

        Args:
            model: The decryption model to use.

        Returns:
            EncryptionModel: The encryption model.
        """
        try:
            new_steps = []
            for d in model.encrypt_steps:
                key, value = next(iter(d.items()))
                if not key in list(OPPOSITE_ENCRYPTION_FUNCTIONS): continue
                new_steps.append({OPPOSITE_ENCRYPTION_FUNCTIONS[key].__name__: value})
            return EncryptionModel(model.base, model.lenght, new_steps)
        except Exception as e:
            raise InvalidModelException(f"Invalid model: {e}")

    def __init__(self, base: int, lenght: int, encrypt_steps: Dict[str, Any]):
        self.base = base
        self.lenght = lenght
        self.encrypt_steps = encrypt_steps
    
    def __call__(self) -> Tuple:
        return self.base, self.lenght, self.encrypt_steps
