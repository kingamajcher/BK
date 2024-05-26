from random import randint

weights = [3, 9, 7, 1, 3, 9, 7, 1]
bank_ids = [1010, 1020, 1240, 1140, 1160]

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

def check(num: str, country: str):
    control_nr = num[:2]
    country_nr = country_to_ascii(country)
    number = int(num[2:] + str(country_nr) + control_nr)

    return number % 97 == 1

def country_to_ascii(country_id: str):
    result = ""
    
    for char in country_id:
        result += str(ord(char) - 55)
    
    return result

def attack(num: int):
    accounts = []
    for i in range(num):
        accounts.append(generate_account_nr('PL'))
    print(accounts)

attack(5)