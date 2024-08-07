from functools import cache
from math import inf
from typing import List


# 旅行商问题（TSP） 本质是排列型 相邻相关
# lc943 最短超级串
from AlgorithmsCabin.Math.Util.utils import mint, ints


def shortestSuperstring(words: List[str]) -> str:
    @cache  # 缓存装饰器，避免重复计算 dfs 的结果
    def dfs(i: int, j: int, pre: str) -> str:
        if i < 0:
            return ''
        res = ''
        cur_v = inf
        for x in range(j.bit_length()):
            if (1 << x) & j > 0:
                mn = min(len(pre), len(words[x]))
                index = 0
                for k in range(mn):
                    if pre[len(pre) - k - 1:] == words[x][:k + 1]:
                        index = k + 1
                cur = words[x][index:] + dfs(i - 1, j ^ (1 << x), words[x])
                if len(cur) < cur_v:
                    cur_v = len(cur)
                    res = cur
        return res

    n = len(words)
    s = (1 << n) - 1
    dp = [words[i] + dfs(n - 2, s ^ (1 << i), words[i]) for i in range(n)]
    ans = ''
    v = inf
    for el in dp:
        if len(el) < v:
            v = len(el)
            ans = el
    return ans


# lc847 访问所有节点的最短路径
def shortestPathLength(graph: List[List[int]]) -> int:
    @cache  # 缓存装饰器，避免重复计算 dfs 的结果
    def dfs(j: int, pre: str, v: int) -> int:
        if j == s:
            return v
        if v >= 2 * n:
            return inf
        cur_v = inf
        for x in graph[pre]:
            cur_v = min(cur_v, dfs(j | (1 << x), x, v + 1))
        return cur_v

    n = len(graph)
    s = (1 << n) - 1
    dp = [dfs(1 << i, i, 0) for i in range(n)]
    return min(dp)


def cf1993E():
    n, m = mint()
    a = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        cur = ints()
        for j, x in enumerate(cur):
            a[i][j] = x
            a[i][m] ^= x
            a[n][j] ^= x
            a[n][m] ^= x

    mask_n = (1 << (n + 1)) - 1
    mask_m = (1 << (m + 1)) - 1
    ans1 = [[inf] * 16 for _ in range(16)]
    dp = [[inf] * (1 << (n + 1)) for _ in range(n + 1)]
    for rmv in range(m + 1):
        w = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            for j in range(i + 1, n + 1):
                w[i][j] = 0
                for l in range(m + 1):
                    if l == rmv:
                        continue
                    w[i][j] += abs(a[i][l] - a[j][l])
                w[j][i] = w[i][j]

        for i in range(n + 1):
            for msk in range(1 << (n + 1)):
                dp[i][msk] = inf
            dp[i][1 << i] = 0

        for msk in range(1 << n + 1):
            for last in range(n + 1):
                if dp[last][msk] == inf:
                    continue
                other = (1 << n + 1) - 1 - msk
                while other:
                    x = other & -other
                    nxt = x.bit_length() - 1
                    dp[nxt][msk + x] = min(dp[nxt][msk + x], dp[last][msk] + w[last][nxt])
                    other -= x
                # if (1 << last) & msk == 0:
                #     continue
                # if msk.bit_count() == n:
                #     continue
                #
                # for nxt in range(n + 1):
                #     if (1 << nxt) & msk > 0:
                #         continue
                #     new_msk = msk | (1 << nxt)
                #     dp[nxt][new_msk] = min(dp[nxt][new_msk], dp[last][msk] + w[last][nxt])

        for i in range(n + 1):
            ans1[i][rmv] = inf
            msk = mask_n ^ (1 << i)
            for last in range(n + 1):
                ans1[i][rmv] = min(ans1[i][rmv], dp[last][msk])

    ans2 = [[inf] * 16 for _ in range(16)]
    dp = [[inf] * (1 << (m + 1)) for _ in range(m + 1)]
    for rmv in range(n + 1):
        w = [[0] * (m + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            for j in range(i + 1, m + 1):
                w[i][j] = 0
                for l in range(n + 1):
                    if l == rmv:
                        continue
                    w[i][j] += abs(a[l][i] - a[l][j])
                w[j][i] = w[i][j]

        for i in range(m + 1):
            for msk in range(1 << (m + 1)):
                dp[i][msk] = inf
            dp[i][1 << i] = 0

        for msk in range(1 << m + 1):
            for last in range(m + 1):
                if dp[last][msk] == inf:
                    continue
                other = (1 << m + 1) - 1 - msk
                while other:
                    x = other & -other
                    nxt = x.bit_length() - 1
                    dp[nxt][msk + x] = min(dp[nxt][msk + x], dp[last][msk] + w[last][nxt])
                    other -= x
                # if (1 << last) & msk == 0:
                #     continue
                # if msk.bit_count() == m:
                #     continue
                #
                # for nxt in range(m + 1):
                #     if (1 << nxt) & msk > 0:
                #         continue
                #     new_msk = msk | (1 << nxt)
                #     dp[nxt][new_msk] = min(dp[nxt][new_msk], dp[last][msk] + w[last][nxt])

        for i in range(m + 1):
            ans2[rmv][i] = inf
            msk = mask_m ^ (1 << i)
            for last in range(m + 1):
                ans2[rmv][i] = min(ans2[rmv][i], dp[last][msk])

    ans = inf
    for i in range(n + 1):
        for j in range(m + 1):
            ans = min(ans, ans1[i][j] + ans2[i][j])

    print(ans)
    return
