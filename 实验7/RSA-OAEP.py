from hashlib import sha1


def MGF(mgfSeed, maskLen):
    """
    参数与算法说明
    mgfSeed 输是入的随机变量
    maskLen 是输出的掩码长度
    1.MGF内部需要调用一个哈希函数，默认为SHA1，其输出哈希长度为hLen=20字节
    2.MGF内部有一个计数器counter，其大小为0~maskLen/hLen
    3.将counter转换成4字节的字符串C，附加到mgfSeed的末尾并计算哈希
    4.递增计数器，计算哈希输出，并链接前一个哈希输出的末尾，直到输出位长达到要求（不少于maskLen）然后截取前maskLen字节返回
    """
    if len(mgfSeed) // 2 > 2 ** 61 - 4:
        return -1
    counter = 0
    hLen = 20
    restLen = maskLen
    mask = ''
    while restLen > 0:
        C = hex(counter)[2:].zfill(8)
        mask += sha1(bytearray.fromhex(mgfSeed + C)).hexdigest()
        counter += 1
        restLen -= hLen
    return mask[:maskLen * 2]


def XOR(x, y):
    return hex(int(x, 16) ^ int(y, 16))[2:].zfill(max(len(x), len(y)))


def RSA_OAEP_encrypt(k, seed, L, m):
    """
    参数说明
    EM           最后要要输出的结果 k字节长度 由00 maskedSeed maskedDB组成
    maskedSeed   hLen字节长度，固定为20字节长度 经过 XOR(MGF(maskedDB), seed)获得
    maskedDB     k-hLen-l字节长度 经过 XOR(MGF(seed), DB)获得
    DB           k-hLen-l字节长度  由lHash PS 01 M组成
    lHash        使用sha1，产生160bit的散列值，20字节长度，由sha1(L).hexdigest()获得
    PS           PS为全0，长度为k-2hLen-2-mLen = k-42-mLen
    M            M为原始密文
    """
    # 检查参数
    hLen = 20
    M = m
    if M == '' or k == 0 or len(L) // 2 >= 2 ** 61 or len(M) // 2 > k - 2 * hLen - 2:
        return -1

    # 计算DB
    lHash = sha1(bytearray.fromhex(L)).hexdigest()
    PS_len = k - 2 * hLen - 2 - len(M) // 2
    PS = '00' * PS_len
    DB = lHash + PS + '01' + M

    # 计算maskedDB
    maskedDB = XOR(MGF(seed, k - hLen - 1), DB)
    if maskedDB == -1:
        return -1

    # 计算maskedSeed
    maskedSeed = XOR(MGF(maskedDB, 20), seed)
    if maskedSeed == -1:
        return -1
    # 计算EM
    EM = '00' + maskedSeed + maskedDB

    return EM


def RSA_OAEP_decrypt(k, L, EM):
    # 检查参数
    hLen = 20
    if len(EM) // 2 != k or k <= 2 * hLen + 2:  # 条件2对应len(m)==0错误情况
        return -1

    # 获取maskedSeed 和 maskedDB
    if EM[0:2] != '00':
        return -1
    maskedSeed, maskedDB = EM[2:2 + 2 * hLen], EM[2 + 2 * hLen:]

    # 计算seed
    _ = MGF(maskedDB, hLen)
    if _ == -1:
        return -1
    seed = XOR(maskedSeed, _)

    # 计算DB
    _ = MGF(seed, k - hLen - 1)
    if _ == -1:
        return -1
    DB = XOR(maskedDB, _)

    # 获取M
    lHash_ = sha1(bytearray.fromhex(L)).hexdigest()
    lHash = DB[:2 * hLen]
    if lHash_ != lHash:
        return -1
    M = ''
    for i in range(hLen * 2, len(DB), 2):
        if DB[i:i+2] == '01':
            M = DB[i+2:]
            break
    if M == '':
        return -1
    return M


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


def quick_pow(b, n, m):
    n_binary = []
    while n != 0:
        n_binary.append(n % 2)
        n = n // 2
    n_binary[:] = n_binary[::-1]
    c = 1
    for i in n_binary:
        c = c * c % m
        if i:
            c = c * b % m
    return c


def encrypt(m, n, e):
    c = quick_pow(m, e, n)
    return c


def decrypt(c, n, d):

    c = quick_pow(c, d, n)
    return c


def RSA(m, N, index, mode):
    if mode == 1:
        return encrypt(m, N, index)
    else:
        return decrypt(m, N, index)


def main():
    mode = int(input())
    k = int(input())
    index = input().strip()
    N = input().strip()
    m = input().strip()
    L = input().strip()
    if mode == 1:
        seed = input().strip()
        em = RSA_OAEP_encrypt(k, seed[2:], L[2:], m[2:])
        if em == -1 or not 0 <= int(em, 16) <= int(N, 16) - 1:
            print('Err')
        else:
            c = RSA(int(em, 16), int(N, 16), int(index, 16), mode)
            print('0x' + hex(c)[2:].zfill(2 * k))
    else:
        em = RSA(int(m, 16), int(N, 16), int(index, 16), mode)
        em = hex(em)[2:].zfill(2 * k)
        m = RSA_OAEP_decrypt(k, L[2:], em)
        if m == -1:
            print('Ree')
        else:
            print(hex(int(m, 16)))


if __name__ == '__main__':
    # main()
    while True:
        main()
        print('-'*64)
