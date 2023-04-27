from gmpy2 import iroot


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


# 求逆元算法
def mod_inverse(a, n):
    if n < 2:
        raise ValueError("modulus must be greater than 1")
    x, y, gcd = extend_gcd(a, n)
    if gcd != 1:
        raise ValueError("No inverse element!")
    else:
        return x % n


def low_index_broadcast_attacks(e, c_n):
    M = [1] * len(c_n)
    for i in range(len(M)):
        for j in range(len(M)):
            if j != i:
                M[i] *= c_n[j][1]
    m_ = 0
    N = M[0] * c_n[0][1]
    for i in range(len(M)):
        m_ += c_n[i][0] * M[i] * mod_inverse(M[i], c_n[i][1])
    m = iroot(m_ % N, e)
    if m[1]:
        print(m[0])


def main():
    n = int(input())
    e = int(input())
    c_n = [[0, 0] for _ in range(n)]
    for i in range(n):
        c_n[i][0] = int(input())
        c_n[i][1] = int(input())
    low_index_broadcast_attacks(e, c_n)


if __name__ == '__main__':
    main()
