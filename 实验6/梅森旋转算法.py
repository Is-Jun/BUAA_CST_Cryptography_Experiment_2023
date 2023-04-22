w, n, m, r = 32, 624, 397, 31
a = 0x9908b0df
f = 0x6c078965
u, d = 11, 0xffffffff
s, b = 7, 0x9d2c5680
t, c = 15, 0xefc60000
l = 18
MT = [0] * n
index = n + 1
lower_mask = (1 << r) - 1
upper_mask = (~lower_mask) & d


def seed_mt(seed):
    global index, MT
    index = n
    MT[0] = seed
    for i in range(1, n):
        MT[i] = (f * (MT[i - 1] ^ (MT[i - 1] >> (w - 2))) + i) & d


def extract_number():
    global index, MT
    if index >= n:
        if index > n:
            raise 'Generator was never seeded'
        twist()
    y = MT[index]
    y = y ^ ((y >> u) & d)
    y = y ^ ((y << s) & b)
    y = y ^ ((y << t) & c)
    y = y ^ (y >> l)
    index += 1
    return y & d


def twist():
    global index, MT
    for i in range(n):
        X = ((MT[i] & upper_mask) + (MT[(i + 1) % n] & lower_mask)) & d
        XA = X >> 1
        if X & 1 != 0:
            XA = XA ^ a
        MT[i] = MT[(i + m) % n] ^ XA
    index = 0


def MT19937(seed, T):
    seed_mt(seed)
    for i in range(T):
        print(extract_number())


def main():
    seed = int(input())
    T = 20
    MT19937(seed, T)


if __name__ == '__main__':
    main()
