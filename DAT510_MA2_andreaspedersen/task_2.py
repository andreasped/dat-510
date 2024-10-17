# Task II. Implementing HMAC for Authentication

from task_1 import diffie_hellman, g, p

BLOCK_SIZE = 64

# Pad the key to block size
def pad_key(key, block_size):
    # Convert key to bytes
    key_bytes = str(key).encode()

    if len(key_bytes) > block_size:
        key_bytes = xor_hash(key_bytes)
    if len(key_bytes) < block_size:
        key_bytes += bytes([0] * (block_size - len(key_bytes)))

    return key_bytes

# XOR hash function
def xor_hash(data):
    hash_value = 0
    # Bitwise XOR for each byte in data
    for byte in data:
        hash_value ^= byte
    # Final XOR result
    return bytes([hash_value])

# XOR bytes used to combine padded key with ipad and opad
def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

# HMAC Function
def hmac_xor(key, message, block_size=BLOCK_SIZE):
    if type(message) == str:
        message = message.encode()

    padded_key = pad_key(key, block_size)

    ipad = bytes([0x36] * block_size)
    opad = bytes([0x5c] * block_size)

    inner_hash = xor_hash(xor_bytes(padded_key, ipad) + message)
    outer_hash = xor_hash(xor_bytes(padded_key, opad) + inner_hash)

    # Final output is the authentication tag (outer hash)
    return outer_hash


key = diffie_hellman(p, g)
message = "Test message"
auth_tag = hmac_xor(key, message, BLOCK_SIZE)
print("Authentication tag:", auth_tag.hex())
