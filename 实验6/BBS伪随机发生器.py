def BBS(len, p, q, s):
    result = ''
    n = p * q
    X = s * s % n
    for i in range(len):
        X = X ** 2 % n
        result = str(X & 1) + result
    result = int(result, base=2)
    return result


def main():
    len = int(input())
    p = int(input())
    q = int(input())
    s = int(input())
    print(BBS(len, p, q, s))


if __name__ == '__main__':
    main()
    # while True:
    #     main()
    #     print('-' * 30)