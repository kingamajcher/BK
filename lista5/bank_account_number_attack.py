from random import randint
from itertools import product
from rc4 import RC4, text_to_ascii

weights = [3, 9, 7, 1, 3, 9, 7, 1]
bank_ids = [1010, 1020, 1240, 1140, 1160]

xor0 = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)]
xor1 = [(0, 1), (1, 0), (2, 3), (3, 2), (4, 5), (5, 4), (6, 7), (7, 6), (8, 9), (9, 8)]
xor2 = [(0, 2), (1, 3), (2, 0), (3, 1), (4, 6), (5, 7), (6, 4), (7, 5)]
xor3 = [(0, 3), (1, 2), (2, 1), (3, 0), (4, 7), (5, 6), (6, 5), (7, 4)]
xor4 = [(0, 4), (1, 5), (2, 6), (3, 7), (4, 0), (5, 1), (6, 2), (7, 3)]
xor5 = [(0, 5), (1, 4), (2, 7), (3, 6), (4, 1), (5, 0), (6, 3), (7, 2)]
xor6 = [(0, 6), (1, 7), (2, 4), (3, 5), (4, 2), (5, 3), (6, 0), (7, 1)]
xor7 = [(0, 7), (1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1), (7, 0)]
xor8 = [(0, 8), (1, 9), (8, 0), (9, 1)]
xor9 = [(0, 9), (1, 8), (8, 1), (9, 0)]
xor10 = [(2, 8), (3, 9), (8, 2), (9, 3)]
xor11 = [(2, 9), (3, 8), (8, 3), (9, 2)]
xor12 = [(4, 8), (5, 9), (8, 4), (9, 5)]
xor13 = [(4, 9), (5, 8), (8, 5), (9, 4)]
xor14 = [(6, 8), (7, 9), (8, 6), (9, 7)]
xor15 = [(6, 9), (7, 8), (8, 7), (9, 6)]

xors = [xor0, xor1, xor2, xor3, xor4, xor5, xor6, xor7, xor8, xor9, xor10, xor11, xor12, xor13, xor14, xor15]

def generate_account_nr(country: str):
    bank_id = bank_ids[randint(0, len(bank_ids) - 1)]
    branch_id = randint(0, 999)
    num = int(str(bank_id) + f"{branch_id:03}")
    
    num_str = str(num)
    K = 0
    for i in range(7):
        K += int(num_str[i]) * weights[i]
    K = (10 - K % 10) % 10

    bank_number = int(num_str + str(K))
    client_number = randint(0, 9999999999999999)

    control_nr = 97 - ((int(str(bank_number) + f"{client_number:016}" + str(country_to_ascii(country))) * 100) % 97) + 1

    account_nr = f"{control_nr:02}" + f"{bank_number:08}" + f"{client_number:016}"

    return account_nr

def check_bank_number_control(bank_number: str):
    K = 0
    for i in range(7):
        K += int(bank_number[i]) * weights[i]
    K = (10 - K % 10) % 10
    return bank_number[7] == K

def generate_control(bank_number: int, client_number: int, country: str):
    control_nr = 97 - ((int(str(bank_number) + f"{client_number:016}" + str(country_to_ascii(country))) * 100) % 97) + 1
    return f"{control_nr:02}"

def check(num: str, country: str):
    bank = str[2:6]
    if bank not in bank_ids:
        return False
    control_nr = num[:2]
    country_nr = country_to_ascii(country)
    number = int(num[2:] + str(country_nr) + control_nr)

    return number % 97 == 1

def country_to_ascii(country_id: str):
    result = ""
    
    for char in country_id:
        result += str(ord(char) - 55)
    
    return result

def xor_sum_max_pair(lists):
    def xor_sum(lst1, lst2):
        return sum(a ^ b for a, b in zip(lst1, lst2))

    max_sum = float('-inf')
    max_indices = (-1, -1)

    n = len(lists)
    for i in range(n):
        for j in range(i + 1, n):
            current_sum = xor_sum(lists[i], lists[j])
            if current_sum > max_sum:
                max_sum = current_sum
                max_indices = (i, j)

    return max_indices

