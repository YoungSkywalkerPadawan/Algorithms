# 严格按顺序从小到大生成所有回文数（不用字符串转换）
from bisect import bisect_left
from math import inf
from typing import List

pal = []
base = 1
while base <= 10000:
    # 生成奇数长度回文数
    for i_ in range(base, base * 10):
        x_ = i_
        t = i_ // 10
        while t:
            x_ = x_ * 10 + t % 10
            t //= 10
        pal.append(x_)
    # 生成偶数长度回文数
    if base <= 1000:
        for i_ in range(base, base * 10):
            x_ = t = i_
            while t:
                x_ = x_ * 10 + t % 10
                t //= 10
            pal.append(x_)
    base *= 10
pal.append(inf)  # 哨兵，防止下面代码中的 i 下标越界


# lc2967 使数组成为等数数组的最小代价
def minimumCost(nums: List[int]) -> int:
    nums.sort()

    # 返回 nums 中的所有数变成 pal[i] 的总代价
    def cost(i: int) -> int:
        target = pal[i]
        return sum(abs(x - target) for x in nums)

    n = len(nums)
    j = bisect_left(pal, nums[(n - 1) // 2])  # 二分找中位数右侧最近的回文数
    if pal[j] <= nums[n // 2]:  # 回文数在中位数范围内
        return cost(j)  # 直接变成 pal[i]
    return min(cost(j - 1), cost(j))  # 枚举离中位数最近的两个回文数 pal[i-1] 和 pal[i]
