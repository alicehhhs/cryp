from collections import Counter

frequent_bigrams = ['ст', 'но', 'то', 'на', 'ен']

excluded_list = ["аь", "еь", "иь", "оь", "уь",
                 "ьь", "ыь", "эь", "юь", "яь"]

alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'

with open("11.txt", "r", encoding="utf-8-sig") as file:
    raw_text = file.read()
text = ''.join(i for i in raw_text if i in alphabet)

bi_list = []
for i in range(0, len(text) - 1, 2):
    bi_list.append(text[i:i + 2])
bi_counter = Counter(bi_list)
sorted_bi_counter = {key: val for key, val in sorted(bi_counter.items(),
                                                     key=lambda ele: ele[1], reverse=True)}
temp_top_bigrams = []
for i in sorted_bi_counter:
    temp_top_bigrams.append(i)
top_bigrams = []
for i in range(0, 5):
    top_bigrams.append(temp_top_bigrams[i])


def greatest_common_divisor(a, b):
    if b == 0:
        return abs(a)
    else:
        return greatest_common_divisor(b, a % b)


def extended_euclidean_algorithm(a, n):
    res = [0, 1]
    while n != 0 and a != 0:
        if n < a:
            res.append(a // n)
            a = a % n
        elif n > a:
            res.append(n // a)
            n = n % a
    for i in range(2, len(res) - 1):
        res[i] = res[i - 2] + (-res[i] * res[i - 1])
    return res[-2]


def modular_equation_solver(a, b, n):
    a = a % n
    b = b % n
    d = greatest_common_divisor(a, n)
    result = []
    if d == 1:
        x = (extended_euclidean_algorithm(a, n) * b) % n
        result.append(x)
        return result
    else:
        if b % d == 0:
            a = a // d
            b = b // d
            n = n // d
            x = (modular_equation_solver(a, b, n)[0])
            result.append(x)
            for i in range(1, d):
                result.append(result[-1] + n)
            return result
        else:
            return result


def index_of_bigram(bigram):
    temp = []
    temp.append(alphabet.index(bigram[0]))
    temp.append(alphabet.index(bigram[1]))
    ind = temp[0] * 31 + temp[1]
    return ind


def decrypt_text(text, key):
    plaintext = []
    a, b = key[0], key[1]
    for i in range(0, len(text) - 1, 2):
        x = (extended_euclidean_algorithm(a, 31 ** 2) * (index_of_bigram(text[i:i + 2]) - b)) % (31 ** 2)
        plaintext.append(alphabet[x // 31] + alphabet[x % 31])

    decrypted_text = ''.join(i for i in plaintext)
    return decrypted_text


def generate_combinations(frequent_bigrams, cy_bigrams):
    bi = []
    comb = []
    for i in frequent_bigrams:
        for j in cy_bigrams:
            bi.append((i, j))
    for i in bi:
        for j in bi:
            if i == j or (j, i) in comb:
                continue
            elif i[0] == j[0] or i[1] == j[1]:
                continue
            comb.append((i, j))
    return comb


combinations = generate_combinations(frequent_bigrams, top_bigrams)


def find_ab_values(combinations):
    ab_values = []
    x1 = index_of_bigram(combinations[0][0])
    x2 = index_of_bigram(combinations[1][0])
    y1 = index_of_bigram(combinations[0][1])
    y2 = index_of_bigram(combinations[1][1])
    a_values = modular_equation_solver(x1 - x2, y1 - y2, 31 ** 2)
    for a in a_values:
        if greatest_common_divisor(a, 31) != 1:
            continue
        b = (y1 - a * x1) % 31 ** 2
        ab_values.append((a, b))
    return ab_values


ab_values_list = []
for comb in combinations:
    temp = find_ab_values(comb)
    if len(temp) != 0:
        for value in temp:
            ab_values_list.append(value)


valid_keys = []
for ab_value in ab_values_list:
    check = 0
    temp_text = decrypt_text(text, ab_value)
    for imp in excluded_list:
        if imp in temp_text:
            check = 1
    if check == 0:
        valid_keys.append(ab_value)

print(valid_keys)
print(decrypt_text(text, valid_keys[0]))
