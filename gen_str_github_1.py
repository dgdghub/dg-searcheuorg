import random

def read_existing_strings(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f)

def write_dom(path, text):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(text + '\n')

def is_valid_string(s):
    for char in set(s):
        if s.count(char) > 5:
            return False
    return True

def generate_human_like_string(input_str, min_length=4, max_length=8):
    alphabet = ''.join([c for c in input_str if c.isalpha()])
    digits = ''.join([c for c in input_str if c.isdigit()])
    used_combinations = set()
    existing_strings = read_existing_strings('./passed.txt')

    while True:
        length = random.randint(min_length, max_length)
        num_letters = length - random.randint(0, 5)  # At least one digit at the start or end
        num_digits = length - num_letters

        if num_digits > 0:
            digit = random.choice(digits)
            digits_part = digit * num_digits
        else:
            digits_part = ''

        letters = random.choices(alphabet, k=num_letters)

        # Decide whether the digits go at the start or end
        if random.choice([True, False]):
            combined = digits_part + ''.join(letters)
        else:
            combined = ''.join(letters) + digits_part

        if combined not in used_combinations and is_valid_string(combined):
            if combined not in existing_strings:
                used_combinations.add(combined)
                write_dom('./domains.txt', combined)
                print(combined)

if __name__ == "__main__":
    input_str = "abcdefghijklmnopqrstuvwxyz0123456789"
    new_str = generate_human_like_string(input_str)