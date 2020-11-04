def encrypt_caesar(plaintext: str, shift: str = 3) -> str:
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
    ciphertext = ''
    for char in plaintext:
        if 'a' <= char <= 'z':
            newCharCode = 97 + (ord(char) - 97 + shift) % 26
        elif 'A' <= char <= 'Z':
            newCharCode = 65 + (ord(char) - 65 + shift) % 26
        else:
            newCharCode = ord(char)
        ciphertext += chr(newCharCode)
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: str = 3) -> str:
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
    plaintext = ''
    for char in ciphertext:
        if 'a' <= char <= 'z':
            newCharCode = 97 + (ord(char) - 97 - shift) % 26
        elif 'A' <= char <= 'Z':
            newCharCode = 65 + (ord(char) - 65 - shift) % 26
        else:
            newCharCode = ord(char)
        plaintext += chr(newCharCode)
    return plaintext
