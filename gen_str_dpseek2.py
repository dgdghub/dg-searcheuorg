import random
import string

def has_consecutive_duplicates(s, max_repeat=5):
    current_char = None
    current_count = 0
    for char in s:
        if char == current_char:
            current_count += 1
            if current_count > max_repeat:
                return True
        else:
            current_char = char
            current_count = 1
    return False

def generate_digits(length):
    while True:
        digits = ''.join(random.choices(string.digits, k=length))
        if not has_consecutive_duplicates(digits, 5):
            return digits

def generate_letters(length):
    vowels = ['a', 'e', 'i', 'o', 'u']
    consonants = [c for c in string.ascii_lowercase if c not in vowels]
    start_with_consonant = random.choice([True, False])
    letters = []
    for i in range(length):
        if (i % 2 == 0 and start_with_consonant) or (i % 2 != 0 and not start_with_consonant):
            letters.append(random.choice(consonants))
        else:
            letters.append(random.choice(vowels))
    return ''.join(letters)

def generate_mixed(length):
    while True:
        letters_length = random.randint(1, length - 1)
        remaining = length - letters_length
        d1 = random.randint(0, remaining)
        d2 = remaining - d1
        if d1 + d2 >= 1:
            break
    digits_start = generate_digits(d1) if d1 > 0 else ''
    digits_end = generate_digits(d2) if d2 > 0 else ''
    letters = generate_letters(letters_length)
    return digits_start + letters + digits_end

def generate_candidate():
    length = random.randint(4, 8)
    type_choice = random.choice(['digits', 'letters', 'mixed'])
    if type_choice == 'digits':
        return generate_digits(length)
    elif type_choice == 'letters':
        return generate_letters(length)
    else:
        return generate_mixed(length)

def read_passed_file():
    try:
        with open('passed.txt', 'r') as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def write_to_passed(s):
    with open('passed.txt', 'a') as f:
        f.write(s + '\n')

def perform():
    passed = read_passed_file()
    while True:
        candidate = generate_candidate()
        if candidate not in passed:
            write_to_passed(candidate)
            return candidate

if __name__ == '__main__':
    print(perform())