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