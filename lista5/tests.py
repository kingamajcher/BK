from rc4 import RC4, is_same_key, text_to_ascii, ascii_to_text, generate_key, generate_message

def rc4(key: list[int], message: str):
    M = text_to_ascii(message)

    encrypted_message = RC4(key, M)
    decrypted_message = RC4(key, encrypted_message)

    recovered_message = ascii_to_text(decrypted_message)

    print("key:               ", key)
    print("original message:  " + message)
    print("encrypted message: ", encrypted_message);
    print("decrypted message: ", decrypted_message)
    print("recovered message: " + recovered_message)

def test_rc4():
    K = generate_key(25)
    message = "tajemnicza wiadomość do zaszyfrowania hehehe"
    rc4(K, message)
    
def test_same_key():
    key1 = generate_key()
    key2 = generate_key()

    while key1 == key2:
        key2 = generate_key()

    message1 = text_to_ascii(generate_message())
    message2 = text_to_ascii(generate_message())
    message3 = text_to_ascii(generate_message())

    encrypted_message_1 = RC4(key1, message1)
    encrypted_message_2 = RC4(key1, message2)
    encrypted_message_3 = RC4(key2, message3)

    test1 = is_same_key(encrypted_message_1, encrypted_message_2)
    test2 =  is_same_key(encrypted_message_1, encrypted_message_3)

    print("Testing whether in two messages encrypted with the same key, the same key is detected (should be true): ", test1, "\n")

    print("Testing whether in two messages encrypted with different keys, the same key is detected (should be false): ", test2)


def main():
    # test_rc4()
    test_same_key()

if __name__ == "__main__":
    main()