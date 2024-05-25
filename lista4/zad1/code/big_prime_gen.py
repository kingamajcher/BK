import math, random

def primeSieve(sieveSize):
    # function which returns a list of prime numbers calculated using the Sieve of Eratosthenes algorithm.

    sieve = [True] * sieveSize # inicializing array with true value for each number
    sieve[0] = False # zero is not a prime
    sieve[1] = False # one is not a prime

    # creating the sieve:
    for i in range(2, int(math.sqrt(sieveSize)) + 1):
        pointer = i * 2
        while pointer < sieveSize:
            sieve[pointer] = False
            pointer += i

    # making the list of primes:
    primes = []
    for i in range(sieveSize):
        if sieve[i] == True:
            primes.append(i)
    return primes

# Rabin-Miller primality test - probability of the number actually being composite is 4**(-k)
def rabinMiller(num):

    if num % 2 == 0 or num < 2: # even numbers cannot be prime
        return False
    if num == 3:
        return True
    s = num - 1
    t = 0
    while s % 2 == 0:
        # halving s until it is odd (and using t to count how many times we halve s)
        s = s // 2
        t += 1
    k = 5
    for trials in range(k): # trying to falsify num's primality k times
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1: # test does not apply if v is 1.
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True


LOW_PRIMES = primeSieve(100)

# checking whether given number is prime
def isPrime(num):
    # numbers less than 2 cannot be prime
    if (num < 2):
        return False
    # checking if primes < 100 divide num
    for prime in LOW_PRIMES:
        if (num == prime):
             return True
        if (num % prime == 0):
             return False
    # using Rabin-Miller test if previous tests do not prove number is composite
    return rabinMiller(num)


# returning a random prime number that is keysize bits in size:
def generateLargePrime(keysize=1024):
    while True:
        num = random.randrange(2**(keysize-1), 2**(keysize))
        if isPrime(num):
            return num