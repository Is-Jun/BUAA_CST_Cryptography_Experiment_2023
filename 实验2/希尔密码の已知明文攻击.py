import random


def extend_gcd(a, b):
    if b == 0:
        return 1, 0, a
    else:
        _x, _y, gcd = extend_gcd(b, a % b)
        x = _y
        y = _x - int(a // b) * _y
        if gcd < 0:
            gcd = -gcd
            x = -x
            y = -y
    return x, y, gcd


def mod_inv(a, n):
    x, y, gcd = extend_gcd(a, n)
    return x % n, gcd


def matrix_mul(matrix1, matrix2):
    n, m = len(matrix1), len(matrix1[0])
    matrix = [[0 for i in range(m)] for j in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(m):
                matrix[i][j] += matrix1[i][k] * matrix2[k][j]
            matrix[i][j] %= 26
    return matrix


def sub_matrix(matrix, i, j):
    # 矩阵matrix第i行第j列元素的余矩阵
    n, m = len(matrix), len(matrix[0])
    result = []
    result = [[matrix[x][y] for y in range(m) if y != j] for x in range(n) if x != i]
    return result


def det_matrix(matrix):
    n, m = len(matrix), len(matrix[0])
    if n == 1 and m == 1:
        return matrix[0][0]
    else:
        value = 0
        for j in range(m):
            value += ((-1) ** (j + 2)) * matrix[0][j] * det_matrix(sub_matrix(matrix, 0, j))
        return value


def matrix_inv(matrix):
    n = len(matrix)
    result = []
    inv, gcd = mod_inv(det_matrix(matrix), 26)
    if gcd != 1:
        return result
    for i in range(n):
        list_ = []
        for j in range(n):
            list_.append(((-1) ** (i + j + 2)) * det_matrix(sub_matrix(matrix, j, i)) * inv % 26)
        result.append(list_)
    return result


def hill_known_plaintext_attack(n, plaintext, cipher):
    while True:
        random_num = []
        while True:
            num = random.randint(0, len(plaintext) - 1)
            if num not in random_num:
                random_num.append(num)
                if len(random_num) == n:
                    break
        m = [plaintext[i] for i in random_num]
        m_ = matrix_inv(m)
        if m_ == []:
            continue
        s = [cipher[i] for i in random_num]
        key = matrix_mul(m_, s)
        return key


n = int(input())
m = input().strip()
s = input().strip()

plaintext = [[ord(m[i * n + j]) - ord('a') for j in range(n)] for i in range(len(m) // n)]
cipher = [[ord(s[i * n + j]) - ord('a') for j in range(n)] for i in range(len(s) // n)]

k = hill_known_plaintext_attack(n, plaintext, cipher)

for i in range(n):
    for j in range(n):
        print(k[i][j], end=' ')
    print()
