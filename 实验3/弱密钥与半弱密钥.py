def inv_key(k):
    key_sub1 = [57, 49, 41, 33, 25, 17,  9,  1, 58, 50, 42, 34, 26, 18,
                10,  2, 59, 51, 43, 35, 27, 19, 11,  3, 60, 52, 44, 36,
                63, 55, 47, 39, 31, 23, 15,  7, 62, 54, 46, 38, 30, 22,
                14,  6, 61, 53, 45, 37, 29, 21, 13,  5, 28, 20, 12,  4]
    list_ = [0] * 64
    for i in range(len(key_sub1)):
        list_[key_sub1[i] - 1] = k[i]

    for i in range(8):
        for ll in range(7):
            list_[i * 8 + 7] ^= int(list_[i * 8 + ll])
        list_[i * 8 + 7] = str(list_[i * 8 + 7])
    _ = ''
    for i in list_:
        _ += i
    even = '0x' + hex(int(_, base=2))[2:].zfill(16)
    for i in range(8):
        list_[i * 8 + 7] = '1' if list_[i * 8 + 7] == '0' else '0'
    _ = ''
    for i in list_:
        _ += i
    odd = '0x' + hex(int(_, base=2))[2:].zfill(16)
    return even, odd


def get_weak_key():
    part = ['0000000000000000000000000000', '1111111111111111111111111111']

    result = []
    for i in part:
        for j in part:
            even, odd = inv_key(i + j)
            result.append(even)
            result.append(odd)
    return result


def get_semi_weak_key():
    part1 = ['00' * 14, '11' * 14]
    part2 = ['01' * 14, '10' * 14]
    result = []
    for i in range(12):
        result.append(['', ''])
    # [[00, 01], [00, 10]] [[11, 01], [11, 10]]
    count = 0
    for i in range(2):
        for j in range(2):
            even, odd = inv_key(part1[i] + part2[j])
            result[count][j] = even
            result[count + 1][j] = odd
        count += 2
    # [[10, 00], [01, 00]] [[10, 11], [01, 11]]
    for i in range(2):
        for j in range(2):
            even, odd = inv_key(part2[j] + part1[i])
            result[count][j] = even
            result[count + 1][j] = odd
        count += 2
    # [[10, 10], [01, 01]] [[10, 01], [01, 10]]
    even, odd = inv_key(part2[0] + part2[0])
    result[count][0] = even
    result[count + 1][0] = odd
    even, odd = inv_key(part2[1] + part2[1])
    result[count][1] = even
    result[count + 1][1] = odd
    count += 2
    even, odd = inv_key(part2[1] + part2[0])
    result[count][0] = even
    result[count + 1][0] = odd
    even, odd = inv_key(part2[0] + part2[1])
    result[count][1] = even
    result[count + 1][1] = odd
    return result


for i in get_weak_key():
    print(i)

for i in get_semi_weak_key():
    print(i[0], i[1])
