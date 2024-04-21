import math
from functools import cache
from math import inf
from typing import List
from collections import Counter


# 相邻无关
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


# 相邻相关
# lc2741 特别的排列
def specialPerm(nums: List[int]) -> int:
    MOD = 10 ** 9 + 7

    @cache  # 缓存装饰器，避免重复计算 dfs 的结果
    def dfs(i: int, j: int, pre: int) -> int:
        if i < 0:
            return 1
        res = 0
        for x in range(j.bit_length()):
            if (1 << x) & j > 0:
                if pre < 0:
                    res += dfs(i - 1, j ^ (1 << x), nums[x])
                else:
                    cur = nums[x]
                    if cur % pre == 0 or pre % cur == 0:
                        res += dfs(i - 1, j ^ (1 << x), nums[x])
        return res % MOD

    n = len(nums)
    s = (1 << n) - 1
    return dfs(n - 1, s, -1)


# lc996 正方形数组的数目
def numSquarefulPerms(nums: List[int]) -> int:
    def is_perfect_square(el):
        if el < 0:
            return False
        return math.sqrt(el) % 1 == 0

    @cache  # 缓存装饰器，避免重复计算 dfs 的结果
    def dfs(i: int, j: int, pre: int) -> int:
        if i < 0:
            return 1
        res = 0
        for x in range(j.bit_length()):
            if (1 << x) & j > 0:
                if pre < 0:
                    res += dfs(i - 1, j ^ (1 << x), nums[x])
                else:
                    cur = nums[x] + pre
                    if is_perfect_square(cur):
                        res += dfs(i - 1, j ^ (1 << x), nums[x])
        return res

    n = len(nums)
    s = (1 << len(nums)) - 1
    counter = Counter(nums)
    rep = 1
    for k, v in counter.items():
        while v:
            rep *= v
            v -= 1
    return dfs(n - 1, s, -1) // rep


# lc1681 最小不兼容性
def minimumIncompatibility(nums: List[int], k: int) -> int:
    nums.sort()
    n = len(nums)
    if n == k:
        return 0
    cnt = n // k
    m = 1 << n

    @cache
    def dp(i: int, j: int) -> int:
        if i < 0:
            return 0

        # 对于每一组，先选最小值，排好序后最小的为lowbit，方便计算不兼容性
        lb = j & -j
        p = lb.bit_length() - 1

        # 相邻相关，当前所选不能和上一次的值相同
        def dfs(cur_s, pre, index):

            if cur_s.bit_count() == cnt:
                return dp(i - 1, j ^ cur_s) + nums[pre] - nums[p]

            if index == n:
                return inf
            # 不选
            res = dfs(cur_s, pre, index + 1)
            # 相邻不相等才能选
            if (1 << index) & j > 0 and nums[index] > nums[pre]:
                res = min(res, dfs(cur_s | (1 << index), index, index + 1))
            return res

        return dfs(lb, p, p + 1)

    ans = dp(k - 1, m - 1)
    dp.cache_clear()
    return ans if ans < inf else -1
