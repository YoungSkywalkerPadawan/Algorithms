# 状态集DP
# 一般定义 f[i][j]表示在前缀a[:i]在状态j下的最优值， 一般j都很小， 比如股票交易问题
from functools import cache
from math import inf
from typing import List


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
