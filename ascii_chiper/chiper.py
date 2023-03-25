from typing import Dict, Union, Any, List, Tuple

from .key_generator import KeyGenerator
from .exceptions import InvalidModeException, \
    InvalidStartIndexException, InvalidEndIndexException, InvalidKeyInputException, \
        EncryptionException, DecryptionException
from .models import DecryptionModel, EncryptionModel
from .utils import swap_back, swap, xor_unshift, xor_shift, \
    deinterleave, interleave, unrotate, rotate, unxor_base, xor_base, xor_unadd, xor_add, \
        deinterleave_key, interleave_key, string_to_ascii, ascii_to_string, ascii_to_base64, \
            base64_to_ascii, clean_input, revert_clean_input, reverse

class Chiper:
    """Encrypts and decrypts messages using a key"""

    BASIC_SWAP_INTERLEAVE = [
        {"interleave": {}},
        {"swap": {}},
    ]

    ROTATE_XORSHIFT = [
        {"rotate": {"index": 5}},
        {"xor_shift": {"index": 7}},
    ]

    XORBASE_ROTATE = [
        {"xor_base": {"base": 113, "start": 0}},
        {"rotate": {"index": 3}},
    ]

    XORADD_INTERLEAVE = [
        {"xor_add": {"start": 0}},
        {"interleave": {}},
    ]

    FULL_ENCRYPTION = [
        {"interleave": {}},
        {"swap": {}},
        {"xor_shift": {"index": 0}},
        {"rotate": {"index": 0}},
        {"xor_base": {"base": 113, "start": 0}},
        {"interleave_key": {"start": 0}},
        {"reverse": {}},
    ]
    PENULTIMATE_OF_KEY = lambda k: k-1
    MIDDLE_OF_KEY = lambda k: int((k-1)/2)


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
    
    @staticmethod
    def format_step_params(step_params: Dict[str, Any], key: List[int]) -> Tuple:
        """Formats the parameters for a step.

        Args:
            step_params: The parameters to format.
            key: The key to use for formatting.

        Returns:
            Dict[str, Any]: The formatted parameters.
        """
        index, start, end, base = step_params.get('index', 0), step_params.get('start', 0), \
            step_params.get('end', len(key)), step_params.get('base', 113)
        if callable(index): index = index(len(key))
        if callable(start): start = start(len(key))
        if callable(end): end = end(len(key))
        if callable(base): base = base(len(key)) 
        if start == "PENULTIMATE_OF_KEY": start = Chiper.PENULTIMATE_OF_KEY(len(key))
        if start == "MIDDLE_OF_KEY": start = Chiper.MIDDLE_OF_KEY(len(key))
        if end == "PENULTIMATE_OF_KEY": end = Chiper.PENULTIMATE_OF_KEY(len(key))
        if end == "MIDDLE_OF_KEY": end = Chiper.MIDDLE_OF_KEY(len(key))
        if base == "PENULTIMATE_OF_KEY": base = Chiper.PENULTIMATE_OF_KEY(len(key))
        if base == "MIDDLE_OF_KEY": base = Chiper.MIDDLE_OF_KEY(len(key))
        if start < 0 or start >= len(key):
            raise InvalidStartIndexException(f"Invalid start index: {start}")
        if end < 0 or end > len(key):
            raise InvalidEndIndexException(f"Invalid end index: {end}")
        return index, start, end, base
    
    @staticmethod
    def check_inputs_types(key: List[int], base: int, len: int, steps: List[Dict[str, Any]], message: Union[str, int, Dict]) -> None:
        """Checks the types of the inputs.

        Args:
            key: The key to check.
            base: The base to check.
            len: The length of the key to check.
            steps: The steps to check.
            message: The message to check.
        """
        if base is not False and not isinstance(base, int):
            raise InvalidKeyInputException("Invalid base input: base must be an integer.")
        
        if len is not False and not isinstance(len, int):
            raise InvalidKeyInputException("Invalid len input: len must be an integer.")
        
        if not isinstance(steps, list) or not all(isinstance(step, dict) and isinstance(next(iter(step.keys())), str) and isinstance(next(iter(step.values())), dict) for step in steps):
            raise InvalidKeyInputException("Invalid steps input: steps must be a list of dictionaries in the format {str, dict}.")
        
        if not isinstance(message, (str, int, dict, list, float)):
            raise InvalidKeyInputException("Invalid message input: message must be a string, integer, float, list or dictionary.")

    def __init__(self, seed: int):
        self.seed, self.encryption_model, self.plain_text, self.base, \
            self.lenght, self.used_key, self.decrypt_model= \
                seed, False, "", 0, 0, [], False

    def encrypt(
        self, 
        message: Union[str, dict, int]=False, 
        base: int=False, 
        lenght: int=0, 
        encrypt_steps: List[Dict[str, Dict]]=False, 
        model: EncryptionModel=False,
        key: List[int]=False,
    ) -> str:
        """
        ### Encrypts a message using a key and a set of steps or a model.

        Args:
            `message` (Union[str, dict, int]): The message to encrypt. Default is False.
            `base` (int): The base for key generation. Default is False.
            `lenght` (int): The length of the key. Default is 0.
            `encrypt_steps` (List[Dict[str, Dict]]): The steps to use for encryption. Default is False.
            `model` (EncryptionModel): The model to use for encryption. Default is False.
            `key` (List[int]): The key to use for encryption. Default is False. If False, a key will be generated.
        
        Returns:
            str: The encrypted message.

        Raises:
            InvalidModeException: If the mode is invalid or missing/invalid arguments.
            InvalidKeyInputException: If one of the input keys is invalid.
            ValueError: If the message is missing.
            InvalidModeException: If the mode is invalid.
            EncryptionException: If the encryption fails.
        
        Examples:
            >>> from ascii_chiper import Chiper
            >>> chiper = Chiper(123)
            >>> chiper.encrypt("Hello World!", 113, 40, Chiper.BASIC_SWAP_INTERLEAVE)
            'xSJJSHNlQWyubF1vDyClV7RvfnKobCZkzyGUIg=='
        """
        try:
            if isinstance(message, bool):
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
        elif (not isinstance(key, list) or not all(isinstance(k, int) for k in key)):
            raise InvalidKeyInputException("Invalid key input: key must be a list of integers.")
        
        Chiper.check_inputs_types(key, base, lenght, encrypt_steps, message)
        try:
            self.encryption_model = EncryptionModel(base, lenght, encrypt_steps)
            ascii_list = string_to_ascii(clean_input(message))
            for item in encrypt_steps:
                step_name, step_params = next(iter(item.items()))

                # Initialize/parse/execute the options
                index, start, end, base = Chiper.format_step_params(step_params, key)

                # Execute the step
                if step_name == 'reverse':
                    ascii_list = reverse(ascii_list)
                elif step_name == 'swap':
                    ascii_list = swap(ascii_list)
                elif step_name == 'xor_shift':
                    ascii_list = xor_shift(ascii_list, key, index)
                elif step_name == 'rotate':
                    ascii_list = rotate(ascii_list, key, index)
                elif step_name == 'xor_base':
                    ascii_list = xor_base(ascii_list, key, base, start, end)
                elif step_name == 'xor_add':
                    ascii_list = xor_add(ascii_list, key, start, end)
                elif step_name == 'interleave':
                    ascii_list = interleave(ascii_list, key, start, end)
                elif step_name == 'interleave_key':
                    ascii_list = interleave_key(ascii_list, key, start, end)
                else: raise InvalidModeException(f"Invalid mode: {step_name}")
            
            # Save the encryption data
            self.plain_text, self.base, self.lenght, self.used_key, self.encrypt_steps = \
                message, base, lenght, key, encrypt_steps
            
            # Return the encrypted message
            return ascii_to_base64(ascii_list)
        except:
            raise EncryptionException("Encryption failed")
        

    def decrypt(
        self, 
        message: Union[str, dict, int]=False, 
        base: int=False, 
        lenght: int=0,
        decrypt_steps: Dict[str, Any]=False, 
        model: DecryptionModel=False,
        key: List[int]=False
    ) -> Union[str, dict, int]:
        """
        ### Decrypts a message using a key and a set of steps or a model.

        Args:
            `message` (Union[str, dict, int]): The message to decrypt. Default is False.
            `base` (int): The base for key generation. Default is False.
            `lenght` (int): The length of the key. Default is 0.
            `decrypt_steps` (Dict[str, Any]): The steps to use for decryption. Default is False.
            `model` (DecryptionModel): The model to use for decryption. Default is False.
            `key` (List[int]): The key to use for decryption. Default is False. If False, a key will be generated.
        
        Returns:
            The decrypted message.
        
        Raises:
            InvalidModeException: If the mode is invalid or missing/invalid arguments.
            InvalidKeyInputException: If one of the input keys is invalid.
            ValueError: If the message is missing.
            InvalidModeException: If the mode is invalid.
            DecryptionException: If the decryption failed.
        
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
        elif (not isinstance(key, list) or not all(isinstance(k, int) for k in key)):
            raise InvalidKeyInputException("Invalid key input: key must be a list of integers.")
        
        Chiper.check_inputs_types(key, base, lenght, decrypt_steps, message)
        decrypt_steps = list(reversed(decrypt_steps))
        try:
            self.decrypt_model = DecryptionModel(base, lenght, decrypt_steps)
            ascii_list = base64_to_ascii(message)
            for item in decrypt_steps:
                step_name, step_params = next(iter(item.items()))

                # Initialize/parse/execute the options
                index, start, end, base = Chiper.format_step_params(step_params, key)
                
                # Execute the step
                if step_name == 'reverse':
                    ascii_list = reverse(ascii_list)
                elif step_name == 'swap_back':
                    ascii_list = swap_back(ascii_list)
                elif step_name == 'xor_unshift':
                    ascii_list = xor_unshift(ascii_list, key, index)
                elif step_name == 'unrotate':
                    ascii_list = unrotate(ascii_list, key, index)
                elif step_name == 'unxor_base':
                    ascii_list = unxor_base(ascii_list, key, base, start, end)
                elif step_name == 'xor_unadd':
                    ascii_list = xor_unadd(ascii_list, key, start, end)
                elif step_name == 'deinterleave':
                    ascii_list = deinterleave(ascii_list, key)
                elif step_name == 'deinterleave_key':
                    ascii_list = deinterleave_key(ascii_list, key, start, end)
                else: raise InvalidModeException(f"Invalid mode: {step_name}")
            
            # Save the decryption data
            self.plain_text, self.base, self.lenght, self.used_key, self.decrypt_steps = \
                message, base, lenght, key, decrypt_steps
            
            # Return the decrypted message
            return revert_clean_input(ascii_to_string(ascii_list))
        except:
            raise DecryptionException("Decryption failed")