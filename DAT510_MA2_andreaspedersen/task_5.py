# Task V. Implementing Double Ratchet for Diffie-Hellman

import hmac
import hashlib
import random
from task_1 import p, g, mod_exp
from task_4 import ratchet_chain_key, send_message

# Function for generating DH key pair
def generate_dh_key_pair():
    private_key = random.randint(1, p-1)
    public_key = mod_exp(g, private_key, p)
    return private_key, public_key

# Function for deriving shared secret
def dh_shared_secret(their_public_key, our_private_key):
    return mod_exp(their_public_key, our_private_key, p)

# Double Ratchet function
def double_ratchet(our_private_key, their_public_key, Kroot):
    # Perform DH key exchange and derive new shared secret
    shared_secret = dh_shared_secret(their_public_key, our_private_key)
    
    # Derive new root key from previous root key and shared secret
    Kroot = hmac.new(Kroot, shared_secret.to_bytes(16, "big"), hashlib.sha256).digest()
    
    # Generate new chain keys (sending and receiving)
    send_chain_key = hmac.new(Kroot, b"send_chain", hashlib.sha256).digest()
    recv_chain_key = hmac.new(Kroot, b"recv_chain", hashlib.sha256).digest()

    return send_chain_key, recv_chain_key, Kroot


if __name__ == "__main__":
    # Initial DH keys and shared secret
    alice_private_key, alice_public_key = generate_dh_key_pair()
    bob_private_key, bob_public_key = generate_dh_key_pair()
    shared_secret = dh_shared_secret(bob_public_key, alice_private_key)

    # Initializing the root key and the first chain keys
    Kroot = hmac.new(shared_secret.to_bytes(16, "big"), b"initialization", hashlib.sha256).digest()
    send_chain_key = hmac.new(Kroot, b"send_chain", hashlib.sha256).digest()
    recv_chain_key = hmac.new(Kroot, b"recv_chain", hashlib.sha256).digest()

    print(f"Initial Kroot: {Kroot.hex()}")

    # Send messages
    messages = ["Hello Bob!", "How are you?", "What's up?", "Had a good day?"]

    for index, msg in enumerate(messages):
        if index > 0 and index % 2 == 0:
            # New DH exchange after every 2 messages
            alice_private_key, alice_public_key = generate_dh_key_pair()
            bob_private_key, bob_public_key = generate_dh_key_pair()
            
            # Derive new root and chain keys based on new DH exchange
            send_chain_key, recv_chain_key, Kroot = double_ratchet(alice_private_key, bob_public_key, Kroot)
            
            print(f"\n\nNew Kroot: {Kroot.hex()}")
        
        send_chain_key, auth_tag = send_message(send_chain_key, msg)
        print(f"\nMessage: {msg}       Auth tag: {auth_tag.hex()}")
        send_chain_key = ratchet_chain_key(send_chain_key)
        print(f"New send_chain_key: {send_chain_key.hex()}")
