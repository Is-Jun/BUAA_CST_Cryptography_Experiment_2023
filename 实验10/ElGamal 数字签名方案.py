from hashlib import sha256
from gmpy2 import invert


def sign(x: int, m: str, k: int):
    hash_m = int(sha256(m.encode('utf-8')).hexdigest(), 16)
    s1 = pow(g, k, p)
    s2 = invert(k, p - 1) * (hash_m - x * s1) % (p - 1)
    return s1, s2


def vrfy(m: str, y: int, s: list):
    hash_m = int(sha256(m.encode('utf-8')).hexdigest(), 16)
    v1 = pow(g, hash_m, p)
    v2 = pow(y, s[0], p) * pow(s[0], s[1], p) % p
    if v1 == v2:
        return 'True'
    else:
        return 'False'


def main():
    global p, g
    p = int(input())
    g = int(input())
    m = input().strip()
    mode = input().strip()
    if mode == 'Sign':
        x = int(input())
        k = int(input())
        s = sign(x, m, k)
        print(s[0], s[1], end='\n')
    else:
        y = int(input())
        s = list(map(int, input().split()))
        print(vrfy(m, y, s))


if __name__ == '__main__':
    main()
