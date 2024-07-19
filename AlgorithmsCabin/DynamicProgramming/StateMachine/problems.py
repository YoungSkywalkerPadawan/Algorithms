# 状态集DP
# 一般定义 f[i][j]表示在前缀a[:i]在状态j下的最优值， 一般j都很小， 比如股票交易问题
from functools import cache
from math import inf
from typing import List
from AlgorithmsCabin.Math.Util.utils import mint, fac

MOD = 10 ** 9 + 7
# lc121 买卖股票的最佳时机


def maxProfit(prices: List[int]) -> int:
    n = len(prices)

    # 第i天结束手上没有股票和有股票两个状态，false表示没有,true 表示有
    # k 表示限制的次数
    @cache
    def dfs(i: int, hold: bool, k: int) -> int:
        if i < 0:
            return -inf if hold else 0

        if hold:
            # 之前一天就是持有，或者之前一天没持有今天买了
            res1 = dfs(i - 1, True, k)
            res2 = -inf
            if k > 0:
                # 之前一天就是持有，或者之前一天没持有今天买了
                res2 = dfs(i - 1, False, k - 1) - prices[i]
            return max(res1, res2)

        # 之前一天就是没有，或者之前一天持有今天卖了
        res1 = dfs(i - 1, False, k)
        res2 = dfs(i - 1, True, k) + prices[i]
        return max(res1, res2)

    return dfs(n - 1, False, 1)


# lc1363 形成三的最大倍数
def largestMultipleOfThree(nums: List[int]) -> str:
    nums.sort()
    n = len(nums)

    @cache
    def dfs(x: int, s: int) -> int:

        if x < 0:
            return -inf if s != 0 else 0

        res1 = dfs(x - 1, s)
        res2 = dfs(x - 1, (nums[x] + s) % 3) + 1
        return max(res1, res2)

    if dfs(n - 1, 0) == 0:
        return ""

    @cache
    def dfs2(x: int, s: int) -> str:

        if x < 0:
            return ""

        res1 = dfs(x - 1, s)
        res2 = dfs(x - 1, (nums[x] + s) % 3) + 1
        if res1 > res2:
            return dfs2(x - 1, s)
        return str(nums[x]) + dfs2(x - 1, (nums[x] + s) % 3)

    ans = dfs2(n - 1, 0)
    if ans[0] == '0':
        return '0'
    return ans


def cf1185G2():
    n, tot = mint()
    f = [[0] * (tot + 1) for _ in range(n + 2)]
    f[0][0] = 1
    g = [[[0] * (tot + 1) for _ in range(n + 2)] for _ in range(n + 2)]
    g[0][0][0] = 1

    # 开始多维0-1背包DP
    # 分别计算选出i个1,时长为t的方案数f[i][t]
    # 选出j个2,k个3时长为t的方案数g[j][k][t]
    cnt = [0] * 3
    for i in range(n):
        w, tp = mint()
        tp -= 1
        if tp == 0:
            for j in range(cnt[0], -1, -1):
                for t in range(tot, w - 1, -1):
                    f[j + 1][t] = (f[j + 1][t] + f[j][t - w]) % MOD
        else:
            idx = [0] * 3
            idx[tp] = 1
            for j in range(cnt[1], -1, -1):
                for k in range(cnt[2], -1, -1):
                    for t in range(tot, w - 1, -1):
                        g[j + idx[1]][k + idx[2]][t] = (g[j + idx[1]][k + idx[2]][t] + g[j][k][t - w]) % MOD
        cnt[tp] += 1

    ans = 0
    c = [[[[0] * 3 for _ in range(cnt[2] + 2)] for _ in range(cnt[1] + 2)] for _ in range(cnt[0] + 2)]
    c[1][0][0][0] = 1
    c[0][1][0][1] = 1
    c[0][0][1][2] = 1
    # 开始状态机DP
    for i, mat in enumerate(c[:cnt[0] + 1]):
        for j, row in enumerate(mat[:cnt[1] + 1]):
            for k, comb in enumerate(row[:cnt[2] + 1]):
                sm = 0
                for t, fit in enumerate(f[i]):
                    sm = (sm + fit * g[j][k][tot - t]) % MOD

                ans = (ans + fac(i) * fac(j) % MOD * fac(k) % MOD * (comb[0] + comb[1] + comb[2]) % MOD * sm) % MOD
                c[i + 1][j][k][0] = (c[i + 1][j][k][0] + comb[1] + comb[2]) % MOD
                c[i][j + 1][k][1] = (c[i][j + 1][k][1] + comb[0] + comb[2]) % MOD
                c[i][j][k + 1][2] = (c[i][j][k + 1][2] + comb[0] + comb[1]) % MOD
    print(ans)
    return
