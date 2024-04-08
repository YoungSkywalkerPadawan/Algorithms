from functools import cache
from math import inf
from typing import List


# lc1879 两个数组的最小异或值和
def minimumXORSum(nums1: List[int], nums2: List[int]) -> int:
    @cache  # 缓存装饰器，避免重复计算 dfs 的结果
    def dfs(i: int, j: int) -> int:
        if i < 0:
            return 0
        res = inf
        for x in range(j.bit_length()):
            if (1 << x) & j > 0:
                cur = nums1[i] ^ nums2[x]
                res = min(res, cur + dfs(i - 1, j ^ (1 << x)))
        return res

    n = len(nums1)
    s = (1 << n) - 1
    return dfs(n - 1, s)


# lc2172 数组的最大与和
def maximumANDSum(nums: List[int], numSlots: int) -> int:
    @cache  # 缓存装饰器，避免重复计算 dfs 的结果
    def dfs(i: int, j: int) -> int:
        if j.bit_count() > i:
            return -inf
        if i < 1:
            return 0 if j == 0 else -inf
        res = dfs(i - 1, j)  # 第 i 篮子空着
        for x in range(j.bit_length()):
            if (1 << x) & j > 0:
                cur = i & nums[x] if i <= numSlots else ((i - numSlots) & nums[x])
                res = max(res, cur + dfs(i - 1, j ^ (1 << x)))
        return res

    s = (1 << len(nums)) - 1
    return dfs(numSlots * 2, s)
