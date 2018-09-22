def encrypt_caesar(plaintext, shift):
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE
    ciphertext = ''
    for char in plaintext:
        charCode = ord(char)
        if (charCode >= 97) and (charCode <= 122):
            newCharCode = 97 + (charCode - 97 + shift) % 26

        elif (charCode >= 65) and (charCode <= 90):
            newCharCode = 65 + (charCode - 65 + shift) % 26

        else:
            newCharCode = charCode

        ciphertext += chr(newCharCode)
    return ciphertext



def decrypt_caesar(ciphertext, shift):
    """
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE
    plaintext = ''
    for char in ciphertext:
        charCode = ord(char)
        if (charCode >= 97) and (charCode <= 122):
            newCharCode = 97 + (charCode - 97 - shift) % 26

        elif (charCode >= 65) and (charCode <= 90):
            newCharCode = 65 + (charCode - 65 - shift) % 26

        else:
            newCharCode = charCode

        plaintext += chr(newCharCode)
    return plaintext

print(encrypt_caesar('Python', 3))
print(decrypt_caesar('Sbwkrq', 3))