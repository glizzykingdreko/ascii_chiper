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
