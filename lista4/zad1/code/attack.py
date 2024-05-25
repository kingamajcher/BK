from rsa_keys_gen import generate_keys
from big_prime_gen import generateLargePrime
from rsa_attack import attack
import time

prime_size = 1024

start = time.time()

print('prime size: ' + str(prime_size) + ' bytes')

p = generateLargePrime(prime_size)

print("p generated")

q = generateLargePrime(prime_size)

print('q generated')

end_primes = time.time()
duration_primes = end_primes - start
print('generating primes: ' + str(duration_primes) + ' s')


start_rsa = time.time()

keys1 = generate_keys(p, q)
keys2 = generate_keys(p, q)

[[n, public1], [_, private1]] = keys1
[[_, public2], [_, private2]] = keys2

print('generated RSA')

end_rsa = time.time()
duration_rsa = end_rsa - start_rsa
print('generating rsa: ' + str(duration_rsa) + ' s')

start_attack = time.time()
priv = attack(n, public1, private1, public2)

if priv == private2:
    print('private key cracked succesfully!')

end_attack = time.time()
duration_attack = end_attack - start_attack
print('cracking RSA: ' + str(duration_attack) + ' s')

duration = end_attack - start

print('elapsed time: ' + str(duration) + ' s')