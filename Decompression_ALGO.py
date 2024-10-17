from random import randint
import tkinter as tk
from tkinter import ttk, messagebox
from itertools import cycle

win=tk.Tk()
win.title("Encryption_Decryption_Algorithm")

# Dictionaries for character encoding
char = {chr(i + 97): i for i in range(26)}  # a:0, b:1, ..., z:25
char2 = {i: chr(i + 97) for i in range(26)}  # 0:a, 1:b, ..., 25:z

#Nested List to make a alphabet matrix
matrix=[
    ['q','w','e','r','t'],
    ['y','u','i','o','p'],
    ['a','s','d','f','g'],
    ['h','k','l','z','x'],
    ['c','v','b','n','m']
    ]

def key_expansion(key):
    """Expand the key into round keys (simplified)."""
    return [key[i:i + 8] for i in range(0, len(key), 8)]

def s_box(byte):
    """Substitution using a simple S-box."""
    sbox = [0x5A, 0x3C, 0x8E, 0x7D, 0xA1, 0x6B, 0xD2, 0xF8,
            0x89, 0x47, 0xB4, 0xA6, 0x34, 0x22, 0x0D, 0xA9]
    return sbox[byte % 16]  # Ensure the byte is in the range of the S-box

def p_box(block):
    """Permutation operation."""
    # Example permutation (not a real P-box)
    permuted = bytearray(len(block))
    perm_order = [3, 0, 1, 2]  # Custom permutation order for 4 bytes
    for i, j in enumerate(perm_order):
        permuted[i] = block[j]
    return bytes(permuted)

def mixing_operation(block):
    """A simple mixing operation (XOR with a constant)."""
    mix_constant = bytes([0x1B, 0x2A, 0x3C, 0x4D])  # Example constant
    return bytes(b ^ m for b, m in zip(block, mix_constant))

def encrypt_block(plaintext, key):
    """Encrypt a 64-bit block with the given key."""
    round_keys = key_expansion(key)
    state = plaintext

    for i in range(8):  # 8 rounds
        state = bytes(s_box(b) for b in state)  # Substitution
        state = p_box(state)                      # Permutation
        state = mixing_operation(state)           # Mixing
        # XOR with the round key
        state = bytes(b ^ round_keys[i % len(round_keys)][j] for j, b in enumerate(state))

    return state

def decrypt_block(ciphertext, key):
    """Decrypt a 64-bit block with the given key (simplified)."""
    round_keys = key_expansion(key)[::-1]  # Reverse the order of round keys
    state = ciphertext

    for i in range(8):  # 8 rounds
        # XOR with the round key
        state = bytes(b ^ round_keys[i % len(round_keys)][j] for j, b in enumerate(state))
        state = mixing_operation(state)       # Mixing (inverse)
        state = p_box(state)                  # Permutation (inverse)
        state = bytes(s_box(b) for b in state)  # Substitution (inverse)

    return state

def string_to_bytes(s):
    """Convert a string to bytes, padding if necessary."""
    # Convert string to bytes and pad to 8 bytes (64 bits) if needed
    b = s.encode('utf-8')
    return b.ljust(8, b'\x00')  # Pad with null bytes if less than 8 bytes

def bytes_to_string(b):
    """Convert bytes back to string."""
    return b.decode('utf-8').rstrip('\x00')  # Remove padding

# Example usage
plaintext = "HELLO!  "  # Ensure the string is 8 characters (64 bits)
key = bytes([0x1F, 0x2E, 0x3D, 0x4C, 0x5B, 0x6A, 0x79, 0x88,
             0x91, 0xA0, 0xB1, 0xC2, 0xD3, 0xE4, 0xF5, 0x06])  # 128-bit key

