import random

def read_existing_strings(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f)

def write_dom(path, text):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(text + '\n')

def generate_human_like_string(alphabet, digits, min_length=4, max_length=8):
    used_combinations = set()
    existing_strings = read_existing_strings('./passed.txt')

    while True:
        length = random.randint(min_length, max_length)
        num_letters = length - random.randint(1, 4)  # At least one digit at the start or end
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

        if combined not in used_combinations:
            if (combined + '.eu.org') not in existing_strings:
                used_combinations.add(combined)
                print(f'new str: {combined}')
                write_dom('./domains.txt', combined)
            else:
                print(f'Already scan: {combined}')
        else:
            print(f'Already generated: {combined}')

if __name__ == "__main__":
    # Example usage
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    digits = "0123456789"
    # alphabet = "abc"
    # digits = "123"
    new_str = generate_human_like_string(alphabet, digits)