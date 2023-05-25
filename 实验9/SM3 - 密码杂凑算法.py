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


def main():
    # 如果输入为空串的话，本地是否去掉strip都可以获得正确答案，但提交到OJ上需要去掉！！！！！
    m = input()
    print(SM3(m.encode('utf-8')))


if __name__ == '__main__':
    main()