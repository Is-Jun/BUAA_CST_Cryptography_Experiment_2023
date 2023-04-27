import random


# 拓展欧几里得算法
def extend_gcd(a, b):
    # 递归版
    # if b == 0:
    #     return 1, 0, a
    # else:
    #     ppx, ppy, gcd = extend_gcd(b, a % b)
    #     x = ppy
    #     y = ppx - int(a // b) * ppy
    #     return x, y, gcd
    # 因为爆栈所以用了非递归版QAQ

    # 非递归版
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


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


# 求逆元算法
def mod_inverse(a, n):
    if n < 2:
        raise ValueError("modulus must be greater than 1")
    x, y, gcd = extend_gcd(a, n)
    if gcd != 1:
        raise ValueError("No inverse element!")
    else:
        return x % n


# 快速抹蜜算法
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


# 素型检验算法
def prime_test_miller_rabin(p):
    if p < 2:
        return False
    if p <= 3:
        return True
    if p & 1 == 0:
        return False
    # p - 1 = 2**k * q
    k, q = 0, p - 1
    while q and q & 1 == 0:
        k += 1
        q >>= 1
    for j in range(20):
        a = random.randint(2, p - 2)
        if gcd(a, p) != 1:
            return False
        b = quick_pow(a, q, p)
        if b == 1 or b == p - 1:  # 不一定是素数
            continue
        for i in range(k):
            b = quick_pow(b, 2, p)
            if b == 1:
                return False
            if b == p - 1:
                if i < k - 1:
                    break
                else:
                    return False
        else:
            return False
    return True


# 秘钥生成函数
def generate_prime(w):
    while True:
        # 产生一个奇数（）
        num = (random.getrandbits(w) | (1 << (w - 1))) | 1
        if prime_test_miller_rabin(num):
            return num


def build_key():
    p = generate_prime(1024)
    q = generate_prime(1024)
    n = p * q
    n_ = (p - 1) * (q - 1)
    while True:
        e = random.randint(2, n_ - 1)  # 随机选择一个与_n互质的整数，一般选择65537。
        if gcd(e, n_) == 1:
            break
    d = mod_inverse(e, n_)
    return n, e, d, p, q  # 返回公私钥，公钥（n,e）,私钥（n,d） 由下题私钥需同时返回 p, q


# 加密函数
def encrypt(m, n, e):
    c = quick_pow(m, e, n)
    return c


# 解密函数（中国剩余定理加速）
def decrypt(c, n, d, p, q):
    # 非加速
    # c = quick_pow(c, d, n)
    # 使用中国剩余定理加速
    m1 = quick_pow((c % p), (d % (p - 1)), p)
    m2 = quick_pow((c % q), (d % (q - 1)), q)
    m = (m1 * mod_inverse(q, p) * q + m2 * mod_inverse(p, q) * p) % n
    return m


def RSA(m, p, q, e, mode):
    if mode == 1:
        return encrypt(m, p * q, e)
    else:
        d = mod_inverse(e, (p - 1)*(q - 1))
        return decrypt(m, p * q, d, p, q)


def main():
    p = int(input())
    q = int(input())
    e = int(input())
    m = int(input())
    mode = int(input())
    print(RSA(m, p, q, e, mode))


if __name__ == '__main__':
    # main()
    while True:
        main()
        print('-' * 64)


