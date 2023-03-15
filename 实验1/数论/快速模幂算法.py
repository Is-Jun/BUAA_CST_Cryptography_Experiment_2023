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


s = input()

print(quick_pow(int(s.split(' ')[0]), int(s.split(' ')[1]), int(s.split(' ')[2])))