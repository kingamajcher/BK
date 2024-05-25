import random

# greatest common divider of a and b
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# generating keys with parameters p and q
def generate_keys(p, q):
    # calculating the product of p and q
    n = p * q

    # calculating the value of Euler's function of n
    phi = (p - 1) * (q - 1)

    # choosing e such that 1 < e < phi and gcd(e, phi) = 1
    e = random.randint((phi/2), phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    # calculating d, the modular multiplicative inverse of e modulo phi
    d = pow(e, -1, phi)

    return ((n, e), (n, d))