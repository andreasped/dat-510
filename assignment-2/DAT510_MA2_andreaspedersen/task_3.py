# Task III. Applying Encryption-Decryption
# Reference for some of the code: https://onboardbase.com/blog/aes-encryption-decryption/

from Crypto.Cipher import AES
from task_2 import hmac_xor, key, message

# Same shared secret as for HMAC
aes_key = key.to_bytes(16, byteorder="big")

# Message + HMAC tag
text_for_encryption = message + hmac_xor(key, message).hex()
print("Plaintext:", text_for_encryption)

# Encrypt text
cipher = AES.new(aes_key, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(text_for_encryption.encode())
nonce = cipher.nonce
print("Encrypted:", ciphertext.hex())

# Decrypt text
cipher = AES.new(aes_key, AES.MODE_EAX, nonce)
decrypted_message = cipher.decrypt_and_verify(ciphertext, tag).decode()
print("Decrypted:", decrypted_message)

# Verify HMAC tag
# We know the XOR hash function of HMAC returns 1 byte (2 hex characters), hence the last 2 characters of the decrypted message ([-2:])
hmac_tag_recv = decrypted_message[-2:]
print("Received HMAC tag:", hmac_tag_recv)

if hmac_tag_recv == hmac_xor(key, decrypted_message[:-2]).hex():
    print("\nHMAC tags match!")
else:
    print("\nHMAC tags do NOT match!")
