from math import sqrt 

def is_prime(n):
    """
    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
    """
    # PUT YOUR CODE HERE
    p = True
    for i in range(2, round(sqrt(n))+1):
        if n % i == 0:
            p = False
    return p

def gcd(a, b):
    """
    >>> gcd(12, 15)
    3
    >>> gcd(3, 7)
    1
    """
    # PUT YOUR CODE HERE
    while a!=0 and b!=0:
        if a > b:
            a = a % b
        else:
            b = b % a
    return (a + b)

def multiplicative_inverse(e, phi):
    """
    >>> multiplicative_inverse(7, 40)
    23
    """
    # PUT YOUR CODE HERE
    
    table = [[phi],         # A
            [e],            # B
            [phi % e],      # A%B
            [phi // e],     #A//B
            [],             # x
            []]             # y
    
    while table[2][-1] != 0:
        table[0].append(table[1][-1])
        table[1].append(table[2][-1])
        table[2].append(table[0][-1] % table[1][-1])
        table[3].append(table[0][-1] // table[1][-1])

    table[4] = [0 for i in range(len(table[0]))]
    table[5] = [0 for i in range(len(table[0]))]
    table[4][-1], table[5][-1] = 0, 1

    for i in range(len(table[0])-2, -1, -1):
        table[4][i] = table[5][i+1]
        table[5][i] = table[4][i+1] - table[5][i+1]*table[3][i]

    d = table[5][0] % table[0][0]
    return d

def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')

    n = pq
    # PUT YOUR CODE HERE

    phi = (p-1)(q-1)
    # PUT YOUR CODE HERE

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)
    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))

print(gcd(40,566))