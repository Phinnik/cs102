def encrypt_vigenere(plaintext, keyword):
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    # PUT YOUR CODE HERE
    ciphertext = ''
    keyword = keyword.lower()
    keyPos = -1
    shifts = [ord(keyword[i])-97 for i in range(len(keyword))]
    for char in plaintext:
        keyPos = (keyPos + 1) % len(shifts) 
        charCode = ord(char)
        if (charCode >= 97) and (charCode <= 122):
            newCharCode = 97 + (charCode - 97 + shifts[keyPos]) % 26

        elif (charCode >= 65) and (charCode <= 90):
            newCharCode = 65 + (charCode - 65 + shifts[keyPos]) % 26

        else:
            newCharCode = charCode

        ciphertext += chr(newCharCode)


    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    # PUT YOUR CODE HERE

    plaintext = ''
    keyword = keyword.lower()
    keyPos = -1
    shifts = [ord(keyword[i])-97 for i in range(len(keyword))]
    for char in ciphertext:
        keyPos = (keyPos + 1) % len(shifts) 
        charCode = ord(char)
        if (charCode >= 97) and (charCode <= 122):
            newCharCode = 97 + (charCode - 97 - shifts[keyPos]) % 26


        elif (charCode >= 65) and (charCode <= 90):
            newCharCode = 65 + (charCode - 65 - shifts[keyPos]) % 26

        else:
            newCharCode = charCode


        plaintext += chr(newCharCode)

    return plaintext
