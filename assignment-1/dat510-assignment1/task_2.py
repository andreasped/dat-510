# Task 2: Evaluate the Avalanche Effect
import time
import config
from task_1 import substitution_then_transposition

caesar_key = config.caesar_key
numeric_key_list = config.numeric_key_list
original_text = config.plaintext
changed_text = "Andreas Bedersen Security and Vulnerability in Networks"


# Step 1: Initial Avalanche Effect Analysis
def percentage_difference(cipher1, cipher2):
    # Make sure the shortest cipher is considered, but they should be equal in length
    length = min(len(cipher1), len(cipher2))
    
    differences = 0

    for i in range(length):
        if cipher1[i] != cipher2[i]:
            differences += 1
        
    return (differences / length) * 100


# Step 2: Repeated Avalanche Effect Analysis
def repeated_avalanche_effect(rounds, original_text, changed_text, caesar_key, numeric_key_list):
    original_cipher = original_text
    changed_cipher = changed_text
    avalanche_effects = []

    start_time = time.time()

    for i in range(rounds):
        original_cipher = substitution_then_transposition(original_cipher, caesar_key, numeric_key_list)
        changed_cipher = substitution_then_transposition(changed_cipher, caesar_key, numeric_key_list)

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

    # Step 1
    original_cipher = substitution_then_transposition(original_text, caesar_key, numeric_key_list)
    changed_cipher = substitution_then_transposition(changed_text, caesar_key, numeric_key_list)

    difference_percentage = percentage_difference(original_cipher, changed_cipher)

    print(f"Original Ciphertext: {original_cipher}")
    print(f"Changed Ciphertext:  {changed_cipher}")
    print(f"\nPercentage Difference: {difference_percentage:.2f}%")

    print("\n")

    # Step 2
    rounds = 20

    results = repeated_avalanche_effect(rounds, original_text, changed_text, caesar_key, numeric_key_list)

    for result in results:
        print(f"Round {result["round"]}: {result["percentage_difference"]:.2f}% difference, Time: {result["time_taken"]:.5f} seconds")
