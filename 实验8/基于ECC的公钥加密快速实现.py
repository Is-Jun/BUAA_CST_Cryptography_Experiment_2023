def extend_gcd(a, b):
    # if b == 0:
    #     return 1, 0, a
    # else:
    #     ppx, ppy, gcd = extend_gcd(b, a % b)
    #     x = ppy
    #     y = ppx - int(a // b) * ppy
    #     return x, y, gcd
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
        delta = ((Q[1] - P[1]) * mod_inverse((Q[0] - P[0]) % p, p)) % p
    else:
        delta = ((3 * P[0] ** 2 + a) * mod_inverse(2 * P[1], p)) % p
    R = [0, 0]
    R[0] = (delta ** 2 - P[0] - Q[0]) % p
    R[1] = (delta * (P[0] - R[0]) - P[1]) % p
    return R


def EC_subtract(P, Q, a, p):
    Q[1] = (-Q[1]) % p
    return EC_add(P, Q, a, p)


def EC_multiply(P, k, a, p):
    res = [0, 0]
    Q = P
    while k > 0:
        if k & 1:
            res = EC_add(res, Q, a, p)
        Q = EC_add(Q, Q, a, p)
        k >>= 1
    return res


def ECC(p, a, G, mode, P, Q, k, N):
    if mode == 1:
        cipher = [[], []]
        cipher[0] = EC_multiply(G, k, a, p)
        _ = EC_multiply(Q, k, a, p)
        cipher[1] = EC_add(P, _, a, p)
        _ = EC_multiply(_, N, a, p)
        cipher[1] = EC_add(cipher[1], _, a, p)
        return cipher
    else:
        _ = EC_multiply(P, k, a, p)
        _ = EC_multiply(_, N + 1, a, p)
        plaintext = EC_subtract(Q, _, a, p)
        return plaintext


def main():
    p = int(input())
    a, b = int(input()), int(input())
    G = list(map(int, input().split()))
    mode = int(input())
    P = list(map(int, input().split()))
    if mode == 1:
        k = int(input())
        Q = list(map(int, input().split()))
    else:
        Q = list(map(int, input().split()))
        k = int(input())
    N = int(input())
    result = ECC(p, a, G, mode, P, Q, k, N)
    if mode == 1:
        print(result[0][0], result[0][1])
        print(result[1][0], result[1][1])
    else:
        print(result[0], result[1])


if __name__ == '__main__':
    main()