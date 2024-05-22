from collections import Counter
from functools import cache
from math import inf
from typing import List


# lc1815 得到新鲜甜甜圈的最多组数
# 状态压缩，相同余数的一起考虑
def maxHappyGroups(batchSize: int, groups: List[int]) -> int:

    @cache
    def dfs(x: int, y: int) -> int:
        if x == 0:
            return 0
        pre = 0 if y > 0 else 1
        res = 0
        for j in range(1, batchSize):
            if (x >> (j * 5)) & 31:
                cur = dfs(x - (1 << (j * 5)), (y + j) % batchSize)
                if cur > res:
                    res = cur
        return res + pre

    f = 0
    ans = 0
    for v in groups:
        if v % batchSize == 0:
            ans += 1
        else:
            i = v % batchSize
            f += 1 << (i * 5)
    ans += dfs(f, 0)
    return ans


# lc691 贴纸拼词
# 反复使用某个对象
def minStickers(stickers: List[str], target: str) -> int:

    n = len(target)
    m = len(stickers)
    t = Counter(target)
    s = []
    for stick in stickers:
        c = Counter()
        for w in stick:
            if t[w] > 0:
                c[w] += 1
        s.append(c)

    @cache
    def dfs(x: int) -> int:
        if x == 0:
            return 0
        res = inf
        idx = [i for i in range(n) if (1 << i) & x]
        for i in range(m):
            cur = x
            cnt = s[i].copy()
            for j in idx:
                if cnt[target[j]]:
                    cnt[target[j]] -= 1
                    cur ^= (1 << j)
            if cur < x:
                res1 = 1 + dfs(cur)
                if res1 < res:
                    res = res1
        return res

    ans = dfs((1 << n) - 1)
    return ans if ans < inf else -1


# lc1434 每个人戴不同帽子的方案数
# 对较小数量的一方进行状态压缩
def numberWays(hats: List[List[int]]) -> int:
    n = len(hats)
    g = [[] for _ in range(40)]
    for i, row in enumerate(hats):
        for v in row:
            v -= 1
            g[v].append(i)
    MOD = 10 ** 9 + 7

    @cache
    def dfs(x: int, y: int) -> int:
        if y == 0:
            return 1
        if x == 40:
            return 0
        res = dfs(x + 1, y)
        for j in g[x]:
            if (1 << j) & y > 0:
                res += dfs(x + 1, y ^ (1 << j))
        return res % MOD

    ans = dfs(0, (1 << n) - 1)
    dfs.cache_clear()
    return ans % MOD
