def multiply(a, b):
    poly = 0x11b
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


def quick_pow(a, b):
    n_binary = []
    while b != 0:
        n_binary.append(b % 2)
        b = b // 2
    n_binary[:] = n_binary[::-1]
    c = 1
    for i in n_binary:
        c = multiply(c, c)
        if i:
            c = multiply(c, a)
    return c


a, b = input().split(' ')
a, b = int(a, base=16), int(b)

print(hex(quick_pow(a, b))[2:])