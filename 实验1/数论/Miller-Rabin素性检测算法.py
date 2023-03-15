import random


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def quick_pow(b, n, m):
    n_binary = []
    while n != 0:
        n_binary.append(n % 2)
        n = n // 2
    n_binary[:] = n_binary[::-1]
    c = 1
    for i in n_binary:
        c = c * c % m
        if i:
            c = c * b % m
    return c


def prime_test_miller_rabin(p):
    if p < 2:
        return False
    if p == 2 or p == 3:
        return True
    if p & 1 == 0:
        return False
    # p - 1 = 2**k * q
    k, q = 0, p - 1
    while q and q & 1 == 0:
        k += 1
        q >>= 1
    for j in range(30):
        a = random.randint(2, p - 2)
        if gcd(a, p) != 1:
            return False
        b = quick_pow(a, q, p)
        if b == 1 or b == p - 1:  # 不一定是素数
            continue
        for i in range(k):
            b = quick_pow(b, 2, p)
            if b == 1:
                return False
            if b == p - 1:
                if i < k - 1:
                    break
                else:
                    return False
        else:
            return False
    return True


p = int(input())

if prime_test_miller_rabin(p):
    print('YES')
else:
    print('NO')