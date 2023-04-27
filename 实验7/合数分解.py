import random


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


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


def get_p_q(e, d, N):
    while True:
        k = e * d - 1
        g = random.randint(0, N)
        while k % 2 == 0:
            k = k // 2
            temp = quick_pow(g, k, N) - 1
            if gcd(temp, N) > 1 and temp != 0:
                return gcd(temp, N)


def main():
    e = int(input())
    d = int(input())
    N = int(input())
    p = get_p_q(e, d, N)
    q = N // p
    if p > q:
        p, q = q, p
    print(p)
    print(q)


if __name__ == '__main__':
    main()