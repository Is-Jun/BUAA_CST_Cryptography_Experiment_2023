def matrix_cipher(n, k, s, way):
    matrix = []
    m = len(s) // n
    for i in range(m):
        list_ = []
        for j in range(n):
            list_.append('')
        matrix.append(list_)
    if way == 1:
        cipher = ''
        for i in range(m):
            for j in range(n):
                matrix[i][j] = s[i * n + j]
        for i in range(n):
            for j in range(m):
                cipher += matrix[j][k[i]]
        return cipher
    else:
        plaintext = ''
        for i in range(n):
            for j in range(m):
                matrix[j][k[i]] = s[i * m + j]
        for i in range(m):
            for j in range(n):
                plaintext += matrix[i][j]
        return plaintext


n = int(input())
k_ = input().strip()
s = input().strip()
way = int(input())

k = {}
for i in range(n):
    k[int(k_[i]) - 1] = i

print(matrix_cipher(n, k, s, way))


