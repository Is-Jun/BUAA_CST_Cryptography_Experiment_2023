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


def common_mod_attack(e1, e2, c1, c2, N):
    s1, s2, gcd = extend_gcd(e1, e2)
    if s1 < 0:
        s1 = -s1
        c1 = mod_inverse(c1, N)
    if s2 < 0:
        s2 = -s2
        c2 = mod_inverse(c2, N)
    return (quick_pow(c1, s1, N) * quick_pow(c2, s2, N)) % N


def main():
    e1 = int(input())
    e2 = int(input())
    c1 = int(input())
    c2 = int(input())
    N = int(input())
    print(common_mod_attack(e1, e2, c1, c2, N))


if __name__ == '__main__':
    main()
