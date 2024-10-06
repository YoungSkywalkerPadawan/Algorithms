# 约束划分个数
# 将数组分成（恰好/至多）k 个连续子数组，计算与这些子数组有关的最优值。
# 一般定义f[i][j] 表示将长为j 的前缀a[:j] 分成i 个连续子数组所得到的最优解。
# 枚举最后一个子数组的左端点 𝐿，从 f[i−1][L] 转移到 f[i][j]，并考虑 a[L:j] 对最优解的影响。
from functools import cache
from itertools import accumulate
from math import inf
from typing import List

# lc3117 划分数组得到最小的值的和
from AlgorithmsCabin.Math.Util.utils import mint, ints


def minimumValueSum(nums: List[int], andValues: List[int]) -> int:
    @cache
    def dfs(x: int, y: int, pre: int) -> int:
        if y >= 0 and pre < andValues[y]:
            return inf
        if x < 0:
            return 0 if y <= 0 and pre == andValues[0] else inf

        # 不划
        res = dfs(x - 1, y, pre & nums[x])
        # 划
        if y >= 0 and pre == andValues[y]:
            res = min(res, nums[x] + dfs(x - 1, y - 1, nums[x]))
        return res

    ans = dfs(len(nums) - 2, len(andValues) - 1, nums[-1]) + nums[-1]
    dfs.cache_clear()
    return ans if ans < inf else -1


# lc1478 安排邮筒
def minDistance(houses: List[int], k: int) -> int:
    houses.sort()
    n = len(houses)
    pre = list(accumulate(houses, initial=0))

    @cache
    def dfs(x: int, y: int) -> int:
        if x == 0:
            return inf
        if y == 1:
            mid = x // 2
            if x % 2:
                return pre[x] - pre[mid + 1] - pre[mid]
            else:
                return pre[x] - pre[mid] - pre[mid]

        res = inf
        for i in range(x):
            mid = i + (x - i) // 2
            if (x - i) % 2:
                cur = pre[x] - pre[mid + 1] - (pre[mid] - pre[i])
            else:
                cur = pre[x] - pre[mid] - (pre[mid] - pre[i])
            res = min(res, dfs(i, y - 1) + cur)
        return res

    ans = dfs(n, k)
    dfs.cache_clear()
    return ans


# lc1278 分割回文串III
def palindromePartition(s: str, k: int) -> int:
    dp = [[0] * len(s) for _ in s]
    for i in range(len(s) - 2, -1, -1):
        dp[i][i + 1] = 0 if s[i] == s[i + 1] else 1
        for j in range(i + 2, len(s)):
            dp[i][j] = dp[i + 1][j - 1] if s[i] == s[j] else dp[i + 1][j - 1] + 1
    n = len(s)

    @cache
    def dfs(x: int, y: int) -> int:
        if x == 0:
            return inf
        if y == 1:
            return dp[0][x - 1]
        res = inf
        for i_ in range(x):
            res = min(res, dfs(i_, y - 1) + dp[i_][x - 1])
        return res

    ans = dfs(n, k)
    dfs.cache_clear()
    return ans


def cf1625C():
    n, t, k = mint()
    d = ints()
    d.append(t)
    a = ints()

    # 区间dp
    # def dfs(x: int, y: int) -> int:
    #     if x < 0:
    #         return 0
    #     if y == 0:
    #         return a[x] * (d[x + 1] - d[x]) + dfs(x - 1, y)
    #     res = a[x] * (d[x + 1] - d[x]) + dfs(x - 1, y)
    #     for j in range(1, y+1):
    #         if x - j >= 0:
    #             res2 = a[x - j] * (d[x + 1] - d[x - j]) + dfs(x - j - 1, y - j)
    #             if res2 < res:
    #                 res = res2
    #         else:
    #             break
    #     return res
    #
    # ans = dfs(n-1, k)
    # print(ans)
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    for j in range(k + 1):
        for i in range(1, n + 1):
            if j == 0:
                dp[i][j] = a[i - 1] * (d[i] - d[i - 1]) + dp[i - 1][j]
            else:
                res = a[i - 1] * (d[i] - d[i - 1]) + dp[i - 1][j]
                for p in range(1, j + 1):
                    if i - p - 1 >= 0:
                        res2 = a[i - p - 1] * (d[i] - d[i - p - 1]) + dp[i - p - 1][j - p]
                        if res2 < res:
                            res = res2
                    else:
                        break
                dp[i][j] = res
    print(dp[n][k])

    return
