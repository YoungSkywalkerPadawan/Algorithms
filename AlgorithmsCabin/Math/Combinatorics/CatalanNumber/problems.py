# 卡特兰数是一种经典的组合数，经常出现在各种计算中，其前几项为 : 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796, 58786

from collections import deque

from AlgorithmsCabin.Math.Util.Factorial import Factorial
from AlgorithmsCabin.Math.Util.utils import mint

fac = Factorial(4 * 10 ** 5, 998244353)


def cf2056E():
    n, m = mint()
    mod = 998244353
    # 卡特兰数
    f = [0] * (n + 1)
    for i in range(n):
        f[i + 1] = fac.combi(2 * i, i) - fac.combi(2 * i, i - 1)

    res = []
    mx = -1
    for _ in range(m):
        l, r = mint()
        l -= 1
        cur = r - l
        if cur > mx:
            mx = cur
        res.append((l, r))

    if mx < n:
        res.append((0, n))
        m += 1

    res.sort(key=lambda p: (p[0], -p[1]))
    dq = deque()
    s = [0] * m
    for i in range(m):
        l, r = res[i]
        while dq and res[dq[-1]][1] <= l:
            dq.pop()

        if dq:
            s[dq[-1]] += r - l - 1
        dq.append(i)

    ans = 1
    for i in range(m):
        l, r = res[i]
        ans *= f[r - l - s[i]]
        ans %= mod
    print(ans)
    return
