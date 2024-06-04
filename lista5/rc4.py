from random import randint

MAX_ASCII_INDEX = 127

# Key Scheduling Algorithm for key K
def KSA(K: list[int]):
    n = len(K) # lenght of key
    j = 0
    T = [K[i%n] for i in range(256)]#256 element array with repetitions of the initial key
    S = list(range(256)) # 256 element array where S[i] = i
    for i in range(256): # generating permutation of S array with use of repeating key T
        j = (j + S[i] + T[i]) % 256
        S[i], S[j] = S[j], S[i]
    return S

# Pseudo-Random Generation Algorithm returning pseudorandom sequence of lenght m given permutated S array
def PRGA(S: list[int], m: int):
    i = 0
    j = 0
    KS = [0 for i in range(m)]
    for b in range(m):
        i = (i + 1) % 256 # updating value of i
        j = (j + S[i]) % 256 # updating value of j
        S[i], S[j] = S[j], S[i]
        KS[b] = S[(S[i] + S[j]) % 256] # adding pseudorandomnes to KS[b]
    return KS

# algorithm for enciphering or deciphering message M with key K
def RC4(K: list[int], M: list[int]):
    m = len(M) # lenght of message
    S = KSA(K)
    KS = PRGA(S, m)
    return [M[i] ^ KS[i] for i in range(m)] # returning XOR of message with pseudorandom sequence

# checking, whether 2 encrypted messages used the same key 
def is_same_key(encrypted_message_1: list[int], encrypted_message_2: list[int]):
    length = min(len(encrypted_message_1), len(encrypted_message_2))
    for i in range(length):
        if encrypted_message_1[i] ^ encrypted_message_2[i] > MAX_ASCII_INDEX:
            return False

    return True

# converting text to ASCII
def text_to_ascii(text):
    return [ord(char) for char in text]

# converting ASCII to text
def ascii_to_text(ascii_list):
    return ''.join([chr(num) for num in ascii_list])

# generating random key
def generate_key(length = 25):
    return [randint(0, 255) for _ in range(length)]

# generating random message
def generate_message(length = 100):
    return ascii_to_text([randint(32, 126) for _ in range(length)])


def main():
    message = "tajna wiadomość"
    M = text_to_ascii(message)
    key = "khbinbkjnjkefnwuanfibkutwwhbjvkJBdki"
    K = text_to_ascii(key)
    encrypted_message = RC4(K, M)
    decrypted_message = RC4(K, encrypted_message)

    recovered_message = ascii_to_text(decrypted_message)

    print("original message:  " + message)
    print("encrypted message: ", encrypted_message);
    print("decrypted message: ", decrypted_message)
    print("recovered message: " + recovered_message)

if __name__ == "__main__":
    main()