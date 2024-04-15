from collections import Counter
from functools import cache
from math import inf
from typing import List


# 枚举子集的子集
# lc1681 最小不兼容性
def minimumIncompatibility(nums: List[int], k: int) -> int:
    n = len(nums)
    if n == k:
        return 0
    cnt = n // k
    m = 1 << n
    mx = [0] * m
    mn = [16] * m
    same = [0] * m
    count = [0] * m
    for index, x in enumerate(nums):
        bit = 1 << index
        val = 1 << x
        for j in range(bit):
            if (same[j] == -1) or ((same[j] | val) == same[j]):
                same[bit | j] = -1
            else:
                same[bit | j] = same[j] | val
            mx[bit | j] = mx[j] if mx[j] >= x else x
            mn[bit | j] = mn[j] if mn[j] <= x else x
            count[bit | j] = count[j] + 1

    @cache
    def dfs(i: int, mask: int) -> int:
        if i == 0:
            return -1 if same[j] == -1 else mx[j] - mn[j]
        s = mask
        res = inf
        while s:
            if count[s] == cnt and (same[s] != -1):
                pre = dfs(i - 1, j ^ s)
                if pre != -1:
                    cur = mx[s] - mn[s] + pre
                    res = res if res <= cur else cur
            s = (s - 1) & j
        return -1 if res == inf else res

    return dfs(k - 1, m - 1)


# lc1494 并行课程II
def minNumberOfSemesters(n: int, relations: List[List[int]], k: int) -> int:
    total = 1 << n
    m = len(relations)
    if m == 0:
        return n // k if n % k == 0 else n // k + 1
    relation = [0] * (n + 1)

    for i in range(m):
        cur = relations[i][1]
        fa = relations[i][0]
        relation[cur] |= (1 << (fa - 1))
    union_relation = [0] * total
    for i in range(n):
        bit = 1 << i
        for j in range(bit):
            union_relation[bit | j] = union_relation[j] | relation[i + 1]

    @cache
    def dfs(mask: int) -> int:
        if mask == 0:
            return 0
        if mask.bit_count() <= k and (union_relation[mask] & mask) == 0:
            return 1
        s = mask
        res = inf
        while s:
            if s.bit_count() <= k and (union_relation[s] & mask) == 0:
                res = min(res, dfs(mask ^ s))
            s = (s - 1) & mask
        return res + 1

    return dfs(total - 1)


# lc1994 好子集的数目
def numberOfGoodSubsets(nums: List[int]) -> int:
    MOD = 10 ** 9 + 7
    PRIMES = 2, 3, 5, 7, 11, 13, 17, 19, 23, 29
    counter = Counter(nums)
    bit_val = []
    cnt = []
    for i, v in counter.items():
        if i == 1:
            cnt.append(pow(2, v, MOD) - 1)
            bit_val.append(1)
        else:
            cur = 0
            for p in PRIMES:
                if i % p == 0:
                    if i % (p * p) == 0:
                        cur = -1
                        break
                    cur |= 1 << p
            if cur == -1:
                continue
            cnt.append(v)
            bit_val.append(cur)
    n = len(cnt)
    if n == 0:
        return 0
    m = 1 << n
    fx = [0] * m
    fx[0] = 1
    bit_sum = [0] * m
    sub = 0
    for i in range(n):
        bit = 1 << i
        for j in range(bit):
            if bit_sum[j] & bit_val[i] == 0:
                if bit_sum[j] | bit_val[i] == 1:
                    sub = (fx[j] * cnt[i]) % MOD
                fx[bit | j] = (fx[j] * cnt[i]) % MOD
            bit_sum[bit | j] = bit_sum[j] | bit_val[i]
    return (sum(fx) - 1 - sub) % MOD
