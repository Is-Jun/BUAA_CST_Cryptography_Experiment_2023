def Hash_padding(m: bytes):
    k = len(m)
    r = 64 - (k + 8) % 64
    padding = bytearray.fromhex('80' + '00' * (r - 1) + hex(8 * k)[2:].zfill(16))
    return m + padding


def Hash_grouping(m: bytes):  # 可与padding合并
    l = len(m)
    result = []
    for i in range(0, l, 64):
        result.append(m[i:i + 64])
    return result


def XOR(x, y):  # 字节异或
    l = len(x)
    x = int.from_bytes(x, byteorder='big')
    y = int.from_bytes(y, 'big')
    return (x ^ y).to_bytes(l, 'big')


def CLS(v: bytes, s: int):  # 循环左移
    # 将字节v循环左移s位
    l = len(v)
    _ = int.from_bytes(v, 'big')
    result = (((_ << s) & ((1 << 8 * l) - 1)) + (_ >> (l * 8 - s))).to_bytes(l, 'big')
    return result


def Hash_extend(Y: bytes):
    W = [b''] * 80
    for i in range(16):
        W[i] = Y[4 * i:4 * (i + 1)]
    for i in range(16, 80):
        W[i] = CLS(XOR(XOR(W[i - 3], W[i - 8]), XOR(W[i - 14], W[i - 16])), 1)
    return W


def Hash_f(x: bytes, y: bytes, z: bytes, t: int):
    l = len(x)
    x = int.from_bytes(x, 'big')
    y = int.from_bytes(y, 'big')
    z = int.from_bytes(z, 'big')
    if 0 <= t <= 19:
        result = (x & y) | ((~x) & z)
    elif 20 <= t <= 39:
        result = x ^ y ^ z
    elif 40 <= t <= 59:
        result = (x & y) | (x & z) | (y & z)
    else:
        result = x ^ y ^ z
    result = result.to_bytes(l, 'big')
    return result


def Hash_K(t):
    if 0 <= t <= 19:
        return 0x5A827999.to_bytes(4, byteorder='big')
    elif 20 <= t <= 39:
        return 0x6ED9EBA1.to_bytes(4, byteorder='big')
    elif 40 <= t <= 59:
        return 0x8F1BBCDC.to_bytes(4, byteorder='big')
    else:
        return 0xCA62C1D6.to_bytes(4, byteorder='big')


def Hash_round(W, A, B, C, D, E):
    l = len(A)
    a, b, c, d, e = A, B, C, D, E
    for t in range(80):
        _ = ((int.from_bytes(CLS(a, 5), 'big') + int.from_bytes(Hash_f(b, c, d, t), 'big')
              + int.from_bytes(e, 'big') + int.from_bytes(W[t], 'big')
              + int.from_bytes(Hash_K(t), 'big')) & ((1 << 32) - 1)).to_bytes(l, 'big')
        a, b, c, d, e = _, a, CLS(b, 30), c, d
    A = ((int.from_bytes(A, 'big') + int.from_bytes(a, 'big')) & ((1 << 32) - 1)).to_bytes(l, 'big')
    B = ((int.from_bytes(B, 'big') + int.from_bytes(b, 'big')) & ((1 << 32) - 1)).to_bytes(l, 'big')
    C = ((int.from_bytes(C, 'big') + int.from_bytes(c, 'big')) & ((1 << 32) - 1)).to_bytes(l, 'big')
    D = ((int.from_bytes(D, 'big') + int.from_bytes(d, 'big')) & ((1 << 32) - 1)).to_bytes(l, 'big')
    E = ((int.from_bytes(E, 'big') + int.from_bytes(e, 'big')) & ((1 << 32) - 1)).to_bytes(l, 'big')
    return A, B, C, D, E


def SHA1(m: bytes):
    A = 0X67452301.to_bytes(4, 'big')
    B = 0XEFCDAB89.to_bytes(4, 'big')
    C = 0X98BADCFE.to_bytes(4, 'big')
    D = 0X10325476.to_bytes(4, 'big')
    E = 0XC3D2E1F0.to_bytes(4, 'big')
    # 填充
    m = Hash_padding(m)
    # 分组
    Y = Hash_grouping(m)
    # 轮函数
    for i in range(len(Y)):
        W = Hash_extend(Y[i])
        A, B, C, D, E = Hash_round(W, A, B, C, D, E)
    result = hex(int.from_bytes(A + B + C + D + E, 'big'))[2:].zfill(40)
    return result


def main():
    m = input().strip()
    # from hashlib import sha1
    # print('my SHA-1:      ', end=' ')
    print(SHA1(m.encode('utf-8')))
    # print('standard SHA-1:', sha1(m.encode('utf-8')).hexdigest())


if __name__ == '__main__':
    main()