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

print(is_prime(13))