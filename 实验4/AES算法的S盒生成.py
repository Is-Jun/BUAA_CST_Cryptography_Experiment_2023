# step 1
# 按逐行上升排列的方式初始化S盒，第x行y列的字节值为xy
Sbox = []
for i in range(16):
    _ = [0] * 16
    for j in range(16):
        _[j] = i * 16 + j
    Sbox.append(_)

for i in range(16):
    for j in range(16):
        print('0x' + hex(Sbox[i][j])[2:].zfill(2), end=' ')
    print()
# step 2
# 将每个字节映射为有限域GF(2^8)上的乘法逆元（注意 0x00 映射到自己）
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


for i in range(16):
    for j in range(16):
        Sbox[i][j] = mod_inverse(Sbox[i][j], poly)

for i in range(16):
    for j in range(16):
        print('0x' + hex(Sbox[i][j])[2:].zfill(2), end=' ')
    print()

# step 3
# 将每个字节表示为b=(b7,b6……,b0)，每个比特位做变化
c = '01100011'[::-1]
for i in range(16):
    for j in range(16):
        b = bin(Sbox[i][j])[2:].zfill(8)[::-1]
        result = ''
        for k in range(8):
            result += str(int(b[k]) ^ int(b[(k+4) % 8]) ^ int(b[(k+5) % 8]) ^ int(b[(k+6) % 8]) ^ int(b[(k+7) % 8]) ^ int(c[k]))
        Sbox[i][j] = int(result[::-1], base=2)

for i in range(16):
    for j in range(16):
        print('0x' + hex(Sbox[i][j])[2:].zfill(2), end=' ')
    print()

# step 4
# 求逆S盒
for i in range(16):
    for j in range(16):
        Sbox[i][j] = i * 16 + j

c = '000000101'[::-1]
for i in range(16):
    for j in range(16):
        b = bin(Sbox[i][j])[2:].zfill(8)[::-1]
        result = ''
        for k in range(8):
            result += str(int(b[(k+2) % 8]) ^ int(b[(k+5) % 8]) ^ int(b[(k+7) % 8]) ^ int(c[k]))
        Sbox[i][j] = int(result[::-1], base=2)

for i in range(16):
    for j in range(16):
        Sbox[i][j] = mod_inverse(Sbox[i][j], poly)

for i in range(16):
    for j in range(16):
        print('0x' + hex(Sbox[i][j])[2:].zfill(2), end=' ')
    print()

