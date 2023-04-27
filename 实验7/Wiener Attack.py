import gmpy2

"""
wiener's attack 原理 资料来源：http://t.csdn.cn/VfG1t
e/N = k/d
代码参考：http://t.csdn.cn/pXtsT
"""


def continuedFra(x, y):
    cf = []
    # x = x//y * y + x%y => x/y = x//y + x%y/y
    # m = x / y
    # while True:
    #     cf.append(int(m)) => int(m) 为x//y
    #     m = m - int(m) => 为x%y/y
    #     if m == 0:
    #         break
    #     m = 1 / m => 1/m 为y/x%y
    while y:
        cf.append(x // y)
        x, y = y, x % y
    return cf


def gradualFra(cf):
    # 自己对代码的理解：
    # a0+1/(a1 + 1/(a2 + 1/a3 ) )
    # 从最底层1/a3 => a3/(a2a3+1)
    # => (a2a3+1)/(a1a2a3+a1+a3)
    x = 0
    y = 1
    for a in cf[::-1]:
        x, y = y, a * y + x
        # 当到a0时，xy又进行了一次调换
        # 所以如果return了x,y则k/d也要调换
        # 当然也可以return y,x
    return x, y


def getGradualFra(cf):  # 计算列表所有的渐近分数
    gf = []
    for i in range(1, len(cf) + 1):
        gf.append(gradualFra(cf[:i]))
    return gf


def wienerAttack(e, n):
    cf = continuedFra(e, n)
    gf = getGradualFra(cf)
    for d, k in gf:
        if k == 0:
            continue
        if (e * d - 1) % k != 0:
            continue
        phi = n - (e * d - 1) // k + 1
        delta = gmpy2.isqrt(phi ** 2 - 4 * n)
        p = (-phi + delta) // 2
        q = (-phi - delta) // 2
        if p * q == n:
            return abs(p), abs(q), abs(d)


def main():
    e = int(input())
    N = int(input())
    p, q, d = wienerAttack(e, N)
    print(min(p, q))
    print(max(p, q))
    print(d)


if __name__ == '__main__':
    main()