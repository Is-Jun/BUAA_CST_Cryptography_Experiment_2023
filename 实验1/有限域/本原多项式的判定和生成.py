def mod(a, b):
    while len(bin(a)) >= len(bin(b)):
        if a == 0:
            break
        rec = len(bin(a)) - len(bin(b))
        a ^= (b << rec)
    return a


def gcd(a, b):
    while b:
        a, b = b, mod(a, b)
    return a


def Ben_Or(n, f):
    i = 1
    while True:
        if i > n / 2:
            return True  # f is irreducible
        else:
            if gcd(f, mod((2 ** (2 ** n - 1)) ** i - 2, f)) == 1:
                i += 1
            else:
                return False  # f is reducible


def pri_poly(n):
    m = 2 ** n - 1
    F = 2 ** m + 1
    poly = []
    for f in range(2 ** n, 2 ** (n + 1)):
        if Ben_Or(n, f):
            if mod(F, f) == 0:
                flag = 0
                for q in range(m):
                    if mod(2 ** q + 1, f) == 0:
                        flag = 1
                        break
                if flag == 0:
                    poly.append(bin(f)[2:])
    return poly


# n = int(input('请输入GF(2)上所需生成的本原多项式次数'))
n = 8
result = pri_poly(n)
print(*result)
