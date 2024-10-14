# Task 1: Apply Encryption
import numpy as np
import config

plaintext = config.plaintext
numeric_key = config.numeric_key
numeric_key_list = config.numeric_key_list
caesar_key = config.caesar_key


# Substitution cipher (caesar cipher)
def caesar_cipher(text, key):
    text = text.replace(" ", "")
    text = text.upper()
    cipher_text = ""

    for letter in text:
        if letter.isupper():
            # If it is an actual letter, do the shift, then append to ciphertext
            # Numbers, symbols and spaces are not checked, only alphabet characters
            cipher_text += chr((ord(letter) + key - 65) % 26 + 65)
        else:
            # If it is not a letter, just append letter to ciphertext
            cipher_text += letter

    return cipher_text


# Transposition cipher (row transposition)
def row_transposition_ciper(text, key):
    text = text.replace(" ", "")
    text = text.upper()
    
    # Calculate the number of columns and rows
    num_cols = len(key)
    num_rows = int(np.ceil(len(text) / num_cols))

    # Pad the text with underscores
    padded_text = text.ljust(num_rows * num_cols, '_')

    # Makes the 2D matrix with the padded text determined by rows and cols
    grid = np.array(list(padded_text)).reshape(num_rows, num_cols)

    sorted_indices = np.argsort(key)

    # Selects columns in the order given by the sorted indices 
    cipher_grid = grid[:, sorted_indices]
    
    # Makes the cipher text into a 1D string 
    cipher_text = "".join(cipher_grid.T.flatten())

    # Remove the padded underscores after cipher is done
    cipher_text = cipher_text.replace("_", "")
    
    return cipher_text


# Option A
def transposition_then_substitution(text, caesar_key, numeric_key_list):
    # First transposition
    row_transposition_ciper_text = row_transposition_ciper(text, numeric_key_list)
    # print(f"Row cipher: {row_transposition_ciper_text}")

    # Then substitution
    caesar_cipher_text = caesar_cipher(row_transposition_ciper_text, caesar_key)
    # print(f"Caesar cipher: {caesar_cipher_text}")

    return caesar_cipher_text


# Option B
def substitution_then_transposition(text, caesar_key, numeric_key_list):
    # First substitution
    caesar_cipher_text = caesar_cipher(text, caesar_key)
    # print(f"Caesar cipher: {caesar_cipher_text}")

    # Then transposition
    row_transposition_ciper_text = row_transposition_ciper(caesar_cipher_text, numeric_key_list)
    # print(f"Row cipher: {row_transposition_ciper_text}")

    return row_transposition_ciper_text




if __name__ == "__main__":

    # Option A
    print("Option A: ")
    print(transposition_then_substitution(plaintext, caesar_key, numeric_key_list))

    print("\n")

    # Option B
    print("Option B: ")
    print(substitution_then_transposition(plaintext, caesar_key, numeric_key_list))
