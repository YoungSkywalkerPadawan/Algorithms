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