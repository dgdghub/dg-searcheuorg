import random
import string
import os
import re
# 常见单词列表，用于生成可读性较高的字符串
common_words = [
    'test', 'ball', 'cake', 'door', 'fish', 'girl', 'hat', 'joke', 'kite', 'lamp',
    'moon', 'nest', 'open', 'pool', 'quit', 'rest', 'sun', 'tent', 'user', 'vase',
    'wall', 'xeno', 'yard', 'zoo', 'able', 'bake', 'cool', 'dark', 'easy', 'fast',
    'good', 'high', 'iron', 'july', 'king', 'love', 'main', 'nice', 'oval', 'play',
    'quiet', 'rose', 'salt', 'tube', 'uber', 'van', 'west', 'yarn', 'zero'
]

# 加载已生成的字符串
def load_passed_strings(file_path):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, 'r') as f:
        return set(line.strip() for line in f)

# 生成字母部分
def generate_letters_part(length):
    # 优先从常见单词中选择
    valid_words = [word for word in common_words if len(word) == length]
    if valid_words:
        return random.choice(valid_words)
    # 如果没有合适的单词，随机生成字母
    letters = []
    prev_char = None
    current_count = 0
    for _ in range(length):
        if prev_char is None:
            char = random.choice(string.ascii_lowercase)
            letters.append(char)
            prev_char = char
            current_count = 1
        else:
            if current_count >= 5:
                available = string.ascii_lowercase.replace(prev_char, '')
                char = random.choice(available)
                letters.append(char)
                prev_char = char
                current_count = 1
            else:
                if random.random() < 0.3:
                    letters.append(prev_char)
                    current_count += 1
                else:
                    available = string.ascii_lowercase.replace(prev_char, '')
                    char = random.choice(available)
                    letters.append(char)
                    prev_char = char
                    current_count = 1
    return ''.join(letters)

# 生成数字部分
def generate_digits_part(length):
    if length == 0:
        return ''
    digits = []
    prev_d = None
    remaining = length
    while remaining > 0:
        if prev_d is None:
            available_digits = '0123456789'
        else:
            available_digits = '0123456789'.replace(prev_d, '')
        d = random.choice(available_digits)
        max_repeat = min(5, remaining)
        repeat = random.randint(1, max_repeat)
        digits.append(d * repeat)
        prev_d = d
        remaining -= repeat
    return ''.join(digits)

# 生成候选字符串
def generate_candidate():
    length = random.randint(4, 8)
    type_choice = random.choices([0, 1, 2, 3], weights=[4, 2, 2, 2], k=1)[0]
    if type_choice == 0:
        # 纯字母
        return generate_letters_part(length)
    elif type_choice == 1:
        # 纯数字
        return generate_digits_part(length)
    elif type_choice == 2:
        # 字母 + 数字
        split = random.randint(1, length - 1)
        letters = generate_letters_part(split)
        digits = generate_digits_part(length - split)
        return letters + digits
    else:
        # 数字 + 字母
        split = random.randint(1, length - 1)
        digits = generate_digits_part(split)
        letters = generate_letters_part(length - split)
        return digits + letters

# 检查字符串是否合法
def is_valid(s, passed_set):
    # 检查是否已存在
    if s in passed_set:
        return False
    # 检查字母和数字的重复次数
    prev_char = None
    current_count = 0
    for char in s:
        if char == prev_char:
            current_count += 1
            if current_count > 5:
                return False
        else:
            prev_char = char
            current_count = 1
    # 检查数字是否只出现在首尾
    if any(c.isdigit() for c in s):
        if not re.fullmatch(r'^(\d+[a-z]+|[a-z]+\d+|\d+|[a-z]+)$', s):
            return False
    return True

# 生成唯一字符串
def generate_unique_string(passed_set):
    while True:
        candidate = generate_candidate()
        if is_valid(candidate, passed_set):
            return candidate

# 主函数
def perform():
    passed_file = 'passed.txt'
    passed_set = load_passed_strings(passed_file)
    new_string = generate_unique_string(passed_set)
    passed_set.add(new_string)
    with open(passed_file, 'a') as f:
        f.write(new_string + '\n')
    return new_string

if __name__ == '__main__':
    print(perform())
