from collections import Counter
from functools import cache
from itertools import accumulate
from math import inf
from typing import List


# lc1140 石子游戏II
def stoneGameII(piles: List[int]) -> int:
    s = list(accumulate(piles, initial=0))  # 前缀和

    @cache  # 缓存装饰器，避免重复计算 dfs 的结果
    def dfs(i: int, j: int) -> int:
        if i == n - 1:  # 递归边界
            return piles[i]
        if i > n - 1:
            return 0
        res = -inf
        for k in range(1, 2 * j + 1):
            if i + k <= n:
                res = max(res, s[i + k] - s[i] - dfs(i + k, max(j, k)))
        return res

    n = len(piles)
    ans = dfs(0, 1)
    dfs.cache_clear()  # 防止爆内存
    return (ans + sum(piles)) // 2


# lc1872 石子游戏VIII
def stoneGameVIII(piles: List[int]) -> int:
    s = list(accumulate(piles, initial=0))  # 前缀和

    @cache  # 缓存装饰器，避免重复计算 dfs 的结果
    def dfs(i: int) -> int:
        if i >= n - 1:
            return s[n]
        res = dfs(i + 1)
        res = max(res, s[i + 1] - dfs(i + 1))
        return res

    n = len(piles)
    ans = dfs(1)
    dfs.cache_clear()  # 防止爆内存
    return ans


def cf1987B():
    int(input())
    a = list(map(int, input().split()))
    cnt = Counter(a)
    a = list(set(a))
    a.sort()
    m = len(a)
    # 尽可能大的选择
    # @cache
    # def dfs(x: int, y: int) -> int:
    #     if x == m:
    #         return 0
    #     res = dfs(x+1, y + 1)
    #     # 可选
    #     if cnt[a[x]] <= y:
    #         res2 = dfs(x+1, y - cnt[a[x]]) + 1
    #         if res2 > res:
    #             res = res2
    #     return res
    #
    # cur = dfs(0,0)
    # dfs.cache_clear()
    dp = [[0] * (m + 1) for _ in range(m + 1)]
    for i in range(m - 1, -1, -1):
        for j in range(i + 1):
            dp[i][j] = dp[i + 1][j + 1]
            if cnt[a[i]] <= j:
                dp[i][j] = max(dp[i][j], dp[i + 1][j - cnt[a[i]]] + 1)

    print(len(a) - dp[0][0])
    return


def cf1966C():
    # n = int(input())
    a = list(map(int, input().split()))
    # 注意每次的缓冲
    cnt = Counter(a)
    res = list(cnt.keys())
    res.sort()
    sub = [0] * (len(res))
    if res[0] > 1:
        sub[0] = 1
    for i in range(1, len(res) - 1):
        if res[i] - res[i - 1] > 1:
            sub[i] = 1
    n = len(sub)
    dp = [[0] * 2 for _ in range(n)]
    dp[-1][0] = dp[-1][1] = 1
    for i in range(n - 2, -1, -1):
        if sub[i] == 0:
            dp[i][0] = 1 if dp[i + 1][1] == 0 else 0
            dp[i][1] = 1 if dp[i + 1][0] == 0 else 0
        else:
            if dp[i + 1][0] == 1 or dp[i + 1][1] == 0:
                dp[i][0] = 1
            if dp[i + 1][1] == 1 or dp[i + 1][0] == 0:
                dp[i][1] = 1

    if dp[0][0] == 1:
        print("Alice")
    else:
        print("Bob")
    return
