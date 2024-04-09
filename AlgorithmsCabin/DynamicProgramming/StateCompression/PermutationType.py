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


# lc1681 最小不兼容性
def minimumIncompatibility(nums: List[int], k: int) -> int:
    n = len(nums)
    if n == k:
        return 0
    cnt = n // k
    m = 1 << n
    mx = [0] * m
    mn = [16] * m
    same = [0] * m
    count = [0] * m
    for index, x in enumerate(nums):
        bit = 1 << index
        val = 1 << x
        for j in range(bit):
            if (same[j] == -1) or ((same[j] | val) == same[j]):
                same[bit | j] = -1
            else:
                same[bit | j] = same[j] | val
            mx[bit | j] = mx[j] if mx[j] >= x else x
            mn[bit | j] = mn[j] if mn[j] <= x else x
            count[bit | j] = count[j] + 1

    @cache
    def dfs(i: int, mask: int) -> int:
        if i == 0:
            return -1 if same[j] == -1 else mx[j] - mn[j]
        s = mask
        res = inf
        while s:
            if count[s] == cnt and (same[s] != -1):
                pre = dfs(i - 1, j ^ s)
                if pre != -1:
                    cur = mx[s] - mn[s] + pre
                    res = res if res <= cur else cur
            s = (s - 1) & j
        return -1 if res == inf else res

    return dfs(k - 1, m - 1)
