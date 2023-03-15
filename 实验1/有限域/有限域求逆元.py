poly = 0x11b


def multiply(a, b):
    ans = 0
    while b > 0:
        if b & 0x01 == 0x01:
            ans ^= a
        a <<= 1
        if a & 0x100 == 0x100:
            a ^= poly
        a &= 0xff
        b >>= 1
    return ans


def divide(a, b):
    ans = 0
    while len(bin(a)) >= len(bin(b)):  # 商为ans 余数为a
        if a == 0:
            break
        rec = len(bin(a)) - len(bin(b))
        a ^= (b << rec)
        ans ^= (1 << rec)
    return ans, a


def extend_gcd(a, b):
    if b == 0:
        return 1, 0, a
    else:
        _x, _y, gcd = extend_gcd(b, divide(a, b)[1])
        x = _y
        y = _x ^ multiply(_y, divide(a, b)[0])
    return x, y, gcd


def mod_inverse(a, m):
    x, y, gcd = extend_gcd(a, m)
    return x


a = int(input(), base=16)
inv = mod_inverse(a, poly)
print('0' + hex(inv)[2:] if inv < 0x10 else hex(inv)[2:])
