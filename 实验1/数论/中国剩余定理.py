def extend_gcd(a, b):
    flag = 0
    if a < b:
        flag = 1
        a, b = b, a
    x1, x2, x3 = 1, 0, a
    y1, y2, y3 = 0, 1, b
    while y3 != 0:
        Q = x3 // y3
        t1, t2, t3 = x1 - Q * y1, x2 - Q * y2, x3 - Q * y3
        x1, x2, x3 = y1, y2, y3
        y1, y2, y3 = t1, t2, t3
    if flag == 0:
        return x1, x2, x3
    else:
        return x2, x1, x3


def mod_inverse(a, n):
    x, y, gcd = extend_gcd(a, n)
    return x % n


def CRT(m, a):
    M = 1
    t = []
    for i in range(3):
        M *= m[i]
    for i in range(3):
        t.append(mod_inverse(M // m[i], m[i]))
    x = 0
    for i in range(3):
        x += a[i] * t[i] * (M // m[i])

    if x % M == 0:
        x = M
    else:
        x %= M
    return x


s1 = input()
s2 = input()
m = []
a = []

for i in range(3):
    m.append(int(s1.split(' ')[i]))

for i in range(3):
    a.append(int(s2.split(' ')[i]))

result = CRT(m, a)
print(result)
