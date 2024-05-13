# 约束划分个数
# 将数组分成（恰好/至多）k 个连续子数组，计算与这些子数组有关的最优值。
# 一般定义f[i][j] 表示将长为j 的前缀a[:j] 分成i 个连续子数组所得到的最优解。
# 枚举最后一个子数组的左端点 𝐿，从 f[i−1][L] 转移到 f[i][j]，并考虑 a[L:j] 对最优解的影响。
from functools import cache
from math import inf
from typing import List


# lc3117 划分数组得到最小的值的和
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
