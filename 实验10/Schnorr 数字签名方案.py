from hashlib import sha1


def sign(x: int, m: str, k: int):
    r = pow(g, k, p)
    e = int(sha1((m + str(r)).encode('utf-8')).hexdigest(), 16)
    s = (k + x * e) % q
    return e, s


def vrfy(m: str, y: int, e: int, s: int):
    r = pow(g, s, p) * pow(y, e, p) % p
    e_ = int(sha1((m + str(r)).encode('utf-8')).hexdigest(), 16)
    if e_ == e:
        return 'True'
    else:
        return 'False'


def main():
    global p, q, g
    p = int(input())
    q = int(input())
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
        print(vrfy(m, y, s[0], s[1]))


if __name__ == '__main__':
    main()
