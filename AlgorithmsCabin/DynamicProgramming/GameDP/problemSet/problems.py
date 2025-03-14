from collections import Counter
from functools import cache
from itertools import accumulate
from math import inf
from typing import List

# lc1140 石子游戏II
from AlgorithmsCabin.Math.Util.utils import mint, ints


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


def cf2002A():
    l, n, m = mint()
    a = ints()
    g = [ints() for _ in range(n)]
    # dp = [[[0] * 8 for _ in range(m + 1)] for _ in range(n + 1)]
    # # dp[i][j][v]表示从[i][j]开始到[n][m]是否能找到v
    # for i in range(n - 1, -1, -1):
    #     for j in range(m - 1, -1, -1):
    #         for v in range(8):
    #             if g[i][j] == v or dp[i + 1][j][v] or dp[i][j + 1][v]:
    #                 dp[i][j][v] = 1

    # 当层可选状态, 1 表示可选
    f = [[True for _ in range(m + 1)] for _ in range(n + 1)]
    for k in range(l - 1, -1, -1):
        v = a[k]
        # 这一层的状态, 看能不能在可选状态中找到v
        flag = False
        diff = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
        for i in range(n - 1, -1, -1):
            for j in range(m - 1, -1, -1):
                if f[i][j] and g[i][j] == v:
                    flag = True
                    if i > 0 and j > 0:
                        diff[1][1] += 1
                        diff[i + 1][1] -= 1
                        diff[1][j + 1] -= 1
                        diff[i + 1][j + 1] += 1

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                diff[i][j] += diff[i - 1][j] + diff[i][j - 1] - diff[i - 1][j - 1]
                if diff[i][j]:
                    f[i - 1][j - 1] = False
                else:
                    f[i - 1][j - 1] = True
        if k == 0:
            print("T" if flag else "N")

    return


def cf1728D():
    s = input()

    def comp(c, d) -> int:
        if c == d:
            return 0
        return -1 if c < d else 1
        # 动态规划

    n = len(s)
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    for k in range(2, n + 1, 2):
        for l in range(n - k + 1):
            r = l + k
            dp[l][r] = 1
            # Alice 尽量要使得结果小
            # Alice选l
            # Bob 要尽量大，Bob两种选择l+1, r-1
            res1 = dp[l + 1][r - 1] if dp[l + 1][r - 1] != 0 else comp(s[l], s[r - 1])
            res2 = dp[l + 2][r] if dp[l + 2][r] != 0 else comp(s[l], s[l + 1])
            res = res1 if res1 > res2 else res2
            if res < dp[l][r]:
                dp[l][r] = res
            # Alice选r-1
            # Bob 要尽量大，Bob两种选择l, r-2
            res1 = dp[l + 1][r - 1] if dp[l + 1][r - 1] != 0 else comp(s[r - 1], s[l])
            res2 = dp[l][r - 2] if dp[l][r - 2] != 0 else comp(s[r - 1], s[r - 2])
            res = res1 if res1 > res2 else res2
            if res < dp[l][r]:
                dp[l][r] = res
    if dp[0][n] == -1:
        print("Alice")
    elif dp[0][n] == 0:
        print("Draw")
    else:
        print("Bob")

    return
