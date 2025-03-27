import string

# Dictionnaires prédéfinis pour les plages communes
LOWERCASE = dict.fromkeys(string.ascii_lowercase)
UPPERCASE = dict.fromkeys(string.ascii_uppercase)
DIGITS = dict.fromkeys(string.digits)
ALPHANUMERIC = {**LOWERCASE, **UPPERCASE, **DIGITS}

PREDEFINED_RANGES = {
    'a-z': LOWERCASE,
    'A-Z': UPPERCASE,
    '0-9': DIGITS,
    'a-zA-Z': ALPHANUMERIC,
    'a-z0-9': ALPHANUMERIC
}

def parse_group(regex):
    return regex[1:regex.index(')')].split('|'), regex.index(')')

def parse_range(range_str):
    if range_str in PREDEFINED_RANGES:
        return PREDEFINED_RANGES[range_str].keys()
    
    chars = set()
    i = 0
    while i < len(range_str):
        if i + 2 < len(range_str) and range_str[i+1] == '-':
            chars.update(chr(c) for c in range(ord(range_str[i]), ord(range_str[i+2])+1))
            i += 3
        else:
            chars.add(range_str[i])
            i += 1
    return chars

def parse_quantifier(regex, i):
    if regex[i] == '+':
        return 1, float('inf'), i + 1
    if regex[i] == '{':
        end = regex.index('}', i)
        nums = regex[i+1:end].split(',')
        if len(nums) == 1:
            return int(nums[0]), int(nums[0]), end + 1
        return int(nums[0]), float('inf') if nums[1] == '' else int(nums[1]), end + 1
    return 1, 1, i

def reg_compare(regex, text):
    i = j = 0
    while i < len(regex) and j <= len(text):
        if i + 1 < len(regex) and regex[i+1] in {'+', '{'}:
            min_rep, max_rep, next_i = parse_quantifier(regex, i+1)
            char_to_match = regex[i]
            count = 0
            while j < len(text) and count < max_rep and (char_to_match == '*' or text[j] == char_to_match):
                j += 1
                count += 1
            if count < min_rep:
                return False
            i = next_i
        elif regex[i] == '(':
            options, end = parse_group(regex[i:])
            if not any(reg_compare(opt + regex[i+end+1:], text[j:]) for opt in options):
                return False
            i += end + 1
        elif regex[i] == '[':
            end = regex.index(']', i)
            if j >= len(text) or text[j] not in parse_range(regex[i+1:end]):
                return False
            i, j = end + 1, j + 1
        elif regex[i] == '*':
            i, j = i + 1, min(j + 1, len(text))
        elif j < len(text) and regex[i] == text[j]:
            i, j = i + 1, j + 1
        else:
            return False
    return i == len(regex) and j == len(text)

def afficher_resultats(regex, tests):
    print(f"Regex analysée : {regex}")
    for test in tests:
        result = "✓" if reg_compare(regex, test) else "✗"
        print(f"{test.ljust(15)} {result}")

# Exemple d'utilisation
regex = "[A-Z]a{1,3}(1|2)+[0-9]"
tests = ["Xa211", "Yaaa222", "Za1", "Baaaa3", "Ca21", "Da1111"]
afficher_resultats(regex, tests)
