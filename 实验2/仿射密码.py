def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def extend_gcd(a, b):
    if b == 0:
        return 1, 0, a
    else:
        _x, _y, gcd = extend_gcd(b, a % b)
        x = _y
        y = _x - int(a // b) * _y
        if gcd < 0:
            gcd = -gcd
            x = -x
            y = -y
    return x, y, gcd


def mod_inverse(a, n):
    x, y, gcd = extend_gcd(a, n)
    return x % n


def affine_cipher(k, b, s, way):
    if gcd(k, 26) != 1:
        return 'invalid key'
    if way == 1:
        cipher = ''
        for i in s:
            cipher += chr((k * (ord(i) - ord('a')) + b) % 26 + ord('a'))
        return cipher
    else:
        plaintext = ''
        k_ = mod_inverse(k, 26)
        for i in s:
            plaintext += chr((k_ * (ord(i) - ord('a') - b)) % 26 + ord('a'))
        return plaintext


k, b = input().split(' ')
k, b = int(k), int(b)
s = input().strip()
way = int(input())

print(affine_cipher(k, b, s, way))
