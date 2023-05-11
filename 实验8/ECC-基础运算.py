def extend_gcd(a, b):
    if b == 0:
        return 1, 0, a
    else:
        ppx, ppy, gcd = extend_gcd(b, a % b)
        x = ppy
        y = ppx - int(a // b) * ppy
        return x, y, gcd


# 求逆元算法
def mod_inverse(a, n):
    if n < 2:
        raise ValueError("modulus must be greater than 1")
    x, y, gcd = extend_gcd(a, n)
    if gcd != 1:
        raise ValueError("No inverse element!")
    else:
        return x % n


def EC_add(P, Q, a, p):
    if P == [0, 0]:
        return Q
    if Q == [0, 0]:
        return P
    if P[0] == Q[0] and (P[1] + Q[1]) % p == 0:
        return [0, 0]
    if P != Q:
        delta = ((Q[1] - P[1]) * mod_inverse((Q[0] - P[0]), p)) % p
    else:
        delta = ((3 * P[0] ** 2 + a) * mod_inverse(2 * P[1], p)) % p
    R = [0, 0]
    R[0] = (delta ** 2 - P[0] - Q[0]) % p
    R[1] = (delta * (P[0] - R[0]) - P[1]) % p
    return R


def EC_subtract(P, Q, a, p):
    Q[1] = (-Q[1]) % p
    return EC_add(P, Q, a, p)


def EC_number_multiply(P, k, a, p):
    res = [0, 0]
    Q = P
    while k > 0:
        if k & 1:
            res = EC_add(res, Q, a, p)
        Q = EC_add(Q, Q, a, p)
        k >>= 1
    return res


def main():
    p = int(input())
    a = int(input())
    b = int(input())
    P = list(map(int, input().split()))
    Q = list(map(int, input().split()))
    k = int(input())
    r1 = EC_add(P, Q, a, p)
    print(r1[0], r1[1])
    r2 = EC_subtract(P, Q, a, p)
    print(r2[0], r2[1])
    r3 = EC_number_multiply(P, k, a, p)
    print(r3[0], r3[1])


if __name__ == '__main__':
    # main()
    while True:
        main()
        print('-' * 64)
