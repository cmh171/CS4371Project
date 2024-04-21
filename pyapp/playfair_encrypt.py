# Christopher Hanly 04/19/2024
# CS 4371 Project
# Playfair Encryption for IOT handling. 
# The encryption end handles for cases of repeated characters in succession
# e.g. the ls in "hello". However, decryption does not handle the removal
# of padding for these cases. Therefore, the decrypted plaintext will still
# include the padding characters.

import sys
import numpy as np

# boilerplate find_position function to get position of a char from matrix
def find_position(char, matrix):
    for i, row in enumerate(matrix):
        if char in row:
            return (i, row.index(char))
    return None

# playfair_encrypt
# using algorithm given in Alex's lecture.
# On good run, returns a string of encrypted text
# On bad runs, void return
def playfair_encrypt(plain, key):
    # key length max of 25 letters
    max_key_length = 25

    if len(key) > max_key_length:
        print ("Key must be 25 characters long or less.")
        return
    if not key.isalpha():
        print ("Key must not contain any numbers or symbols.")
        return
    if not plain.isalpha():
        print ("Plaintext must not contain any numbers or symbols.")
        return
    
    # reformat plaintext and key
    key = key.upper().replace(" ","")
    plain = plain.upper().replace(" ","")

    # processing the key into playfair-friendly
    
    # remove duplicate letters from the key
    seen = set()
    processed_key = [x for x in key if not (x in seen or seen.add(x))]

    # alphabet with J removed per playfair convention
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

    # take all characters that are in the alphabet, but not the key
    remaining_letters = [x for x in alphabet if x not in seen]

    # create a set of characters starting with processed_key and
    # then remaining alphabet. 
    final_chars = processed_key + remaining_letters

    # initialize 5x5 key matrix
    key_matrix = [[None]*5 for _ in range(5)]

    # starting filling key matrix with our processed playfair alphabet
    index = 0
    for i in range(5):
        for j in range(5):
            if index < len(final_chars):
                key_matrix[i][j] = final_chars[index]
                index += 1

    # for debugging
    for row in key_matrix:
        print(row)

    # starting processing plaintext string
    # handle for repeated characters
    adjusted_plain = ""
    last_char = ""
    for char in plain:
        if char == last_char:
            adjusted_plain += 'X' if char != 'X' else 'Q' # Add 'X' or 'Q' between repeated characters
        adjusted_plain += char
        last_char = char

    # handle for odd number of characters. Using Z for padding.
    appended_char_flag = 0
    if len(adjusted_plain) %2 != 0:
        plain += 'Z'
        appended_char_flag = 1
    
    encrypted_text = ""

    for i in range(0, len(adjusted_plain), 2):
        char1 = plain[i]
        char2 = plain[i+1]

        row1, col1 = find_position(char1, key_matrix)
        row2, col2 = find_position(char2, key_matrix)

        # Case 1 of Playfair algo
        if row1 == row2:
            # Same row: shift right
            col1 = (col1 + 1) % 5
            col2 = (col2 + 1) % 5
        
        # Case 2 of Playfair algo
        elif col1 == col2:
            # Same column: shift down
            row1 = (row1 + 1) % 5
            row2 = (row2 + 1) % 5
        
        # Case 3 of Playfair algo
        else:
            # Rectangle swap: swap columns
            col1, col2 = col2, col1

        # Append shifted characters to encrypted string
        encrypted_text += key_matrix[row1][col1] + key_matrix[row2][col2]

    # if odd number of chars present in plaintext, trims encrypted string
    if appended_char_flag == 1:
        encrypted_text = encrypted_text[:-1]

    return encrypted_text