from random import randint
import tkinter as tk
from tkinter import ttk, messagebox
from itertools import cycle

win=tk.Tk()
win.title("Encryption_Decryption_Algorithm")

# Create a dictionary for lowercase letters
# Dictionaries for character encoding
letter_to_index  = {chr(i + 97): i for i in range(26)}  # a:0, b:1, ..., z:25
index_to_letter = {i: chr(i + 97) for i in range(26)}  # 0:a, 1:b, ..., 25:z

# Function to find the modular multiplicative inverse
def mod_inverse(key, m):
    for i in range(1, m):
        if (key * i) % m == 1:
            return i
    return None  # If no inverse exists

# Function to encrypt the plain text using multiplicative cipher (lowercase only)
def encrypt_multiplicative(plain_text, key):
    encrypted_text = ""
    for char in plain_text:
        if char in letter_to_index:  # Check if char is a lowercase letter
            current_index = letter_to_index[char]
            new_index = (current_index * key) % 26
            encrypted_text += index_to_letter[new_index]
    return encrypted_text

# Function to decrypt the cipher text using multiplicative cipher (lowercase only)
def decrypt_multiplicative(cipher_text, key):
    decrypted_text = ""
    inv_key = mod_inverse(key, 26)
    if inv_key is None:
        raise ValueError("Key is not valid; it must be coprime with 26.")
    for char in cipher_text:
        if char in letter_to_index:  # Check if char is a lowercase letter
            current_index = letter_to_index[char]
            new_index = (current_index * inv_key) % 26
            decrypted_text += index_to_letter[new_index]
    return decrypted_text

# Function to encrypt the plain text using addition cipher (lowercase only)
def encrypt_additive(plain_text, key):
    encrypted_text = ""
    for char in plain_text:
        if char in letter_to_index:  # Check if char is a lowercase letter
            current_index = letter_to_index[char]
            new_index = (current_index + key) % 26
            encrypted_text += index_to_letter[new_index]
    return encrypted_text

# Function to decrypt the cipher text using addition cipher (lowercase only)
def decrypt_additive(cipher_text, key):
    decrypted_text = ""
    for char in cipher_text:
        if char in letter_to_index:  # Check if char is a lowercase letter
            current_index = letter_to_index[char]
            new_index = (current_index - key) % 26
            decrypted_text += index_to_letter[new_index]
    return decrypted_text

