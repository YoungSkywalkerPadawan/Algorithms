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


# LCP53 守护太空城
def defendSpaceCity(time: List[int], position: List[int]) -> int:
    n, m = max(position), 1 << max(time)
    rain = [0] * (n + 1)
    for t, p in zip(time, position):
        rain[p] |= 1 << (t - 1)

    union = [0] * m
    single = [0] * m
    for i in range(1, m):
        lb = i & -i
        j = i ^ lb
        lb2 = j & -j
        union[i] = union[j] + (1 if lb == (lb2 >> 1) else 3)  # lb == (lb2 >> 1) 表示两个时间点相邻
        single[i] = single[j] + (1 if lb == (lb2 >> 1) else 2)  # 递推

    @cache  # 缓存装饰器，避免重复计算 dfs 的结果
    def dfs(x: int, y: int) -> int:
        if x < 0:
            return 0
        ans = inf
        pre = mask = (m - 1) ^ y
        while True:  # 枚举 j 的补集 mask 中的子集 pre
            cost = dfs(x - 1, pre) + union[y] + single[(mask ^ pre) & rain[x]]
            ans = min(ans, cost)
            if pre == 0:
                break
            pre = (pre - 1) & mask
        return ans

    return dfs(n, 0)


# LCP04 覆盖
def domino(n: int, m: int, broken: List[List[int]]) -> int:
    a = [(1 << m) - 1] * n
    for x, y in broken:
        a[x] -= (1 << y)

    @cache  # 缓存装饰器，避免重复计算 dfs 的结果
    def dp(i: int, j: int) -> int:
        if i < 0:
            return 0

        def dfs(cur_i, s):
            if cur_i == m:
                return dp(i - 1, s)
            res = dfs(cur_i + 1, s)  # 放弃当前这个格子
            if cur_i <= m - 2 and (1 << cur_i) & s > 0 and (1 << (cur_i + 1)) & s > 0:  # 横放一块骨牌
                res = max(res, 1 + dfs(cur_i + 2, s ^ (1 << cur_i) ^ (1 << (cur_i + 1))))
            if (1 << cur_i) & s > 0 and (1 << cur_i) & j > 0:  # 竖放一块骨牌，前提是上一行这一列有空位
                res = max(res, 1 + dfs(cur_i + 1, s ^ (1 << cur_i)))
            return res

        return dfs(0, a[i])

    return dp(n - 1, 0)
