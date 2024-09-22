from itertools import cycle
from math import gcd
char = {
    'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15,
    'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 
    'y': 24, 'z': 25
}

char2 = {
    0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm', 13: 'n', 14: 'o', 15: 'p',
    16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v', 22: 'w', 23: 'x', 
    24: 'y', 25: 'z'
}

matrix=[
    ['q','w','e','r','t'],
    ['y','u','i','o','p'],
    ['a','s','d','f','g'],
    ['h','k','l','z','x'],
    ['c','v','b','n','m']
    ]

def find_pos(char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j
            
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

def Encrypt_additive_cipher(plain_text, key):
    cipher = ""
    for ch in plain_text.lower():
        if ch in char:    
            add_key=(char[ch] + key )%26
            cipher += char2[add_key]
    return cipher
        
def Decrypt_additive_cipher(cipher_text,key):
    plain = ""
    for ch in cipher_text.lower():
        if ch in char:    
            add_key=(char[ch] - key )%26
            plain += char2[add_key]
    return plain

def Encrypt_multiplicative_cipher(plain_text, key):
    plain=""
    for ch in plain_text.lower():
        if ch in char:
            multi= (char[ch] * key )%26
            plain+= char2[multi]
    return plain

def Decrypt_multiplicative_cipher(cipher_text, key):
    cipher=""
    for ch in cipher_text:
        if ch in char:
            res = (char[ch]* pow(key, -1, 26))%26
            cipher+= char2[res]
    return cipher


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

def get_number(str):
    while True:
        try:
            return int(input(str))  
        except ValueError:
            print("Invalid input. Please enter a valid number.") 

text = input("Enter Text to Encrypt: ")
text=text.replace(" ","")
key1 = get_number("Enter Number Key1: ")

key2 = get_number("Enter Number Key2: ")
while key2%2==0:
    print(f"Key {key2} is not coprime to 26; please choose another key.")
    key2 = get_number("Enter Number Key2: ")

keyword = input("Enter Keyword: ")
keyword=keyword.replace(" ","")

encrypt = Encrypt_additive_cipher(text, key1)
encrypt = Encrypt_multiplicative_cipher(encrypt, key2)
encrypt = Encrypt_Vigenere_cipher(encrypt, keyword)
encrypt = Encrypt_PlayFair_cipher(encrypt)

print(f"Cipher Text: {encrypt}")

decrypt = Decrypt_PlayFair_cipher(encrypt)
decrypt = Decrypt_Vigenere_cipher(decrypt, keyword)
decrypt = Decrypt_multiplicative_cipher(decrypt, key2)
decrypt = Decrypt_additive_cipher(decrypt,key1)

print(f"Plain Text: {decrypt}")
