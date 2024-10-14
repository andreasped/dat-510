# Task 5: Enhance Security with Block Ciphers
import time
import config
from task_1 import substitution_then_transposition
from task_2 import percentage_difference

caesar_key = config.caesar_key
numeric_key_list = config.numeric_key_list
original_text = config.plaintext
changed_text = "Andreas Bedersen Security and Vulnerability in Networks"
BLOCK_SIZE = 8


# Padding function for making sure the plaintext can be split up into the set block size
def pad(plaintext):
    padding_len = BLOCK_SIZE - (len(plaintext) % BLOCK_SIZE)
    if padding_len != BLOCK_SIZE:
        padding = "_" * padding_len
    else:
        padding = ""
    
    return plaintext + padding


# Function that does the ECB encryption
def ecb_block_cipher(plaintext, caesar_key, numeric_key_list):
    plaintext = plaintext.replace(" ", "")
    padded_plaintext = pad(plaintext)
    ciphertext = ""
    
    for i in range(0, len(padded_plaintext), BLOCK_SIZE):
        block = padded_plaintext[i:i + BLOCK_SIZE]
        encrypted_block = substitution_then_transposition(block, caesar_key, numeric_key_list)
        ciphertext += encrypted_block

    return ciphertext


def repeated_ecb_avalanche_effect(rounds, original_text, changed_text, caesar_key, numeric_key_list):
    original_cipher = original_text
    changed_cipher = changed_text
    avalanche_effects = []

    start_time = time.time()

    for i in range(rounds):
        original_cipher = ecb_block_cipher(original_cipher, caesar_key, numeric_key_list)
        changed_cipher = ecb_block_cipher(changed_cipher, caesar_key, numeric_key_list)
        
        difference_percentage = percentage_difference(original_cipher, changed_cipher)
        
        # Seconds
        time_taken = time.time() - start_time
        
        avalanche_effects.append({
            "round": i+1,
            "percentage_difference": difference_percentage,
            "time_taken": time_taken
        })
        
    return avalanche_effects




if __name__ == "__main__":

    rounds = 20

    results = repeated_ecb_avalanche_effect(rounds, original_text, changed_text, caesar_key, numeric_key_list)

    for result in results:
        print(f"Round {result["round"]}: {result["percentage_difference"]:.2f}% difference, Time: {result["time_taken"]:.5f} seconds")
