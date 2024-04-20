import sys
import numpy as np

# boilerplate find_position function to return row, col of a character
def find_position(char, matrix):
    for i, row in enumerate(matrix):
        if char in row:
            return (i, row.index(char))
    return None

# playfair_decrypt
# same as playfair_encrypt, but in the shift phase has inverted steps
def playfair_decrypt(cipher, key):
    # key length max of 25 letters
    max_key_length = 25

    if len(key) > max_key_length:
        print ("Key must be 25 characters long or less.")
        return
    if not key.isalpha():
        print ("Key must not contain any numbers or symbols.")
        return
    if not cipher.isalpha():
        print ("Plaintext must not contain any numbers or symbols.")
        return
    
    # reformat plaintext and key
    key = key.upper().replace(" ","")
    cipher = cipher.upper().replace(" ","")

    # initializations for playfair cipher
    seen = set()
    processed_key = [x for x in key if not (x in seen or seen.add(x))]

    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    remaining_letters = [x for x in alphabet if x not in seen]

    final_chars = processed_key + remaining_letters

    key_matrix = [[None]*5 for _ in range(5)]

    # starting filling key matrix
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
    appended_char_flag = 0
    if len(cipher) %2 != 0:
        cipher += 'X'
        appended_char_flag = 1
    
    plain_text = ""

    for i in range(0, len(cipher), 2):
        char1 = cipher[i]
        char2 = cipher[i+1]

        row1, col1 = find_position(char1, key_matrix)
        row2, col2 = find_position(char2, key_matrix)

        # inverse of Case #1 shift from powerpoint
        if row1 == row2:
            # Same row: shift right
            col1 = (col1 - 1) % 5
            col2 = (col2 - 1) % 5
        
        # inverse of Case #2 shift from powerpoint
        elif col1 == col2:
            # Same column: shift down
            row1 = (row1 - 1) % 5
            row2 = (row2 - 1) % 5
        
        # Case #3 shift from powerpoint (xy swap doesn't need inversion)
        else:
            # Rectangle swap: swap columns
            col1, col2 = col2, col1

        plain_text += key_matrix[row1][col1] + key_matrix[row2][col2]

    # if odd number of chars in encrypted text, trim tail
    if appended_char_flag == 1:
        plain_text = plain_text[:-1]

    return plain_text