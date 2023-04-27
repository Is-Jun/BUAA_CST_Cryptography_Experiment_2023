def extend_gcd(a, b):
    if b == 0:
        return 1, 0, a
    else:
        ppx, ppy, gcd = extend_gcd(b, a % b)
        x = ppy
        y = ppx - int(a // b) * ppy
        return x, y, gcd


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


def EC_multiply(P, k, a, p):
    res = [0, 0]
    Q = P
    while k > 0:
        if k & 1:
            res = EC_add(res, Q, a, p)
        Q = EC_add(Q, Q, a, p)
        k >>= 1
    return res


def ECC(p, a, G, mode, P, Q, k):
    if mode == 1:
        cipher = [[], []]
        cipher[0] = EC_multiply(G, k, a, p)
        cipher[1] = EC_add(P, EC_multiply(Q, k, a, p), a, p)
        return cipher
    else:
        plaintext = EC_subtract(Q, EC_multiply(P, k, a, p), a, p)
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
    result = ECC(p, a, G, mode, P, Q, k)
    if mode == 1:
        print(result[0][0], result[0][1])
        print(result[1][0], result[1][1])
    else:
        print(result[0], result[1])


if __name__ == '__main__':
    # main()
    while True:
        main()
        print('-' * 64)