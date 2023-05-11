# 客户端代码
import socket
from math import ceil, log
from hashlib import sha256
from random import randint
from time import sleep


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


p = 0x8542d69e4c044f18e8b92435bf6ff7de457283915c45517d722edb8b08f1dfc3
a, b = 0x787968b4fa32c3fd2417842e73bbfeff2f3c848b6831d7e0ec65228b3937e498, 0x63e4c6d3b23b0c849cf84241484bfe48f61d59a5b16ba06e6e12d1da27c5249a
G = [0x421debd61b62eab6746434ebc3cc315e32220b3badd50bdc4c4e6c147fedd43d, 0x680512bcbb42c07d47349d2153b70c4e5d7fdfcbfa36ea1a85841b9e46e09a2]
n = 0x8542d69e4c044f18e8b92435bf6ff7dd297720630485628d5ae74ee7c32e79b7
h = 1  # 余因子
klen = 128
Par = 256  # 安全参数
w = ceil(ceil(log(n, 2)) / 2) - 1

dB = 0x5e35d7d3f3c54dbac72e61819e730b019a84208ca3a35e4c2e353dfccb2a3b53
PA = [0x3099093bf3c137d8fcbbcdf4a2ae50f3b0f216c3122d79425fe03a45dbfe1655, 0x3df79e8dac1cf0ecbaa2f2b49d51a4b387f2efaf482339086a27a8e05baed98b]
PB = [0x245493d446c38d8cc0f118374690e7df633a8a4bfb3329b5ece604b2b4f37f43, 0x53c0869f4b9e17773de68fec45e14904e0dea45bf6cecf9918c85ea047c60a4c]
IDA = '414c494345313233405941484f4f2e434f4d'
IDB = '42494c4c343536405941484f4f2e434f4d'
entlenA, entlenB = len(IDA) * 4, len(IDB) * 4
ENTLA, ENTLB = hex(entlenA)[2:].zfill(4), hex(entlenB)[2:].zfill(4)
ZA = sha256(bytearray.fromhex(ENTLA + IDA + hex(a)[2:].zfill(Par // 4) + hex(b)[2:].zfill(Par // 4)
                              + hex(G[0])[2:].zfill(Par // 4) + hex(G[1])[2:].zfill(Par // 4)
                              + hex(PA[0])[2:].zfill(Par // 4) + hex(PA[1])[2:].zfill(Par // 4))).hexdigest()
ZB = sha256(bytearray.fromhex(ENTLB + IDB + hex(a)[2:].zfill(Par // 4) + hex(b)[2:].zfill(Par // 4)
                              + hex(G[0])[2:].zfill(Par // 4) + hex(G[1])[2:].zfill(Par // 4)
                              + hex(PB[0])[2:].zfill(Par // 4) + hex(PB[1])[2:].zfill(Par // 4))).hexdigest()


def SM2_B(client_sock):
    print('Prepare for SM2 key negotiation……')
    confirm_A, confirm_B = 0, 0
    selectB = input('Please choose whether to proceed with SM2 key negotiation:[Y/N]:')
    while True:
        if selectB == 'Y' or selectB == 'y':
            confirm_B = 1
            break
        elif selectB == 'N' or selectB == 'n':
            confirm_B = 0
            break
        else:
            input('Please input Y(y) or N(n)')
    client_sock.sendall(str(confirm_B).encode())
    confirm_A = int(client_sock.recv(1024))
    if confirm_A and confirm_B:
        print('Confirmed successfully! SM2 key negotiation starts……')
    elif not confirm_A and confirm_B:
        print('A cancels the negotiation and the negotiation stops.')
        return False
    elif confirm_A and not confirm_B:
        print('B cancels the negotiation and the negotiation stops.')
        return False
    else:
        print('Both parties cancel the negotiation and the negotiation is suspended.')
        return False
    print('Please be patient and wait:')
    for i in range(10):
        sleep(0.3)
        print('.', end='')
    print()

    # step 1 产生随机数rA
    rB = randint(1, n - 1)
    # step 2 计算RB=rB·G=(x2,y2)
    RB = EC_multiply(G, rB, a, p)
    # step 3 计算x2_如下
    x2_ = (1 << w) + (RB[0] & ((1 << w) - 1))
    # step 4 计算tB
    tB = (dB + x2_ * rB) % n
    RA = list(map(int, client_sock.recv(1024).split()))
    judgeB = 1
    if RA[1] ** 2 % p != (RA[0] ** 3 + a * RA[0] + b) % p:
        judgeB = 0
    client_sock.sendall(str(judgeB).encode())
    if not judgeB:
        print('RA does not satisfy the curve equation. B failed to negotiate!')
        return False
    # step 5 计算x1_如下
    x1_ = (1 << w) + (RA[0] & ((1 << w) - 1))
    # step 6 计算椭圆曲线点
    V = EC_multiply(EC_add(PA, EC_multiply(RA, x1_, a, p), a, p), h * tB, a, p)
    if V == [0, 0]:
        judgeB = 0
    client_sock.sendall(str(judgeB).encode())
    if not judgeB:
        print('V = O. B failed to negotiate!')
        return False
    # step 7 计算KB
    KB = KDF(bin(V[0])[2:].zfill(Par) + bin(V[1])[2:].zfill(Par) + hex_to_bin(ZA) + hex_to_bin(ZB), klen)
    # step 8 计算SB
    _ = sha256(bytearray.fromhex(hex(V[0])[2:].zfill(Par // 4) + ZA + ZB
                                 + hex(RA[0])[2:].zfill(Par // 4) + hex(RA[1])[2:].zfill(Par // 4)
                                 + hex(RB[0])[2:].zfill(Par // 4) + hex(RB[1])[2:].zfill(Par // 4))).hexdigest()
    SB = sha256(bytearray.fromhex('02' + hex(V[1])[2:].zfill(Par // 4) + _)).hexdigest()
    # step 9 将RB SB发送给A
    client_sock.sendall((str(RB[0]) + ' ' + str(RB[1])).encode())
    client_sock.sendall(SB.encode())
    judgeA = int(client_sock.recv(1024))
    if not judgeA:
        print('RB does not satisfy the curve equation. A failed to negotiate!')
        return False
    judgeA = int(client_sock.recv(1024))
    if not judgeA:
        print('U = O. A failed to negotiate!')
        return False
    judgeA = int(client_sock.recv(1024))
    if not judgeA:
        print('S1 != SB. A failed to negotiate!')
        return False
    # step 10 计算SA
    S2 = int(sha256(bytearray.fromhex('03' + hex(V[1])[2:].zfill(Par // 4) + _)).hexdigest(), 16)
    SA = int(client_sock.recv(1024), 16)
    if S2 != SA:
        judgeB = 0
    client_sock.send(str(judgeB).encode())
    if not judgeB:
        print('S2 != SA. B failed to negotiate!')
        return False
    if judgeA and judgeB:
        print('Key negotiation succeeded!')
    return True


def main():
    server_host = '127.0.0.1'
    server_port = 8888

    # 创建套接字并连接到服务器
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((server_host, server_port))

    SM2_B(client_sock)

    # 关闭套接字
    client_sock.close()


if __name__ == '__main__':
    main()
