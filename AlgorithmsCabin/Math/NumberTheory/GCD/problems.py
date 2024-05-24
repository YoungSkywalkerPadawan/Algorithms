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
