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