def attack(num: int):
    accounts = []

    for i in range(num):
        account = generate_account_nr("PL")
        accounts.append(account)

    key = 'supermegamocnyklucz'
    K = text_to_ascii(key)

    encrypted_accounts = []
    for i in range(num):
        encrypted_accounts.append(RC4(K, text_to_ascii(accounts[i])))

    xored = [0] * 26

    index1, index2 = xor_sum_max_pair(encrypted_accounts)
    for i in range(26):
        xored[i] = encrypted_accounts[index1][i] ^ encrypted_accounts[index2][i]

    print("pair with least calculations: ", index1, ", ", index2)
    print(xored)

    control_number_xored = xored[:2]
    bank_number_xored = xored[2:10]
    client_number_xored = xored[10:]

    possible_control_numbers1 = []
    possible_control_numbers2 = []

    possible_bank_numbers1 = []
    possible_bank_numbers2 = []

    for i0, i1 in product(xors[control_number_xored[0]], xors[control_number_xored[1]]):
        possible_control_numbers1.append(str(i0[0]) + str(i1[0]))
        possible_control_numbers2.append(str(i0[1]) + str(i1[1]))

    print("all possible control numbers found")

    # cracking bank number
    for i0, i1, i2, i3, i4, i5, i6, i7 in product(
        xors[bank_number_xored[0]], xors[bank_number_xored[1]], xors[bank_number_xored[2]], xors[bank_number_xored[3]],
        xors[bank_number_xored[4]], xors[bank_number_xored[5]], xors[bank_number_xored[6]], xors[bank_number_xored[7]]
    ):
        bank_number1 = ''.join([str(i0[0]), str(i1[0]), str(i2[0]), str(i3[0]), str(i4[0]), str(i5[0]), str(i6[0]), str(i7[0])])
        bank_number2 = ''.join([str(i0[1]), str(i1[1]), str(i2[1]), str(i3[1]), str(i4[1]), str(i5[1]), str(i6[1]), str(i7[1])])

        if check_bank_number_control(bank_number1) and check_bank_number_control(bank_number2):
            possible_bank_numbers1.append(bank_number1)
            possible_bank_numbers2.append(bank_number2)

    print("all possible bank numbers found")
    account_numbers_found = False

    #cracking the rest
    for i0, i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14, i15 in product(
        xors[client_number_xored[0]], xors[client_number_xored[1]], xors[client_number_xored[2]], xors[client_number_xored[3]],
        xors[client_number_xored[4]], xors[client_number_xored[5]], xors[client_number_xored[6]], xors[client_number_xored[7]],
        xors[client_number_xored[8]], xors[client_number_xored[9]], xors[client_number_xored[10]], xors[client_number_xored[11]],
        xors[client_number_xored[12]], xors[client_number_xored[13]], xors[client_number_xored[14]], xors[client_number_xored[15]]
    ):
        client_number1 = (
            str(i0[0]) + str(i1[0]) + str(i2[0]) + str(i3[0]) + str(i4[0]) + str(i5[0]) + str(i6[0]) + str(i7[0]) +
            str(i8[0]) + str(i9[0]) + str(i10[0]) + str(i11[0]) + str(i12[0]) + str(i13[0]) + str(i14[0]) + str(i15[0])
        )
        client_number2 = (
            str(i0[1]) + str(i1[1]) + str(i2[1]) + str(i3[1]) + str(i4[1]) + str(i5[1]) + str(i6[1]) + str(i7[1]) +
            str(i8[1]) + str(i9[1]) + str(i10[1]) + str(i11[1]) + str(i12[1]) + str(i13[1]) + str(i14[1]) + str(i15[1])
        )

        for i in range(len(possible_bank_numbers1)):
            calculated_control1 = generate_control(possible_bank_numbers1[i], client_number1, 'PL')
            calculated_control2 = generate_control(possible_bank_numbers2[i], client_number2, 'PL')

            if calculated_control1 in possible_control_numbers1 and calculated_control2 in possible_control_numbers2:
                account_numbers_found = True
            account_numbers_found = True

        if account_numbers_found:
            break
    
                                                                    

    account1 = calculated_control1 + bank_number1 + client_number1
    print(account1)
    account2 = calculated_control2 + bank_number2 + client_number2
    print(account2)

    if account1 in accounts and account2 in accounts:
        print("accounts decrpyted correctly")


    # to find all other account numbers:
    #       1) xor found account1 with its corresponding values in xored_accounts - you get part of the key used to encrypt all the accounts
    #       2) xor every encrypted account with this part of the key - you get decrypted account number

attack(10000)