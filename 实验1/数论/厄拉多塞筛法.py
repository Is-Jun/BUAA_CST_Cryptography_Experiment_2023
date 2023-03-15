def Eeatosthese(N):
    isp = [True] * (N + 1)
    pr = []
    for i in range(2, N + 1):
        if isp[i]:
            pr.append(i)
        j = 0
        while j < len(pr) and pr[j] * i <= N:
            isp[i * pr[j]] = False
            if i % pr[j] == 0:
                break
            j += 1
    return pr


N = int(input())
pr = Eeatosthese(N)
print(*pr)