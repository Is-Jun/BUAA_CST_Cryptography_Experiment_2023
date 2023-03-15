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


s = input()
a, b = int(s.split(' ')[0]), int(s.split(' ')[1])
x, y, gcd = extend_gcd(a, b)

x = x % abs(b//gcd)
y = (gcd - a * x) // b

print(x, y, gcd)