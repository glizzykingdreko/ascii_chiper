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

### Hello World
```python
from ascii_chiper import Chiper

# Initialize the Chiper
chiper = Chiper(123)

encrypted = chiper.encrypt("Hello World!", 113, 40, Chiper.BASIC_SWAP_INTERLEAVE)
print(f"Encrypted: {encrypted}")
# Output 'xSJJSHNlQWyubF1vDyClV7RvfnKobCZkzyGUIg=='

decrypted = chiper.decrypt(encrypted)
print(f"Decrypted: {decrypted}")
# Output 'Hello World!'
```

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
custom_config = [
    {"interleave": {}},
    {"swap": {}},
    {"rotate": {"index": 5}},
    {"xor_base": {"base": 137, "start": 0}},
]

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
custom_config = [
    {"interleave": {}},
    {"rotate": {"index": 2}},
    {"xor_add": {"start": 0}},
]

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

### Custom configuration with lambda functions
```python
from ascii_chiper import Chiper, EncryptionModel, DecryptionModel

# Initialize the Chiper
chiper = Chiper.initialize()

# Encrypt a message using a custom encryption configuration
message = "A custom encryption example."
base, length = 987654321, 92
custom_config = [
    {"swap": {}},
    {"rotate": {
        # We can use a lambda function to define the index
        # the len of the key is passed as the first argument
        "index": lambda key: key % 5,
    }},
    {"xor_base": {
        "base": 137,
        # We can use predefined functions as well
        "start": Chiper.MIDDLE_OF_KEY,
        "end": Chiper.PENULTIMATE_OF_KEY,
    }},
]

encrypted_message = chiper.encrypt(message, base, length, encrypt_steps=custom_config)

# Decrypt the encrypted message using a DecryptionModel
decryption_model = DecryptionModel.from_encryption_model(EncryptionModel(base, length, custom_config))
decrypted_message = chiper.decrypt(encrypted_message, model=decryption_model)

print("Original message:", message)
print("Encrypted message:", encrypted_message)
print("Decrypted message:", decrypted_message)
```

### Decrypt message by knowing key and steps
```python
from ascii_chiper import Chiper, EncryptionModel, DecryptionModel

# Decrypt a message using a custom encryption configuration
encrypted = "2tqBEWERKhGjI3qxKsFLuaMbWhNaybG5s5IqkmrKapJyyypDm6IqklrBmrlrWSq5WyuBkmrKymJqoZoTarErYqOBG6l6yyoiaqLKkqOqOhNaU3paq9ObE5ODKpqTy1pSq4taQ2Oxm1qryyvDe4NrC0q6qwtbWYGLMpIqYnILW9ObyxtiY5FKU3KhaoOrgavTq8taoptZEZJh6hHaEYkRYSMqsaPBerkqG0sTo8lauVqSsZKzyiqSastqQ3KiKpKbwSq5WlmauWsrKpJbmoFTq8F7InqiK1NqksoTMqIqYlLDehOLg0u5e7kqUmKLgYuby1pag5p7g6uTKwtqupsLWqmri1tDOoNCIyrTMsuaU6upG1NyoRqDcstq03qaC2KjuVqSm1lb6ZvqEdphCxGDg0tjCxtLo3N7g3kzI2ERKhGjI3qxKsFLuaMbWhNaybG5s5IqkmrKapJyyypDm6IqklrBmrlrWSq5WyuBkmrKymJqoZoTarErYqOBG6l6yyoiaqLKkqOqOhNaU3paq9ObE5ODKpqTy1pSq4taQ2Oxm1qryyvDe4NrC0q6qwtbWYGLMpIqYnILW9ObyxtiY5FKU3KhaoOrgavTq8taoptZEZJh6hHaK6Ojw4N5MyNhESoRoyN6sSrBS7mjG1oTWsmxubOSKpJqymqScssqQ5uiKpJawZq5a1kquVsrgZKrmntTesErImqiylMykioTUqJ6YovDSxN7gyq5YrmBUpuLWouDy3taq5org2qTmwtauqsLW6k6i0JDKoMyI5rTq8sbU3KpGlNyoWqDessL06OaWmKbuVuSm1kR6erq"
used_encrypt_steps = [
    {"swap": {}},
    {"xor_shift": {}}
]
used_key = [114,114]
excepted_output = [["0","Edt6O8E7ictbK9K76RvREYMRMyNhETsRE8K7S+m7EekR0YMLY4MbS6MLe0t5cyODETMRYUtbGjKKOzubsprSEyrJKquhK6lKsyuxepoamWIau+kq0RFLEaNzkysLc2ljI4NpM0uzuyuTK+sR"],["1","Edt6O8E7ictbK9K76RvREYMRMyNhETsRE8K7S+m7EekR0Sujo8ODeTMjYRFbETJLOxqbipo7E7LJ0qsqKypKoSuperMasWKau5kqGhHpEdFzSyujc5NjC4NpMyOzaStLK7sRk+s="],["application/pdf","Edt6O8E7ictbK9K76RvREYMRMyNhETsRE8K7S+m7EekR0YMLY4MbS6MLe0t5cyODETMRYUtbGjKKOzubsprSEyrJKquhK6lKsyuxepoamWIau+kq0RFLEaNzkysLc2ljI4NpM0uzuyuTK+sR"],["text/pdf","Edt6O8E7ictbK9K76RvREYMRMyNhETsRE8K7S+m7EekR0Sujo8ODeTMjYRFbETJLOxqbipo7E7LJ0qsqKypKoSuperMasWKau5kqGhHpEdFzSyujc5NjC4NpMyOzaStLK7sRk+s="]]

# Create the EncryptionModel
enc_model = EncryptionModel(0, 0, encrypt_steps=used_encrypt_steps)

# Initialize the Chiper
chiper = Chiper.initialize()

# Decrypt the encrypted message
decrypted_message = chiper.decrypt(encrypted, key=used_key, decrypt_steps=DecryptionModel.from_encryption_model(enc_model).decrypt_steps)
print("Decrypted message:", decrypted_message)
print(f"Decrypted message is equal to excepted output: {decrypted_message == excepted_output}")
# Have fun :P those looks like some mime_types encrypted
```
For other examples usages, please refer to the Examples folder.

## Encryption Methods

`ascii_chiper` offers various encryption techniques that can be combined in different configurations to achieve the desired level of security:

| Name            | Description                                          | Optional Parameters                 |
|-----------------|------------------------------------------------------|-------------------------------------|
| reverse         | Reverse the input data.                              |                                     |
| swap            | Swaps pairs of characters in the input data.         |                                     |
| rotate          | Rotates the input data by a specified index from the key. | Index from key to use           |
| interleave      | Interleaves the input data, effectively rearranging the characters. | key start/end                 |
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
