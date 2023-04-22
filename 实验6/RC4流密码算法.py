import sys


def KSA(k: str):
    S = [i for i in range(256)]
    l = len(k)
    T = [int(k[(i * 2) % l:(i * 2) % l + 2], base=16) for i in range(256)]
    j = 0
    for i in range(256):
        j = (j + S[i] + T[i]) % 256
        S[i], S[j] = S[j], S[i]
    return S


# def PRGA(S, l):
#     i, j = 0, 0
#     key = [0] * l
#     for k in range(l):
#         i = (i + 1) % 256
#         j = (j + S[i]) % 256
#         S[i], S[j] = S[j], S[i]
#         key[k] = S[(S[i] + S[j]) % 256]
#     return key
#
#
# def main():
#     k = input().strip()[2:]
#     s = input().strip()[2:]
#     S = KSA(k)
#     l = len(s) // 2
#     key = PRGA(S, l)
#     result = '0x'
#     for i in range(l):
#         result += hex(key[i] ^ int(s[2 * i:(i + 1) * 2], base=16))[2:].zfill(2)
#     print(result)


def RC4():
    k = input().strip()[2:]
    S = KSA(k)
    i, j = 0, 0
    result = sys.stdin.read(2)
    while True:
        s = sys.stdin.read(1)
        if s == '\n':
            break
        s += sys.stdin.read(1)
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        key = S[(S[i] + S[j]) % 256]
        result += hex(key ^ int(s, base=16))[2:].zfill(2)
    print(result)


if __name__ == '__main__':
    # main()
    # while True:
    #     main()
    #     print('-' * 32)
    RC4()

"""
PRGA()与main()是将明文全部输入之后再加密
RC4()是边读入边加密，其中while中，s可以read(2)但判断条件需要修改
"""