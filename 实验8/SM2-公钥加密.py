from hashlib import sha256
from math import ceil


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


def bin_to_hex(s):  # bin与hex来回转化需要int，看着太麻烦了
    # if len(s) % 4 != 0:
    #     print('Did you forget to replenish zero?')
    #     s = '0' * (len(s) % 4) + s
    dic = {'0000': '0', '0001': '1', '0010': '2', '0011': '3',
           '0100': '4', '0101': '5', '0110': '6', '0111': '7',
           '1000': '8', '1001': '9', '1010': 'a', '1011': 'b',
           '1100': 'c', '1101': 'd', '1110': 'e', '1111': 'f',}
    result = ''
    for i in range(0, len(s), 4):
        result += dic[s[i:i+4]]
    return result


def hex_to_bin(s):
    dic = {'0': '0000', '1': '0001', '2': '0010', '3': '0011',
           '4': '0100', '5': '0101', '6': '0110', '7': '0111',
           '8': '1000', '9': '1001', 'a': '1010', 'b': '1011',
           'c': '1100', 'd': '1101', 'e': '1110', 'f': '1111', }
    result = ''
    for i in s:
        result += dic[i]
    return result


def KDF(Z, klen):
    """
    :param Z: 比特串
    :param klen: 要获得的密钥数据的比特长度
    :return: 长度为klen的密钥数据比特串K
    """
    # v为密码杂凑函数的返回比特长度
    # if klen >= ((1 << 32) - 1) * v:
    #     return 'error'
    v = 256  # sha256返回256比特
    ct = 0x00000001
    K = ''
    for i in range(ceil(klen / v)):
        K += hex_to_bin(sha256(bytearray.fromhex(bin_to_hex(Z + bin(ct)[2:].zfill(32)))).hexdigest())
        ct += 1
    return K[:klen]


def SM2(p, a, G, Par, mode, text, P, d, k):
    if mode == 1:
        m = hex_to_bin(text)
        klen = len(m)
        C1 = EC_multiply(G, k, a, p)
        x, y = EC_multiply(P, k, a, p)
        t = KDF(bin(x)[2:].zfill(Par) + bin(y)[2:].zfill(Par), klen)
        C2 = bin(int(m, 2) ^ int(t, 2))[2:].zfill(klen)
        C3 = hex_to_bin(sha256(bytearray.fromhex(bin_to_hex(bin(x)[2:].zfill(Par) + m + bin(y)[2:].zfill(Par)))).hexdigest())
        return bin_to_hex(bin(C1[0])[2:].zfill(Par) + bin(C1[1])[2:].zfill(Par) + C2 + C3)
    else:
        text = text[2:]  # 去除04
        C1 = [int(text[:Par // 4], 16), int(text[Par // 4:Par // 2], 16)]
        C2 = text[Par // 2:-64]
        C3 = text[-64:]
        x, y = EC_multiply(C1, d, a, p)
        klen = len(C2) * 4
        t = KDF(bin(x)[2:].zfill(Par) + bin(y)[2:].zfill(Par), klen)
        m = hex(int(C2, 16) ^ int(t, 2))
        return m


def main():
    p = int(input())
    a, b = int(input()), int(input())
    G = list(map(int, input().split()))
    Par = int(input())
    mode = int(input())
    text = input().strip()[2:]
    if mode == 1:
        P = list(map(int, input().split()))
        k = int(input())
        cipher = SM2(p, a, G, Par, mode, text, P, 0, k)
        print('0x04' + cipher)
    else:
        d = int(input())
        plaintext = SM2(p, a, G, Par, mode, text, 0, d, 0)
        print(plaintext)


if __name__ == '__main__':
    main()
