# Task IV. Implementing Single Ratchet for Chain Key

from task_1 import diffie_hellman, p, g
import hmac
import hashlib

# Ratchet the chain key using HMAC
def ratchet_chain_key(Kchain):
    return hmac.new(Kchain, b"ratchet", hashlib.sha256).digest()

# Derive message key from chain key
def derive_message_key(Kchain):
    return hmac.new(Kchain, b"message", hashlib.sha256).digest()

# Sending message: ratchet chain key, derive message key, authenticate message
def send_message(Kchain, message):
    # Ratchet the chain key
    Kchain = ratchet_chain_key(Kchain)

    # Message key
    Kmessage = derive_message_key(Kchain)
    
    # Use the message key for authentication of the message
    auth_tag = hmac.new(Kmessage, message.encode(), hashlib.sha256).digest()
    
    return Kchain, auth_tag


if __name__ == "__main__":
    # Chain key init with shared secret from Diffie-Hellman
    shared_secret = diffie_hellman(p, g).to_bytes(32, byteorder="big")
    Kchain = hmac.new(shared_secret, b"initialization", hashlib.sha256).digest()
    
    print(f"Initial Kchain: {Kchain.hex()}")
    
    # Send the messages
    messages = ["Hello Bob!", "How are you?", "Had lunch?"]
    for msg in messages:
        Kchain, auth_tag = send_message(Kchain, msg)
        print(f"\nMessage: {msg}       Auth tag: {auth_tag.hex()}")
        print(f"New Kchain: {Kchain.hex()}")
