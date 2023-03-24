from ascii_chiper import Chiper, DecryptionModel, \
    EncryptionModel

# Initialize the Chiper
chiper = Chiper.initialize()

# Encrypt a message using multiple encryption configurations
message = "Testing encryption configurations."

# Create encryption models
base1, length1 = 24681357, 224
encryption_model1 = EncryptionModel(base1, length1, Chiper.BASIC_SWAP_INTERLEAVE)
encryption_model2 = EncryptionModel(base1, length1, Chiper.ROTATE_XORSHIFT)
encryption_model3 = EncryptionModel(base1, length1, Chiper.XORBASE_ROTATE)
encryption_model4 = EncryptionModel(base1, length1, Chiper.XORADD_INTERLEAVE)
encryption_model5 = EncryptionModel(base1, length1, Chiper.FULL_ENCRYPTION)

encrypted_message1 = chiper.encrypt(message, model=encryption_model1)
encrypted_message2 = chiper.encrypt(message, base1, length1, encrypt_steps=Chiper.ROTATE_XORSHIFT)
encrypted_message3 = chiper.encrypt(message, base1, length1, encrypt_steps=Chiper.XORBASE_ROTATE)
encrypted_message4 = chiper.encrypt(message, base1, length1, encrypt_steps=Chiper.XORADD_INTERLEAVE)
encrypted_message5 = chiper.encrypt(message, base1, length1, encrypt_steps=Chiper.FULL_ENCRYPTION)

print("Original message:", message)
print("Encrypted message 1:", encrypted_message1)
print("Encrypted message 2:", encrypted_message2)
print("Encrypted message 3:", encrypted_message3)
print("Encrypted message 4:", encrypted_message4)
print("Encrypted message 5:", encrypted_message5)

# Decrypt the encrypted message
decrypted_message1 = chiper.decrypt(encrypted_message1, model=DecryptionModel.from_encryption_model(encryption_model1))
decrypted_message2 = chiper.decrypt(encrypted_message2, model=DecryptionModel.from_encryption_model(encryption_model2))
decrypted_message3 = chiper.decrypt(encrypted_message3, model=DecryptionModel.from_encryption_model(encryption_model3))
decrypted_message4 = chiper.decrypt(encrypted_message4, model=DecryptionModel.from_encryption_model(encryption_model4))
decrypted_message5 = chiper.decrypt(encrypted_message5, model=DecryptionModel.from_encryption_model(encryption_model5))

print("Decrypted message 1:", decrypted_message1)
print("Decrypted message 2:", decrypted_message2)
print("Decrypted message 3:", decrypted_message3)
print("Decrypted message 4:", decrypted_message4)
print("Decrypted message 5:", decrypted_message5)