from gmpy2 import invert
def SM3_padding(m: bytes):  # 与SHA1一样
    k = len(m)
    r = 64 - (k + 8) % 64
    padding = bytearray.fromhex('80' + '00' * (r - 1) + hex(8 * k)[2:].zfill(16))
    return m + padding


def SM3_grouping(m: bytes):  # 可与padding合并
    l = len(m)
    B = []
    for i in range(0, l, 64):
        B.append(m[i:i + 64])
    return B


def XOR(x, y):  # 字节异或
    l = len(x)
    x = int.from_bytes(x, byteorder='big')
    y = int.from_bytes(y, 'big')
    return (x ^ y).to_bytes(l, 'big')


def CLS(v: bytes, s):  # 循环左移
    # 将字节v循环左移s位
    l = len(v)
    _ = int.from_bytes(v, 'big')
    result = (((_ << s) & ((1 << 8 * l) - 1)) + (_ >> (l * 8 - s))).to_bytes(l, 'big')
    return result


def SM3_P(X: bytes, mode):
    if mode == 0:
        return XOR(X, XOR(CLS(X, 9), CLS(X, 17)))
    else:
        return XOR(X, XOR(CLS(X, 15), CLS(X, 23)))


def SM3_extend(B: bytes):
    W = [b''] * 68
    W_ = [b''] * 64
    for i in range(16):
        W[i] = B[4 * i:4 * (i + 1)]
    for i in range(16, 68):
        W[i] = XOR(SM3_P(XOR(XOR(W[i - 16], W[i - 9]), CLS(W[i - 3], 15)), 1), XOR(CLS(W[i - 13], 7), W[i - 6]))
    for i in range(64):
        W_[i] = XOR(W[i], W[i + 4])
    return W, W_


def SM3_T(t):
    if 0 <= t <= 15:
        return 0x79cc4519.to_bytes(4, 'big')
    else:
        return 0x7a879d8a.to_bytes(4, 'big')


def FF(X, Y, Z, t):
    if 0 <= t <= 15:
        return XOR(XOR(X, Y), Z)
    else:
        return ((int.from_bytes(X, 'big') & int.from_bytes(Y, 'big')) |
                (int.from_bytes(X, 'big') & int.from_bytes(Z, 'big')) |
                (int.from_bytes(Y, 'big') & int.from_bytes(Z, 'big'))).to_bytes(4, 'big')


def GG(X, Y, Z, t):
    if 0 <= t <= 15:
        return XOR(XOR(X, Y), Z)
    else:
        return ((int.from_bytes(X, 'big') & int.from_bytes(Y, 'big')) |
                ((~int.from_bytes(X, 'big')) & int.from_bytes(Z, 'big'))).to_bytes(4, 'big')


def SM3_CF(V: bytes, W, W_):
    A, B, C, D, E, F, G, H = V[0:4], V[4:8], V[8:12], V[12:16], V[16:20], V[20:24], V[24:28], V[28:32]
    for i in range(64):
        SS1 = CLS(((int.from_bytes(CLS(A, 12), 'big') +
                    int.from_bytes(E, 'big') +
                    int.from_bytes(CLS(SM3_T(i), i % 32), 'big')) & ((1 << 32) - 1)).to_bytes(4, 'big'), 7)
        SS2 = XOR(SS1, CLS(A, 12))
        TT1 = ((int.from_bytes(FF(A, B, C, i), 'big') +
                int.from_bytes(D, 'big') +
                int.from_bytes(SS2, 'big') +
                int.from_bytes(W_[i], 'big')) & ((1 << 32) - 1)).to_bytes(4, 'big')
        TT2 = ((int.from_bytes(GG(E, F, G, i), 'big') +
                int.from_bytes(H, 'big') +
                int.from_bytes(SS1, 'big') +
                int.from_bytes(W[i], 'big')) & ((1 << 32) - 1)).to_bytes(4, 'big')
        D = C
        C = CLS(B, 9)
        B = A
        A = TT1
        H = G
        G = CLS(F, 19)
        F = E
        E = SM3_P(TT2, 0)
    return XOR(A + B + C + D + E + F + G + H, V)


def SM3(m):
    IV = 0x7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e.to_bytes(32, byteorder='big')
    M = SM3_padding(m)
    B = SM3_grouping(M)
    V = [IV]
    for i in range(len(B)):
        W, W_ = SM3_extend(B[i])
        V.append(SM3_CF(V[i], W, W_))
    return hex(int.from_bytes(V[-1], 'big'))[2:].zfill(64)


def EC_add(P, Q):
    if P == [0, 0]:
        return Q
    if Q == [0, 0]:
        return P
    if P[0] == Q[0] and (P[1] + Q[1]) % p == 0:
        return [0, 0]
    if P != Q:
        delta = ((Q[1] - P[1]) * invert((Q[0] - P[0]), p)) % p
    else:
        delta = ((3 * P[0] ** 2 + a) * invert(2 * P[1], p)) % p
    R = [0, 0]
    R[0] = (delta ** 2 - P[0] - Q[0]) % p
    R[1] = (delta * (P[0] - R[0]) - P[1]) % p
    return R


def EC_multiply(k, P):
    res = [0, 0]
    Q = P
    while k > 0:
        if k & 1:
            res = EC_add(res, Q)
        Q = EC_add(Q, Q)
        k >>= 1
    return res


def sign(Z, m: str, d, k):
    M = bytearray.fromhex(Z) + m.encode('utf-8')
    e = int(SM3(M), 16)
    G1 = EC_multiply(k, G)
    r = (e + G1[0]) % n
    s = (invert(1 + d, n) * (k - r * d)) % n
    return r, s


def vrfy(Z, P, m: str, r, s):
    if not 1 <= r <= n - 1:
        return 'False'
    if not 1 <= s <= n - 1:
        return 'False'
    M = bytearray.fromhex(Z) + m.encode('utf-8')
    e = int(SM3(M), 16)
    t = (r + s) % n
    if t == 0:
        return 'False'
    G1 = EC_add(EC_multiply(s, G), EC_multiply(t, P))
    v = (e + G1[0]) % n
    if v == r:
        return 'True'
    else:
        return 'False'


def adjust(x: int):
    x_ = hex(x)[2:]
    if len(x_) & 1 == 1:
        x_ = '0' + x_
    return bytearray().fromhex(x_)


def main():
    global p, a, b, G, n
    p = int(input())
    a, b = int(input()), int(input())
    G = list(map(int, input().split()))
    n = int(input())
    ID = input().strip().encode('utf-8')
    P = list(map(int, input().split()))
    m = input().strip()
    mode = input().strip()
    entlen = len(ID) * 8
    ENTL = bytearray.fromhex(hex(entlen)[2:].zfill(4))
    Z = SM3(ENTL + ID + adjust(a) + adjust(b) + adjust(G[0]) + adjust(G[1]) + adjust(P[0]) + adjust(P[1]))
    if mode == 'Sign':
        d = int(input())
        k = int(input())
        r, s = sign(Z, m, d, k)
        print(r, s, end='\n')
    else:
        r = int(input())
        s = int(input())
        print(vrfy(Z, P, m, r, s))


if __name__ == '__main__':
    main()