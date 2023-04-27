from math import ceil, log
from hashlib import sha256


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


def SM2_DH_A(p, a, b, G, n, IDA, IDB, dA, PA, PB, rA, RB):
    h = 1  # 余因子
    klen = 128
    Par = 256  # 安全参数
    w = ceil(ceil(log(n, 2)) / 2) - 1
    # step 1 产生随机数rA
    # step 2 计算RA=rA·G=(x1,y1)
    RA = EC_multiply(G, rA, a, p)
    # step 3 将RA发送给B
    # step 4 计算x1_如下
    x1_ = (1 << w) + (RA[0] & ((1 << w) - 1))
    # step 5 计算tA
    tA = (dA + x1_ * rA) % n
    # step 6 计算x2_如下
    x2_ = (1 << w) + (RB[0] & ((1 << w) - 1))
    # step 7 计算椭圆曲线点
    U = EC_multiply(EC_add(PB, EC_multiply(RB, x2_, a, p), a, p), h * tA, a, p)
    # step 8 计算KA
    entlenA, entlenB = len(IDA) * 4, len(IDB) * 4
    ENTLA, ENTLB = hex(entlenA)[2:].zfill(4), hex(entlenB)[2:].zfill(4)
    ZA = sha256(bytearray.fromhex(ENTLA + IDA + hex(a)[2:].zfill(Par // 4) + hex(b)[2:].zfill(Par // 4)
                                  + hex(G[0])[2:].zfill(Par // 4) + hex(G[1])[2:].zfill(Par // 4)
                                  + hex(PA[0])[2:].zfill(Par // 4) + hex(PA[1])[2:].zfill(Par // 4))).hexdigest()
    ZB = sha256(bytearray.fromhex(ENTLB + IDB + hex(a)[2:].zfill(Par // 4) + hex(b)[2:].zfill(Par // 4)
                                  + hex(G[0])[2:].zfill(Par // 4) + hex(G[1])[2:].zfill(Par // 4)
                                  + hex(PB[0])[2:].zfill(Par // 4) + hex(PB[1])[2:].zfill(Par // 4))).hexdigest()
    KA = KDF(bin(U[0])[2:].zfill(Par) + bin(U[1])[2:].zfill(Par) + hex_to_bin(ZA) + hex_to_bin(ZB), klen)
    # step 9 计算S1
    _ = sha256(bytearray.fromhex(hex(U[0])[2:].zfill(Par // 4) + ZA + ZB
                                 + hex(RA[0])[2:].zfill(Par // 4) + hex(RA[1])[2:].zfill(Par // 4)
                                 + hex(RB[0])[2:].zfill(Par // 4) + hex(RB[1])[2:].zfill(Par // 4))).hexdigest()
    S1 = sha256(bytearray.fromhex('02' + hex(U[1])[2:].zfill(Par // 4) + _)).hexdigest()
    # step 10 计算SA并发送给B
    SA = sha256(bytearray.fromhex('03' + hex(U[1])[2:].zfill(Par // 4) + _)).hexdigest()
    return int(KA, 2), int(S1, 16), int(SA, 16)


def SM2_DH_B(p, a, b, G, n, IDA, IDB, dB, PA, PB, rB, RA):
    h = 1  # 余因子
    klen = 128
    Par = 256  # 安全参数
    w = ceil(ceil(log(n, 2)) / 2) - 1
    # step 1 产生随机数rB
    # step 2 计算RB=rB·G=(x2,y2)
    RB = EC_multiply(G, rB, a, p)
    # step 3 计算x2_如下
    x2_ = (1 << w) + (RB[0] & ((1 << w) - 1))
    # step 4 计算tB
    tB = (dB + x2_ * rB) % n
    # step 5 计算x1_如下
    x1_ = (1 << w) + (RA[0] & ((1 << w) - 1))
    # step 6 计算椭圆曲线点
    V = EC_multiply(EC_add(PA, EC_multiply(RA, x1_, a, p), a, p), h * tB, a, p)
    # step 7 计算KB
    entlenA, entlenB = len(IDA) * 4, len(IDB) * 4
    ENTLA, ENTLB = hex(entlenA)[2:].zfill(4), hex(entlenB)[2:].zfill(4)
    ZA = sha256(bytearray.fromhex(ENTLA + IDA + hex(a)[2:].zfill(Par // 4) + hex(b)[2:].zfill(Par // 4)
                                  + hex(G[0])[2:].zfill(Par // 4) + hex(G[1])[2:].zfill(Par // 4)
                                  + hex(PA[0])[2:].zfill(Par // 4) + hex(PA[1])[2:].zfill(Par // 4))).hexdigest()
    ZB = sha256(bytearray.fromhex(ENTLB + IDB + hex(a)[2:].zfill(Par // 4) + hex(b)[2:].zfill(Par // 4)
                                  + hex(G[0])[2:].zfill(Par // 4) + hex(G[1])[2:].zfill(Par // 4)
                                  + hex(PB[0])[2:].zfill(Par // 4) + hex(PB[1])[2:].zfill(Par // 4))).hexdigest()
    KB = KDF(bin(V[0])[2:].zfill(Par) + bin(V[1])[2:].zfill(Par) + hex_to_bin(ZA) + hex_to_bin(ZB), klen)
    # step 8 计算SB
    _ = sha256(bytearray.fromhex(hex(V[0])[2:].zfill(Par // 4) + ZA + ZB
                                 + hex(RA[0])[2:].zfill(Par // 4) + hex(RA[1])[2:].zfill(Par // 4)
                                 + hex(RB[0])[2:].zfill(Par // 4) + hex(RB[1])[2:].zfill(Par // 4))).hexdigest()
    SB = sha256(bytearray.fromhex('02' + hex(V[1])[2:].zfill(Par // 4) + _)).hexdigest()
    # step 9 将RB SB发送给A
    # step 10 计算SA
    S2 = sha256(bytearray.fromhex('03' + hex(V[1])[2:].zfill(Par // 4) + _)).hexdigest()
    return int(KB, 2), int(SB, 16), int(S2, 16)


def main():
    id = input().strip()
    p = int(input())
    a, b = int(input()), int(input())
    G = list(map(int, input().split()))
    n = int(input())
    IDA = input().strip()
    IDB = input().strip()
    d = int(input())
    PA = list(map(int, input().split()))
    PB = list(map(int, input().split()))
    r = int(input())
    R = list(map(int, input().split()))
    if id == 'A':
        KA, S1, SA = SM2_DH_A(p, a, b, G, n, IDA, IDB, d, PA, PB, r, R)
        print(KA)
        print(S1, SA)
    else:
        KB, SB, S2 = SM2_DH_B(p, a, b, G, n, IDA, IDB, d, PA, PB, r, R)
        print(KB)
        print(SB, S2)


if __name__ == '__main__':
    # main()
    while True:
        main()
        print('-' * 64)