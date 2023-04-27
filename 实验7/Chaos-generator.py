from AITMCLAB.libnum import invmod, n2s
from gmpy2 import next_prime
import time


time_start = time.time()
p = 74318463376311964657848870236469351222861371046000989980725143814597652972079
g = 10135979321704650132001133858909900216529170765388975908180263641843583056994
N = 46560744052031492000075598084262814175984839629218579003339825251165084535288738001196294968344403225296587992393409186512832442084313772062189640462381680977493272839744503195012137744652370256066011590369737294828406013950810998314546935103160880000499234316605414326064476117367727072344004644766745175963
c = 23334367507777982721463578689282517343702422017568936413397591619899938216343800551132594869485665306596562901129144338015710969994575939792628945297846703002122172051500112438041566171992504143239954624689779597268840813422509867439815100802585538453946245512563984478922752113443379737653491922857109660034
e = 65537


def chaos_maker(p, G, x):
    res = 0
    for i in range(256):
        x = G[x % 28361]
        if x < (p-1) // 2:
            res -= (1 << i) - 1
        elif x > (p-1) // 2:
            res += (1 << i) + 1
        else:
            res ^= (1 << i + 1)
    return res if res > 0 else -res


# 求g的生成群
G = [0] * 28361
G[0] = 1
for i in range(1, 28361):
    G[i] = (g * G[i-1]) % p

# 求uv
uv = [0] * 28361
for x in range(0, 28361):
    uv[x] = chaos_maker(p, G, x)
uv.sort()

finish = False
for i in range(0, 28361):
    left = i + 1
    right = 28360
    mid = 0
    while left <= right:  # 找到一个比较合适的v，此时的v<=正确的v，但不会相差太大
        mid = (left + right) // 2
        if (uv[i] ** 2 + uv[mid] ** 2) * 2 * uv[i] * uv[mid] >= N:
            best = mid
            right = mid - 1
        else:
            left = mid + 1
    for j in range(mid-1, min(mid+30, 28361)):
        u = uv[i] * uv[i] + uv[j] * uv[j]
        v = 2 * uv[i] * uv[j]
        if u * v <= N <= (u + 1000) * (v + 1000):
            p = next_prime(u)
            # v = next_prime(v)
            if N % p == 0:
                q = N // p
                finish = True
                break
    if finish:
        break

# x = (u - 1) * (v - 1)
d = invmod(e, (p - 1) * (q - 1))
flag = pow(c, d, N)
print(n2s(int(flag)))
# print('flag{U_g&5-th3_BA51cs_MY_PaDawan>_<}')
time_end = time.time()
print(f'运行时间：{time_end - time_start}')