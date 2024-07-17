import math
from collections import defaultdict, Counter
from functools import cache
from math import gcd, sqrt
from typing import List


# lc1819 序列中不同最大公约数的数目
def countDifferentSubsequenceGCDs(nums: List[int]) -> int:
    st = set(nums)
    ans = 0
    mx = max(nums)
    for i in range(1, mx + 1):
        gc = 0
        for j in range(i, mx + 1, i):
            if j in st:
                if gc:
                    gc = gcd(gc, j)
                else:
                    gc = j
        ans += gc == i
    return ans


@cache
def factorize(num: int) -> Counter:
    if num == 1:
        return []
    ans = set()
    for i in range(2, int(sqrt(num)) + 2):
        if num % i == 0:
            num //= i
            ans.add(i)
            ans = ans.union(factorize(num))
            return ans
    ans.add(num)
    return ans


# LCP14 切分数组
def splitArray(nums: List[int]) -> int:
    n = len(nums)
    dp = [n] * (n + 1)
    dp[0] = 0
    dt = defaultdict()
    for i, x in enumerate(nums):
        fac = factorize(x)
        dp[i + 1] = dp[i] + 1
        for f in fac:
            if f not in dt.keys():
                dt[f] = dp[i]
            else:
                dt[f] = dt[f] if dt[f] < dp[i] else dp[i]

        for f in fac:
            dp[i + 1] = dp[i + 1] if dp[i + 1] < dt[f] + 1 else dt[f] + 1

    return dp[n]


def cf1972D():
    n, m = map(int, input().split())
    # a = k1 * c, b = k2 * c,k1, k2 互质, k2 * c = K * (k1 + k2) => (k1 + k2) | c
    # k1 < a / k1, k2 < b / k2
    k_a = math.isqrt(n) + 1
    k_b = math.isqrt(m) + 1
    f = [[0] * k_b for _ in range(k_a)]
    for i in range(2, min(k_a, k_b)):
        for a in range(i, k_a, i):
            for b in range(i, k_b, i):
                f[a][b] = 1

    ans = 0
    for a in range(1, k_a):
        for b in range(1, k_b):
            if f[a][b] == 0:
                mx = min((n // a, m // b))
                ans += mx // (a + b)
    print(ans)
    return