#Defination to find the position of characters in Matrix for Playfair Algorithm
def find_pos(char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j

#Defination for making text pair for Playfair Algorithm
def make_pair(text):
    text = text.lower().replace('j', 'i') 
    pair = []
    i = 0
    while i < len(text):
        if i + 1 == len(text) or text[i] == text[i + 1]:
            pair.append((text[i], 'x'))
            i += 1
        else:
            pair.append((text[i], text[i + 1]))
            i += 2
    return pair

#Defination of PlayFair Encryption Algorithm
def Encrypt_PlayFair_cipher(plain_text):
    pairs = make_pair(plain_text)
    cipher = ""
    for pair_a, pair_b in pairs:
        row_a, col_a = find_pos(pair_a)
        row_b, col_b = find_pos(pair_b)
        if row_a == row_b: 
            cipher += matrix[row_a][(col_a + 1) % 5]
            cipher += matrix[row_b][(col_b + 1) % 5]
        elif col_a == col_b: 
            cipher += matrix[(row_a + 1) % 5][col_a]
            cipher += matrix[(row_b + 1) % 5][col_b]
        else: 
            cipher += matrix[row_a][col_b]
            cipher += matrix[row_b][col_a]
    return cipher

#Definition of PlayFair Decryption Algorithm
def Decrypt_PlayFair_cipher(cipher_text):
    pairs = make_pair(cipher_text)
    plain_text = ""
    for pair_a, pair_b in pairs:
        row_a, col_a = find_pos(pair_a)
        row_b, col_b = find_pos(pair_b)
        if row_a == row_b:  
            plain_text += matrix[row_a][(col_a - 1) % 5]
            plain_text += matrix[row_b][(col_b - 1) % 5]
        elif col_a == col_b:  
            plain_text += matrix[(row_a - 1) % 5][col_a]
            plain_text += matrix[(row_b - 1) % 5][col_b]
        else:  
            plain_text += matrix[row_a][col_b]
            plain_text += matrix[row_b][col_a]
    return plain_text.replace('x', ' ')

#Defination of Additive Encryption Algorithm
def Encrypt_additive_cipher(plain_text, key):
    cipher = ""
    for ch in plain_text.lower():
        if ch in char:    
            add_key=(char[ch] + key )%26
            cipher += char2[add_key]
    return cipher

# Definition of Additive Decryption Algorithm
def Decrypt_additive_cipher(cipher_text,key):
    plain = ""
    for ch in cipher_text.lower():
        if ch in char:    
            add_key=(char[ch] - key )%26
            plain += char2[add_key]
    return plain

#Definition of Multiplicative Encryption Algorithm
def Encrypt_multiplicative_cipher(plain_text, key):
    plain=""
    for ch in plain_text.lower():
        if ch in char:
            multi= (char[ch] * key )%26
            plain+= char2[multi]
    return plain

#Defination of Multiplicative Decryption Algorithm
def Decrypt_multiplicative_cipher(cipher_text, key):
    cipher=""
    for ch in cipher_text:
        if ch in char:
            res = (char[ch]* pow(key, -1, 26))%26
            cipher+= char2[res]
    return cipher

#Defination of Vigenere Encryption Algorithm
def Encrypt_Vigenere_cipher(plain_text, key):
    cipher=""
    p_text=plain_text.lower()
    p_text = p_text.replace(" ","")
    k_text=key.lower()
    k_text=k_text.replace(" ","")
    for ch, value in zip(p_text, cycle(k_text)):
        if ch in char:
            res = (char[ch] + char[value])%26
            cipher+= char2[res]
    return cipher

#Defination of Vigenere Decryption Algorithm
def Decrypt_Vigenere_cipher(cipher_text, key):
    plain=""
    p_text=cipher_text.lower()
    p_text = p_text.replace(" ","")
    k_text=key.lower()
    k_text=k_text.replace(" ","")
    for ch, value in zip(p_text, cycle(k_text)):
        if ch in char:
            res = (char[ch] - char[value])%26
            plain+= char2[res]
    return plain

#Defination of Encryption Algorithm
def my_Encryption(plaintext):
    plaintext=plaintext.lower()
    plaintext=plaintext.replace(" ","")
    cipher=""
    for ch in plaintext:
       cipher += ch + char2[randint(0, 100) % 26] + char2[randint(0, 100) % 26] + char2[randint(0, 100) % 26]
    return cipher

#Defination of Decryption Algorithm
def my_decryption(ciphertext):
    ciphertext=ciphertext.lower()
    ciphertext=ciphertext.replace(" ","")
    plain=""
    for ch in range(0,len(ciphertext),4):
        plain+=ciphertext[ch]
    return plain

# Function for Encryption Button
def perform_encryption():
    plain_text = text.get()
    key1 = Key1.get()
    key2 = Key2.get()
    keyword = Keyword.get().replace(" ", "")
    if plain_text == "" and key1 == "" and key2 == "" and keyword == "":
        messagebox.showerror("Error","Please fill all input fields.")
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
                    encrypt = Encrypt_additive_cipher(plain_text, int(key1))
                    encrypt = Encrypt_multiplicative_cipher(encrypt, int(key2))
                    plaintext_bytes = string_to_bytes(encrypt)
                    encrypt = encrypt_block(plaintext_bytes, key)
                    encrypt = bytes_to_string(encrypt)
                    encrypt = my_Encryption(encrypt)
                    encrypt = Encrypt_Vigenere_cipher(encrypt, keyword)
                    encrypt = Encrypt_PlayFair_cipher(encrypt)
                    win.clipboard_clear()
                    win.clipboard_append(encrypt)
                    ResultLabel.config(text= f"Cipher Text: {encrypt}")
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
    keyword = Keyword.get().replace(" ", "")
    if cipher_text == "" or key1 == "" or key2 == "" or keyword == "":
        messagebox.showerror("Error","Please fill all input fields.")
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
                    decrypt = Decrypt_PlayFair_cipher(cipher_text)
                    decrypt = Decrypt_Vigenere_cipher(decrypt, keyword)
                    decrypt = my_decryption(decrypt)
                    encrypted_bytes = string_to_bytes(encrypt)
                    encrypt = decrypt_block(encrypted_bytes, key)
                    decrypt = Decrypt_multiplicative_cipher(decrypt, int(key2))
                    decrypt = Decrypt_additive_cipher(decrypt, int(key1))
                    win.clipboard_clear()
                    win.clipboard_append(decrypt)
                    ResultLabel.config(text= f"Plain Text: {decrypt}")
                else:
                    messagebox.showwarning("Warning", "Key1 and key2 should be less than 50.")
    Text_Entry.delete(0, tk.END)
    Key1_Entry.delete(0, tk.END)
    Key2_Entry.delete(0, tk.END)
    Keyword_Entry.delete(0, tk.END)
    Text_Entry.focus()

# Create Frame
Frame1 = ttk.LabelFrame(win)
Frame1.grid(row=1, column=0, padx= 30, pady=30)

#Create Labels
Text_Label = ttk.Label(Frame1, text="Enter Text:", font=("TimesNewRoman",20))
Text_Label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
Key1_Label = ttk.Label(Frame1, text="Enter Key1 (number):", font=("TimesNewRoman",20))
Key1_Label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
Key2_Label = ttk.Label(Frame1, text="Enter Key2 (number):", font=("TimesNewRoman",20))
Key2_Label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
Keyword_Label = ttk.Label(Frame1, text="Enter Keyword:", font=("TimesNewRoman",20))
Keyword_Label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
ResultLabel = ttk.Label(Frame1, text="", font=("TimesNewRoman", 20))
ResultLabel.grid(row=5, columnspan=2, padx=10, pady=10, sticky=tk.W)

#Create Entries
text = tk.StringVar()
Text_Entry = ttk.Entry(Frame1, width=50, textvariable=text,font=("TimesNewRoman",20))
Text_Entry.grid(row=0, column=1, padx=10, pady=10)
Text_Entry.focus()
Key1 = tk.StringVar()
Key1_Entry = ttk.Entry(Frame1, width=50, textvariable=Key1,font=("TimesNewRoman",20))
Key1_Entry.grid(row=1, column=1, padx=10, pady=10)
Key2 = tk.StringVar()
Key2_Entry = ttk.Entry(Frame1, width=50, textvariable=Key2,font=("TimesNewRoman",20))
Key2_Entry.grid(row=2, column=1, padx=10, pady=10)
Keyword = tk.StringVar()
Keyword_Entry = ttk.Entry(Frame1, width=50, textvariable=Keyword, font=("TimesNewRoman",20))
Keyword_Entry.grid(row=3, column=1, padx=10, pady=10)

#Create Submit Buttons
encrypt_button = ttk.Button(Frame1, text="Encryption", command=perform_encryption)
encrypt_button.grid(row=4, column=0, padx=10, pady=10)
decrypt_button = ttk.Button(Frame1, text="Decryption", command=perform_decryption)
decrypt_button.grid(row=4, column=1, padx=10, pady=10)


win.mainloop()
