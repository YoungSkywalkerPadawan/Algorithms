# 容斥原理
# ｜A1UA2U···UAm｜ = ∑（1<=i<=m）|Ai| - ∑（1<=i<j<=m）|Ai∩Aj| + ∑（1<=i<j<k<=m）|Ai∩Aj∩Ak|-···+(-1)^m|A1∩A2∩···∩Am|

from math import lcm
from typing import List

from AlgorithmsCabin.Math.NumberTheory.GCD.PrimeTable import PrimeTable
from AlgorithmsCabin.Math.Util.utils import sint, ints

MOD = 10 ** 9 + 7


# lc393周赛T4 单面值组合的第k小金额
def findKthSmallest(coins: List[int], k: int) -> int:
    def check(x: int) -> bool:
        cnt = 0
        for mask in range(1, 1 << len(coins)):
            cur = 1
            for i, v in enumerate(coins):
                if mask >> i & 1:
                    cur = lcm(cur, v)
                    if cur > x:
                        break
            else:
                cnt += x // cur if mask.bit_count() % 2 else -(x // cur)
        return cnt >= k

    l = k - 1
    r = min(coins) * k
    while l < r:
        mid = (l + r) // 2
        if check(mid):
            r = mid - 1
        else:
            l = mid + 1
    return l if check(l) else l + 1


def cf451E():
    def bit_count(self):
        return bin(self).count("1")

    # 快速幂
    def myPow(x, y):
        res = 1
        while y > 0:
            if y % 2:
                res = res * x % MOD
            x = x * x % MOD
            y //= 2
        return res

    # 计算组合数
    def comb(x, y):
        if x < y:
            return 0
        x %= MOD
        p = 1
        for i in range(1, y + 1):
            p = p * (x - i + 1) % MOD
        return p * invF[y] % MOD

    n, s = map(int, input().split())
    a = list(map(int, input().split()))

    # 提前预处理阶乘的逆元
    invF = [1] * 20
    m = 1
    for j in range(1, 20):
        m = m * j % MOD
        invF[j] = myPow(m, MOD - 2)

    ans = 0
    tot = sum(a)
    if tot < s:
        print(0)
        return
    for mask in range(1 << n):
        s2 = s
        for j, v in enumerate(a):
            if (mask >> j) & 1:
                s2 -= v + 1
        c = comb(s2 + n - 1, n - 1) if s2 + n - 1 >= n - 1 else 0
        if bit_count(mask) % 2:
            c = -c
        ans += c
    print(ans % MOD)
    return


def getMu(n):
    mu = [0] * (n + 1)
    flg = [0] * (n + 1)
    p = [0] * (n + 1)
    tot = 0
    mu[1] = 1
    for i in range(2, n + 1):
        if flg[i] == 0:
            tot = tot + 1
            p[tot] = i
            mu[i] = -1
        j = 1
        while j <= tot and i * p[j] <= n:
            flg[i * p[j]] = 1
            if i % p[j] == 0:
                mu[i * p[j]] = 0
                break
            mu[i * p[j]] = - mu[i]
            j = j + 1
    return mu


def cf2037G():
    pt = PrimeTable(10 ** 6)
    n = sint()
    a = ints()
    mod = 998244353
    dp = [0] * (10 ** 6 + 1)
    mu = getMu(10 ** 6)
    for f in pt.get_factors(a[-1]):
        if f > 1:
            dp[f] = 1
    ans = 0
    for i in range(n - 2, -1, -1):
        ans = 0
        for f in pt.get_factors(a[i]):
            if f > 1:
                ans -= dp[f] * mu[f]
                if ans < 0:
                    ans += mod
                elif ans >= mod:
                    ans -= mod

        for f in pt.get_factors(a[i]):
            dp[f] += ans
            if dp[f] >= mod:
                dp[f] -= mod

    print(ans)

    return
