from functools import cache
from typing import List

# lc546 移除盒子
from AlgorithmsCabin.Math.Util.utils import sint, ints


def removeBoxes(boxes: List[int]) -> int:
    # 计算区间[x, y]的分数，k为[y+1,)等于boxes[r]的个数
    @cache
    def dfs(x: int, y: int, k: int) -> int:

        if x > y:
            return 0

        while y > x and boxes[y] == boxes[y - 1]:
            y -= 1
            k += 1
        res = dfs(x, y - 1, 0) + (k + 1) ** 2
        # 保留，再后面计算
        for i in range(x, y):
            if boxes[i] == boxes[y]:
                cur = dfs(x, i, k + 1) + dfs(i + 1, y - 1, 0)
                if cur > res:
                    res = cur
        return res

    return dfs(0, len(boxes) - 1, 0)


# lc312 戳气球
def maxCoins(nums: List[int]) -> int:
    # 正难则反，考虑添加气球，加入哨兵
    @cache
    def dfs(x: int, y: int) -> int:

        res = 0
        for i in range(x + 1, y):
            cur = nums[x] * nums[y] * nums[i] + dfs(x, i) + dfs(i, y)
            if cur > res:
                res = cur
        return res

    nums.insert(0, 1)
    nums.append(1)

    n = len(nums)
    ans = dfs(0, n - 1)
    dfs.cache_clear()
    return ans


def cf1509C():
    n = sint()
    a = ints()
    a.sort()

    # 区间DP
    # def dfs(x: int, y: int) -> int:
    #     if x == y:
    #         return 0
    #     res1 = dfs(x + 1, y)
    #     res2 = dfs(x, y - 1)
    #     return min(res1, res2) + a[y] - a[x]
    #
    # ans = dfs(0, n - 1)
    # print(ans)
    dp = [[0] * n for _ in range(n)]

    for i in range(1, n):
        for j in range(n - i):
            s, e = j, j + i
            dp[s][e] = min(dp[s + 1][e], dp[s][e - 1]) + a[e] - a[s]

    print(dp[0][n - 1])
    return
