# algorithm for calculating p and q when given n and public and private keys corresponding with n
def find_p_q(n, e, d):
    kphi = d * e - 1
    t = kphi

    while t % 2 == 0:
        t = t // 2
    
    a = 2
    p = None
    while a < 100:
        k = t
        while k < kphi:
            x = pow(a, k, n)
            if x != 1 and x != (n - 1) and pow(x, 2, n) == 1:
                p = GCD(x - 1, n)
                break
            k = k * 2
        a = a + 2
    q = n // p
    return int(p), int(q)

# algorithm for calculating greatest common divider
def GCD(x, y):
    while(y):
       x, y = y, x % y
    return abs(x)

# algorithm for finding such x and y that ax + by = gcd(a, b)
def extended_gcd_iterative(a, b):
    old_r, r = a, b
    old_s, s = 1, 0

    while (r != 0):
        quotient = old_r // r
        old_r, r = r, old_r - quotient*r
        old_s, s = s, old_s - quotient*s
    
    if (b != 0):
        bezout_t = (old_r - old_s*a) // b
    else:
        bezout_t = 0

    return old_r, old_s, bezout_t
    
# algorithm for cracking private key
def attack(n, public1, private1, public2):
    p, q = find_p_q(n, public1, private1)
    phi = (p - 1) * (q - 1)

    gcd, private2, _ = extended_gcd_iterative(public2, phi)
    while (private2 < 0):
        private2 += (phi // gcd)
    return private2