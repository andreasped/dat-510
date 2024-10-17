# Task I. Implementing Diffie-Hellman

import random

# Modular exponentiation function
def mod_exp(base, exp, mod):
    return pow(base, exp, mod)


# Diffie-Hellman function
def diffie_hellman(p, g):
    alice_private = random.randint(1, p-1)
    bob_private = random.randint(1, p-1)

    alice_public = mod_exp(g, alice_private, p)
    bob_public = mod_exp(g, bob_private, p)
    
    # Shared secrets
    alice_shared_secret = mod_exp(bob_public, alice_private, p)
    bob_shared_secret = mod_exp(alice_public, bob_private, p)
    
    # Check if shared secrets are the same
    if alice_shared_secret == bob_shared_secret:
        return alice_shared_secret
    else:
        return "Shared secret is NOT the same"
    

# Shared public parameters
p = 353
g = 3

shared_secret = diffie_hellman(p, g)
print("Shared secret:", shared_secret)
