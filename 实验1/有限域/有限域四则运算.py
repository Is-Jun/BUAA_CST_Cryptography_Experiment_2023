def calculate(x, y, z):
    poly = 0x11b
    a = int(x, base=16)
    b = int(z, base=16)
    ans = 0
    result = ''
    if y == '+' or y == '-':
        ans = a ^ b
        result = '0' + hex(ans)[2:] if ans < 0x10 else hex(ans)[2:]
    elif y == '*':
        while b > 0:
            if b & 0x01 == 0x01:
                ans ^= a
            a <<= 1
            if a & 0x100 == 0x100:
                a ^= poly
            a &= 0xff
            b >>= 1
        result = '0' + hex(ans)[2:] if ans < 0x10 else hex(ans)[2:]
    else:
        while len(bin(a)) >= len(bin(b)):
            if a == 0:
                break
            rec = len(bin(a)) - len(bin(b))
            a ^= (b << rec)
            ans ^= (1 << rec)
        x = ('0' + hex(a)[2:] if a < 0x10 else hex(a)[2:])
        result = ('0' + hex(ans)[2:] if ans < 0x10 else hex(ans)[2:]) + ' ' + x
    return result


s = input()
x, y, z = s.split(' ')
print(calculate(x, y, z))
