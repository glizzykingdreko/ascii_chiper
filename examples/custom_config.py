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
