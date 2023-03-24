from typing import Dict, Union, Any, List

from .key_generator import KeyGenerator
from .exceptions import InvalidKeyException, InvalidModeException, \
    InvalidStartIndexException, InvalidEndIndexException, InvalidBaseException, InvalidKeyInputException, \
        EncryptionException, DecryptionException
from .models import DecryptionModel, EncryptionModel
from .utils import swap_back, swap, xor_unshift, xor_shift, \
    deinterleave, interleave, unrotate, rotate, unxor_base, xor_base, xor_unadd, xor_add, \
        deinterleave_key, interleave_key, string_to_ascii, ascii_to_string, ascii_to_base64, \
            base64_to_ascii, clean_input, revert_clean_input, reverse

class Chiper:
    """Encrypts and decrypts messages using a key"""

    BASIC_SWAP_INTERLEAVE = {
        "interleave": {},
        "swap": {},
    }

    ROTATE_XORSHIFT = {
        "rotate": {"index": 5},
        "xor_shift": {"index": 7},
    }

    XORBASE_ROTATE = {
        "xor_base": {"base": 113, "start": 0},
        "rotate": {"index": 3},
    }

    XORADD_INTERLEAVE = {
        "xor_add": {"start": 0},
        "interleave": {},
    }

    FULL_ENCRYPTION = {
        "interleave": {},
        "swap": {},
        "xor_shift": {"index": 0},
        "rotate": {"index": 0},
        "xor_base": {"base": 113, "start": 0},
        "interleave_key": {"start": 0},
        "reverse": {},
    }

    @staticmethod
    def initialize() -> "Chiper":
        """Initializes a Chiper object with a random key.

        Returns:
            Chiper: A Chiper object with a random key.
        """
        return Chiper(KeyGenerator.generate_seed())
    
    @staticmethod
    def encrypt_from_model(message: str, seed: int, model: Union[EncryptionModel, DecryptionModel]) -> str:
        """Encrypts a message using a model.

        Args:
            message: The message to encrypt.
            seed: The seed to use for key generation.
            model: The model to use for encryption.

        Returns:
            str: The encrypted message.
        """
        return Chiper(seed).encrypt(message, *model())

    def __init__(self, seed: int):
        self.seed, self.encryption_model, self.plain_text, self.base, \
            self.lenght, self.used_key, self.decrypt_model= \
                seed, False, "", 0, 0, [], False

    def encrypt(
        self, 
        message: Union[str, dict, int]=False, 
        base: int=False, 
        lenght: int=0, 
        encrypt_steps: Dict[str, Any]=False, 
        model: EncryptionModel=False,
        key: List[int]=False,
    ) -> str:
        """
        ### Encrypts a message using a key and a set of steps or a model.

        Args:
            `message` (Union[str, dict, int]): The message to encrypt. Default is False.
            `base` (int): The base for key generation. Default is False.
            `lenght` (int): The length of the key. Default is 0.
            `encrypt_steps` (Dict[str, Any]): The steps to use for encryption. Default is False.
            `model` (EncryptionModel): The model to use for encryption. Default is False.
            `key` (List[int]): The key to use for encryption. Default is False. If False, a key will be generated.
        
        Returns:
            str: The encrypted message.

        Raises:
            InvalidModeException: If the mode is invalid or missing/invalid arguments.
            InvalidKeyInputException: If the key input is invalid.
        
        Examples:
            >>> from ascii_chiper import Chiper
            >>> chiper = Chiper(123)
            >>> chiper.encrypt("Hello World!", 113, 40, Chiper.BASIC_SWAP_INTERLEAVE)
            'xSJJSHNlQWyubF1vDyClV7RvfnKobCZkzyGUIg=='
        """
        try:
            if not message:
                if not self.plain_text:
                    raise ValueError("Missing message")
                message = self.plain_text
            if model:
                base, lenght, encrypt_steps = model()
            elif not encrypt_steps or not base or not lenght:
                if self.decrypt_model:
                    base, lenght, encrypt_steps = EncryptionModel.from_decryption_model(self.decrypt_model)()
                elif not key:
                    raise ValueError("Missing arguments")
        except: raise InvalidModeException("Invalid mode or missing/invalid arguments")
        if not key:
            try: key = KeyGenerator(self.seed).create_key(base, lenght)
            except: raise InvalidKeyInputException("Invalid key input")
        try:
            self.encryption_model = EncryptionModel(base, lenght, encrypt_steps)
            ascii_list = string_to_ascii(clean_input(message))
            for step_name, step_params in encrypt_steps.items():
                index, start, end, base = step_params.get('index', 0), step_params.get('start', 0), \
                    step_params.get('end', len(key)), step_params.get('base', 113)
                if step_name == 'reverse':
                    ascii_list = reverse(ascii_list)
                elif step_name == 'swap':
                    ascii_list = swap(ascii_list)
                elif step_name == 'xor_shift':
                    if index < 0 or index > len(key):
                        raise InvalidStartIndexException("Invalid start index")
                    ascii_list = xor_shift(ascii_list, key, index)
                elif step_name == 'rotate':
                    if index < 0 or index > len(key):
                        raise InvalidStartIndexException("Invalid start index")
                    ascii_list = rotate(ascii_list, key, index)
                elif step_name == 'xor_base':
                    if start < 0 or start > len(key):
                        raise InvalidStartIndexException("Invalid start index")
                    if end < 0 or end > len(key):
                        raise InvalidEndIndexException("Invalid end index")
                    if base < 0:
                        raise InvalidBaseException("Invalid base")
                    ascii_list = xor_base(ascii_list, key, base, start, end)
                elif step_name == 'xor_add':
                    if start < 0 or start > len(key):
                        raise InvalidStartIndexException("Invalid start index")
                    if end < 0 or end > len(key):
                        raise InvalidEndIndexException("Invalid end index")
                    ascii_list = xor_add(ascii_list, key, start, end)
                elif step_name == 'interleave':
                    if len(key) < len(ascii_list):
                        raise InvalidKeyException("Key is too short")
                    ascii_list = interleave(ascii_list, key)
                elif step_name == 'interleave_key':
                    if start < 0 or start > len(key):
                        raise InvalidStartIndexException("Invalid start index")
                    if end < 0 or end > len(key):
                        raise InvalidEndIndexException("Invalid end index")
                    ascii_list = interleave_key(ascii_list, key, start, end)
                else: raise InvalidModeException(f"Invalid mode: {step_name}")
            self.plain_text, self.base, self.lenght, self.used_key, self.encrypt_steps = \
                message, base, lenght, key, encrypt_steps
            return ascii_to_base64(ascii_list)
        except:
            raise EncryptionException("Encryption failed")
        

    def decrypt(
        self, message: 
        str=False, 
        base: int=False, 
        lenght: int=0,
        decrypt_steps: Dict[str, Any]=False, 
        model: DecryptionModel=False,
        key: List[int]=False
    ) -> Union[str, dict, int]:
        """
        ### Decrypts a message using a key and a set of steps or a model.

        Args:
            `message` (str): The message to decrypt. Default is False.
            `base` (int): The base for key generation. Default is False.
            `lenght` (int): The length of the key. Default is 0.
            `decrypt_steps` (Dict[str, Any]): The steps to use for decryption. Default is False.
            `model` (DecryptionModel): The model to use for decryption. Default is False.
            `key` (List[int]): The key to use for decryption. Default is False. If False, a key will be generated.
        
        Returns:
            The decrypted message.
        
        Raises:
            InvalidModeException: If the mode is invalid or missing/invalid arguments.
            InvalidKeyInputException: If the key input is invalid.
        
        Examples:
            >>> from ascii_chiper import Chiper
            >>> chiper = Chiper(123)
            >>> encrypted = chiper.encrypt("Hello World!", 113, 40, Chiper.BASIC_SWAP_INTERLEAVE)
            >>> chiper.decrypt(encrypted)
            'Hello World!'
        """
        try:
            if not message:
                if not self.plain_text:
                    raise ValueError("Missing message")
                message = self.plain_text
            if model:
                base, lenght, decrypt_steps = model()
            elif not decrypt_steps or not base or not lenght:
                if self.encryption_model:
                    base, lenght, decrypt_steps = DecryptionModel.from_encryption_model(self.encryption_model)()
                elif not key:
                    raise ValueError("Missing arguments")
        except: raise InvalidModeException("Invalid mode or missing/invalid arguments")
        if not key:
            try: key = KeyGenerator(self.seed).create_key(base, lenght)
            except: raise InvalidKeyInputException("Invalid key input")
        decrypt_steps = {k: value for k, value in reversed(decrypt_steps.items())}
        try:
            self.decrypt_model = DecryptionModel(base, lenght, decrypt_steps)
            ascii_list = base64_to_ascii(message)
            for step_name, step_params in decrypt_steps.items():
                index, start, end, base = step_params.get('index', 0), step_params.get('start', 0), \
                    step_params.get('end', len(key)), step_params.get('base', 113)
                if step_name == 'reverse':
                    ascii_list = reverse(ascii_list)
                elif step_name == 'swap_back':
                    ascii_list = swap_back(ascii_list)
                elif step_name == 'xor_unshift':
                    if index < 0 or index > len(key):
                        raise InvalidStartIndexException("Invalid start index")
                    ascii_list = xor_unshift(ascii_list, key, index)
                elif step_name == 'unrotate':
                    if index < 0 or index > len(key):
                        raise InvalidStartIndexException("Invalid start index")
                    ascii_list = unrotate(ascii_list, key, index)
                elif step_name == 'unxor_base':
                    if start < 0 or start > len(key):
                        raise InvalidStartIndexException("Invalid start index")
                    if end < 0 or end > len(key):
                        raise InvalidEndIndexException("Invalid end index")
                    if base < 0:
                        raise InvalidBaseException("Invalid base")
                    ascii_list = unxor_base(ascii_list, key, base, start, end)
                elif step_name == 'xor_unadd':
                    if start < 0 or start > len(key):
                        raise InvalidStartIndexException("Invalid start index")
                    if end < 0 or end > len(key):
                        raise InvalidEndIndexException("Invalid end index")
                    ascii_list = xor_unadd(ascii_list, key, start, end)
                elif step_name == 'deinterleave':
                    ascii_list = deinterleave(ascii_list, key)
                elif step_name == 'deinterleave_key':
                    if start < 0 or start > len(key):
                        raise InvalidStartIndexException("Invalid start index")
                    if end < 0 or end > len(key):
                        raise InvalidEndIndexException("Invalid end index")
                    ascii_list = deinterleave_key(ascii_list, key, start, end)
                else: raise InvalidModeException(f"Invalid mode: {step_name}")
            self.plain_text, self.base, self.lenght, self.used_key, self.decrypt_steps = \
                message, base, lenght, key, decrypt_steps
            return revert_clean_input(ascii_to_string(ascii_list))
        except:
            raise DecryptionException("Decryption failed")