# Function to encrypt the plain text using Vigenère cipher
def encrypt_vigenere(plain_text, keyword):
    encrypted_text = ""
    keyword_repeated = (keyword * (len(plain_text) // len(keyword))) + keyword[:len(plain_text) % len(keyword)]
    for p_char, k_char in zip(plain_text, keyword_repeated):
        if p_char in letter_to_index and k_char in letter_to_index:  # Check if characters are lowercase letters
            new_index = (letter_to_index[p_char] + letter_to_index[k_char]) % 26
            encrypted_text += index_to_letter[new_index]
    return encrypted_text

# Function to decrypt the cipher text using Vigenère cipher
def decrypt_vigenere(cipher_text, keyword):
    decrypted_text = ""
    keyword_repeated = (keyword * (len(cipher_text) // len(keyword))) + keyword[:len(cipher_text) % len(keyword)]
    for c_char, k_char in zip(cipher_text, keyword_repeated):
        if c_char in letter_to_index and k_char in letter_to_index:  # Check if characters are lowercase letters
            new_index = (letter_to_index[c_char] - letter_to_index[k_char]) % 26
            decrypted_text += index_to_letter[new_index]
    return decrypted_text


def make_matrix(plaintext):
    matrix1 = []
    row = []
    for ch in plaintext:
        row.append(ch)
        if len(row) == 5:
            matrix1.append(row)
            row = []
    # Fill the remaining row with 'x' if it's not empty
    if row:
        while len(row) < 5:  # Fill with 'x' until row length is 5
            row.append('x')
        matrix1.append(row)
    return matrix1

def transpositional_matrix(plaintext):
    key = [3, 1, 4, 0, 2]
    matrix2 = []
    for rw in plaintext:
        row = []
        for i in key:
            if i < len(rw):  # Ensure index is within bounds
                row.append(rw[i])
        matrix2.append(row)
    return matrix2


def transpositional_matrix_decrypt(matrix):
    key = [3, 1, 4, 0, 2]
    decrypted_matrix = []

    for rw in matrix:
        row = [''] * len(key)
        for i, char in enumerate(rw):
            row[key[i]] = char  # Place characters in original position
        decrypted_matrix.append(row)
    # Remove 'x' from the last row if it exists
    if decrypted_matrix and 'x' in decrypted_matrix[-1]:
        decrypted_matrix[-1] = [ch for ch in decrypted_matrix[-1] if ch != 'x']
    return decrypted_matrix

def matrix_to_string(matrix):
    result = ''
    for row in matrix:
        result += ''.join(row)  # Join characters in the row and add to result
    return result

# Definition of Encryption Algorithm
def my_Encryption(plaintext):
    plaintext=plaintext.lower()
    plaintext=plaintext.replace(" ","")
    cipher=""
    for ch in plaintext:
       cipher += ch + index_to_letter[randint(0, 100) % 26]
    return cipher

#Defination of Decryption Algorithm
def my_decryption(ciphertext):
    ciphertext=ciphertext.lower()
    ciphertext=ciphertext.replace(" ","")
    plain=""
    for ch in range(0,len(ciphertext),2):
        plain+=ciphertext[ch]
    return plain


# Function for Encryption Button
def perform_encryption():
    plain_text = text.get()
    key1 = Key1.get()
    key2 = Key2.get()
    keyword = Keyword.get().lower().replace(" ", "")
    plain_text = plain_text.lower().replace(" ","")
    if plain_text == "" and key1 == "" and key2 == "" and keyword == "":
        messagebox.showerror("Error","Please fill all input fields.")
    if len(keyword) >= 15:
        messagebox.showwarning("WARNING", "Keyword must be less than 15 characters.")
    else:
        try:
            key1 = int(key1)
            key2 = int(key2)
        except ValueError:
            messagebox.showerror("Error", "Key1 and Key2 should be in numbers.")
        else:
            if key2 % 2 == 0:
                messagebox.showwarning("Warning", "Key2 should be coprime of 26.")
            else:
                if int(key1) > 0 and int(key1) < 50 and int(key2) > 0 and int(key2) < 50:
                    cipher_text = encrypt_additive(plain_text, key1)
                    cipher_text = encrypt_multiplicative(cipher_text, key2)
                    cipher_text = encrypt_vigenere(cipher_text, keyword)
                    cipher_text = make_matrix(cipher_text)
                    cipher_text = transpositional_matrix(cipher_text)
                    cipher_text = matrix_to_string(cipher_text)
                    cipher_text = encrypt_additive(cipher_text, key1)
                    cipher_text = encrypt_multiplicative(cipher_text, key2)
                    cipher_text = encrypt_vigenere(cipher_text, keyword)
                    cipher_text = my_Encryption(cipher_text)
                    win.clipboard_clear()
                    win.clipboard_append(cipher_text)
                    ResultLabel.config(text= f"Cipher Text: {cipher_text}")
                else:
                    messagebox.showwarning("Warning", "Key1 and key2 should be less than 50.")
    Text_Entry.delete(0, tk.END)
    Key1_Entry.delete(0, tk.END)
    Key2_Entry.delete(0, tk.END)
    Keyword_Entry.delete(0, tk.END)
    Text_Entry.focus()

# Function for Decryption Button
def perform_decryption():
    cipher_text = text.get()
    key1 = Key1.get()
    key2 = Key2.get()
    keyword = Keyword.get().lower().replace(" ", "")
    cipher_text = cipher_text.lower().replace(" ","")
    if cipher_text == "" or key1 == "" or key2 == "" or keyword == "":
        messagebox.showerror("Error","Please fill all input fields.")
        
    if len(keyword) >= 15:
        messagebox.showwarning("WARNING", "Keyword must be less than 15 characters.")

    else:
        try:
            key1 = int(key1)
            key2 = int(key2)
        except ValueError:
            messagebox.showerror("Error", "Key1 and Key2 should be in numbers.")

        else:
            if key2 % 2 == 0:
                messagebox.showwarning("Warning", "Key2 should be coprime of 26.")

            else:
                if int(key1) > 0 and int(key1) < 50 and int(key2) > 0 and int(key2) < 50:
                    decrypted_text = my_decryption(cipher_text)
                    decrypted_text = decrypt_vigenere(decrypted_text, keyword)
                    decrypted_text = decrypt_multiplicative(decrypted_text, key2)
                    decrypted_text = decrypt_additive(decrypted_text, key1)
                    decrypted_matrix = make_matrix(decrypted_text)
                    decrypted_matrix = transpositional_matrix_decrypt(decrypted_matrix)
                    decrypted_text = matrix_to_string(decrypted_matrix)
                    decrypted_text = decrypt_vigenere(decrypted_text, keyword)
                    decrypted_text = decrypt_multiplicative(decrypted_text, key2)
                    decrypted_text = decrypt_additive(decrypted_text, key1)
                    win.clipboard_clear()
                    win.clipboard_append(decrypted_text)
                    ResultLabel.config(text= f"Plain Text: {decrypted_text}")
                else:
                    messagebox.showwarning("Warning", "Key1 and key2 should be less than 50.")
    Text_Entry.delete(0, tk.END)
    Key1_Entry.delete(0, tk.END)
    Key2_Entry.delete(0, tk.END)
    Keyword_Entry.delete(0, tk.END)
    Text_Entry.focus()

# Center a frame
win.columnconfigure(0, weight=1)

# Create Frame 
Frame1 = ttk.LabelFrame(win)
Frame1.grid(row=1, column=0, padx= 30, pady=30)

#Create Labels
Text_Label = ttk.Label(Frame1, text="Enter Text:", font=("TimesNewRoman",12))
Text_Label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
Key1_Label = ttk.Label(Frame1, text="Enter Key1 (number):", font=("TimesNewRoman",12))
Key1_Label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
Key2_Label = ttk.Label(Frame1, text="Enter Key2 (number):", font=("TimesNewRoman",12))
Key2_Label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
Keyword_Label = ttk.Label(Frame1, text="Enter Keyword:", font=("TimesNewRoman",12))
Keyword_Label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
ResultLabel = ttk.Label(Frame1, text="", font=("TimesNewRoman", 12), wraplength=600, justify="left")
ResultLabel.grid(row=5, columnspan=2, padx=10, pady=10, sticky=tk.W)

#Create Entries
text = tk.StringVar()
Text_Entry = ttk.Entry(Frame1, width=50, textvariable=text,font=("TimesNewRoman",12))
Text_Entry.grid(row=0, column=1, padx=10, pady=10)
Text_Entry.focus()
Key1 = tk.StringVar()
Key1_Entry = ttk.Entry(Frame1, width=50, textvariable=Key1,font=("TimesNewRoman",12))
Key1_Entry.grid(row=1, column=1, padx=10, pady=10)
Key2 = tk.StringVar()
Key2_Entry = ttk.Entry(Frame1, width=50, textvariable=Key2,font=("TimesNewRoman",12))
Key2_Entry.grid(row=2, column=1, padx=10, pady=10)
Keyword = tk.StringVar()
Keyword_Entry = ttk.Entry(Frame1, width=50, textvariable=Keyword, font=("TimesNewRoman",12))
Keyword_Entry.grid(row=3, column=1, padx=10, pady=10)

#Create Submit Buttons
encrypt_button = ttk.Button(Frame1, text="Encryption", command=perform_encryption)
encrypt_button.grid(row=4, column=0, padx=10, pady=10)
decrypt_button = ttk.Button(Frame1, text="Decryption", command=perform_decryption)
decrypt_button.grid(row=4, column=1, padx=10, pady=10)

win.mainloop()
