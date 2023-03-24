# ascii_chiper
`ascii_chiper `is a Python module for encrypting and decrypting strings, integers, and dictionaries using various encryption techniques. The module provides user-friendly and customizable encryption configurations to suit different use cases and levels of security.

## Features
- Accepts strings, integers, and dictionaries as input for encryption
- Supports multiple encryption techniques, including swapping, XOR shifting, interleaving, rotation, XOR base, XOR addition, and interleaving with key
- Offers pre-configured encryption configurations for quick use
- Allows users to create custom encryption configurations

## Installation
To install the ascii_chiper module, use pip: 
```
pip install ascii_chiper
```

## Usage

This module is designed to be simple and easy to use. To get started, import the `Chiper` class and initialize an instance of it. You can then use the `encrypt` and `decrypt` methods to encrypt and decrypt your data.

The `encrypt` method takes the data to be encrypted, a base key, a length, and an encryption configuration as input. You can use one of the predefined encryption configurations or create your own custom configuration. The `decrypt` method requires the encrypted data, base key, length, and the same encryption configuration used during encryption.

### Basic usage
```python
from ascii_chiper import Chiper

# Initialize the Chiper
chiper = Chiper.initialize()

# Encrypt a message using a default encryption configuration
message = "This is a test message."
base, length = 123456789, 5
encrypted_message = chiper.encrypt(message, base, length, encrypt_steps=Chiper.XORBASE_ROTATE)

# Decrypt the encrypted message
decrypted_message = chiper.decrypt(encrypted_message)

print("Original message:", message)
print("Encrypted message:", encrypted_message)
print("Decrypted message:", decrypted_message)
```

### Custom configuration
```python
from ascii_chiper import Chiper, EncryptionModel, DecryptionModel

# Initialize the Chiper
chiper = Chiper.initialize()

# Encrypt a message using a custom encryption configuration
message = "A custom encryption example."
base, length = 987654321, 92
custom_config = {
    "interleave": {},
    "swap": {},
    "rotate": {"index": 5},
    "xor_base": {"base": 137, "start": 0},
}

encrypted_message = chiper.encrypt(message, base, length, encrypt_steps=custom_config)

# Decrypt the encrypted message using a DecryptionModel
decryption_model = DecryptionModel.from_encryption_model(EncryptionModel(base, length, custom_config))
decrypted_message = chiper.decrypt(encrypted_message, model=decryption_model)

print("Original message:", message)
print("Encrypted message:", encrypted_message)
print("Decrypted message:", decrypted_message)
```

### Advanced usage
```python
from ascii_chiper import Chiper, KeyGenerator, \
    EncryptionModel, DecryptionModel

# Custom encryption configuration
custom_config = {
    "interleave": {},
    "rotate": {"index": 2},
    "xor_add": {"start": 0},
}

# Create an encryption seed and model
seed = KeyGenerator.generate_seed()
encryption_model = EncryptionModel(123456789, 52, custom_config)

# Encrypt a message using a custom encryption configuration
message = {
    "example": True,
    "message": "This is a test message."
}
encrypted_message = Chiper(seed).encrypt(message, model=encryption_model)

# Decrypt the encrypted message using a DecryptionModel
decryption_model = DecryptionModel.from_encryption_model(encryption_model)
decrypted_message = Chiper(seed).decrypt(encrypted_message, model=decryption_model)

print("Original message:", message)
print("Encrypted message:", encrypted_message)
print("Decrypted message:", decrypted_message)
```
For other examples usages, please refer to the Examples folder.

## Encryption Methods

`ascii_chiper` offers various encryption techniques that can be combined in different configurations to achieve the desired level of security:

| Name            | Description                                          | Optional Parameters                 |
|-----------------|------------------------------------------------------|-------------------------------------|
| swap            | Swaps pairs of characters in the input data.         |                                     |
| rotate          | Rotates the input data by a specified index from the key. | Index from key to use           |
| interleave      | Interleaves the input data, effectively rearranging the characters. |                             |
| interleave_key  | Interleaves the input data based on the key start and end positions. | key start/end                 |
| xor_shift       | Applies an XOR shift operation using a specified index from the key. | index of key to use           |
| xor_base        | Performs XOR operation on the input data using the base and the key start and end positions. | base to use, start/end key to use |
| xor_add         | Adds the key start and end values to the input data using XOR addition. | start/end key to use         |

You can combine these encryption methods in a custom configuration to suit your specific requirements.

## Encryption Configurations
In addition to creating your own custom encryption configurations, `ascii_chiper` provides several pre-configured encryption configurations that cater to different use cases and security levels:

- **BASIC_SWAP_INTERLEAVE**: A simple configuration that combines Swap and Interleave encryption methods for basic security.
- **ROTATE_XORSHIFT**: Combines the Rotate and XorShift methods for an intermediate level of security.
- **XORBASE_ROTATE**: Combines the XorBase and Rotate methods for enhanced security.
- **XORADD_INTERLEAVE**: Combines the XorAdd and Interleave methods for a higher level of security.
- **FULL_ENCRYPTION**: Uses all available encryption methods for maximum security.

Remember to use the same encryption configuration for both encryption and decryption to ensure proper functionality.

## Personal Thoughts

I hope you find this module useful. This module is the exact Python implementation of the encryption method used by a well-known web anti-bot system. If you know what I'm talking about, you'll definitely find it useful. 
Please feel free to contact me for any help or suggestions via [Email](mailto:glizzykingdreko@protonmail.com) or [Twitter](https://mobile.twitter.com/glizzykingdreko). I appreciate your feedback and contributions to the project.

## License
This project is licensed under the MIT [License](LICENSE). See the LICENSE file for more details.

## My links
- [Project repository](https://github.com/glizzykingdreko/ascii_chiper)
- [GitHub](https://github.com/glizzykingdreko)
- [Twitter](https://mobile.twitter.com/glizzykingdreko)
- [Medium](https://medium.com/@glizzykingdreko)
- [Email](mailto:glizzykingdreko@protonmail.com)
