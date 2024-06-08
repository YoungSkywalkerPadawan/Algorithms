# 最长递增子序列
# 1.枚举选哪个
# 2.二分贪心
# 3.计算a和把a排序后的数组sortedA的最长公共子序列
# 4.数据结构优化
from bisect import bisect_left
from collections import Counter
from typing import List
from AlgorithmsCabin.DataStructure.BinaryIndexedTree.BIT import BIT
from AlgorithmsCabin.DataStructure.SegmentTree.SegmentTree import SegmentTree


# 最长递增子序列I
def lengthOfLIS(nums: List[int]) -> int:
    n = len(nums)
    res = [0] * n
    for i, x in enumerate(nums):
        mx = 0
        for j in range(i):
            if nums[j] < x:
                mx = max(mx, res[j])
        res[i] = mx + 1
    return max(res)


# 这是最长递增子序列I的加强版，一方面加入了整数K（子序列相邻元素差）的限制
# 另一方面，数组的大小最大将达到10^5,对于时间复杂度有了更高的要求。因此，在原先动态规划的基础上，还需要进行优化

# 首先模仿最长递增子序列I，使用动态规划（递推）。dp[i] = max(dp[j]) + 1
# 其中，j < i,nums[i]-k=<nums[j]<=nums[i]-1
# 时间复杂度:O(n^2), 空间复杂度:O(n)
def lengthOfLIS_II(nums: List[int], k: int) -> int:
    # dp 递推 时间复杂度O(n^2)
    n = len(nums)
    # 维护以当前索引元素为终点的最长递增子序列数量
    dp = [0] * n
    for i, x in enumerate(nums):
        mx = 0
        for j in range(i):
            if nums[j] < x and x - nums[j] <= k:
                mx = max(mx, dp[j])
        dp[i] = mx + 1
    return max(dp)


# 优化思路
# 在动态规划过程中，计算每一个dp[i] 都需要遍历之前的dp元素以查询最大值
# 因此整个过程具有区间查询和单点更新的特性。基于该特性可以用树状数组和线段树进行优化
# 其中，树状数组大多用于区间求和，要查询[x,y]的区间和，求出[1,x-1]的和与[1,y]的和，然后相减就得出了[x,y]区间的和
# 而区间最值则没有这个性质。因此，在查询的时候，不能直接更新y = y & (y - 1)。需要判断该值是否在区间内，如果不在的话则更新y = y - 1

# 树状数组优化 时间复杂度O(n(logn)^2) 空间复杂度O(n)
# 从二进制的角度分析，直接计算[1,y]的最值，可以通过直接计算y = y & (y - 1) 每次更新 y 最低位的1变为0，直到最后变成0退出循环
# 已知该过程时间复杂度为O（logn）
# 在计算[x,y]的最值时 （x > 1），每次更新的时候如果通过最低位直接由1变成0的方式小于x,则y进行减1操作
# 此时y的最低位变成了1，又需要重新进行之前的变0操作，经过一次logn操作，y与x不同的最高位至少下降了1位
# 与之前相比，logn次操作相当于之前的一次操作，所以时间复杂度为原先的logn倍，即O(n(logn)^ 2)
def lengthOfLIS_BIT(nums: List[int], k: int) -> int:
    mx = max(nums)
    t = BIT(mx + 1)
    for x in nums:
        f = t.query_max(max(x - k, 1), x - 1) + 1
        t.update(x, f)
    return t.query_max(1, mx)


# 时间复杂度:O(nlogn), 空间复杂度:O(n)
def lengthOfLIS_ST(nums: List[int], k: int) -> int:
    # 线段树优化
    mx = max(nums)
    t = SegmentTree(mx)
    for x in nums:
        if x == 1:
            t.update(1, 1, mx, 1, 1)
        else:
            f = t.query(1, 1, mx, max(x - k, 1), x - 1) + 1
            t.update(1, 1, mx, x, f)
    return t.query(1, 1, mx, 1, mx)


# 线段树的特性直接能查询区间内的最大值，不需要进行特殊判断，相比树状数组更简单。
# 树状数组能做的题目，基本都能用线段树进行优化。但线段树涉及的变量更多，树状数组相对更简洁。


# 前后缀分解，分布统计a[i]结尾和a[i]开始的最长递增子序列
# 如果pre[i] + suf[i] - 1 = 原最长递增子序列的长度，则有可能是必须
# 统计pre[i]各value出现的次数，如果出现次数大于1，则为非必须，剩下的是必须
def cf486E():
    n = int(input())
    a = list(map(int, input().split()))
    b = sorted(set(a))  # 离散化
    t = BIT(len(b) + 1)
    suf = [0] * len(a)
    mx = 0
    for i in range(n - 1, -1, -1):
        x = a[i]
        j = len(b) - bisect_left(b, x)  # 离散化后的值（从 1 开始）
        f = t.pre_max(j - 1) + 1
        suf[i] = f
        mx = max(mx, f)
        t.update(j, f)
    ans = ['1'] * n
    pres = [0] * n
    t2 = BIT(len(b) + 1)
    cnt = Counter()
    for i, x in enumerate(a):
        j = bisect_left(b, x) + 1  # 离散化后的值（从 1 开始）
        f = t2.pre_max(j - 1) + 1
        pre = f
        pres[i] = pre
        if suf[i] + pre - 1 == mx:
            ans[i] = '3'
            cnt[pre] += 1
        t2.update(j, f)

    for i, v in enumerate(pres):
        if cnt[v] > 1 and ans[i] == '3':
            ans[i] = '2'
    print("".join(ans))

    return


# 离线查询
# 统计a[i]所对应的修改的值，两种情况。
# 1.最长递增子序列带这个值，则用之前前后缀分解的时候同时计算
# 2.不带这个值，则考虑原序列这个值是否必须
# 必须则原最长递增序列长度-1，反之为原最长递增子序列长度
def cf650D():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    st = set(a)
    queries = [[] for _ in range(n)]
    for i in range(q):
        idx, val = map(int, input().split())
        queries[idx - 1].append(val * q + i)

    ans = [0] * q
    b = sorted(st)  # 离散化
    t = BIT(len(b) + 1)
    suf = [0] * len(a)
    mx = 0
    for i in range(n - 1, -1, -1):
        for v in queries[i]:
            val, q_idx = divmod(v, q)
            i_v = bisect_left(b, val)
            ans_j = len(b) - i_v  # 离散化后的值（从 1 开始）
            ans_j = ans_j - 1 if i_v < len(b) and val == b[i_v] else ans_j
            ans[q_idx] += t.pre_max(ans_j) + 1

        x = a[i]
        j = len(b) - bisect_left(b, x)  # 离散化后的值（从 1 开始）
        f = t.pre_max(j - 1) + 1
        suf[i] = f
        if f > mx:
            mx = f
        t.update(j, f)

    res = ['1'] * n
    pres = [0] * n
    t2 = BIT(len(b) + 1)
    cnt = Counter()
    for i, x in enumerate(a):
        for v in queries[i]:
            val, q_idx = divmod(v, q)
            ans_j = bisect_left(b, val) + 1  # 离散化后的值（从 1 开始）
            ans[q_idx] += t2.pre_max(ans_j - 1)

        j = bisect_left(b, x) + 1  # 离散化后的值（从 1 开始）
        f = t2.pre_max(j - 1) + 1
        pre = f
        pres[i] = pre
        if suf[i] + pre - 1 == mx:
            res[i] = '3'
            cnt[pre] += 1
        t2.update(j, f)

    for i, v in enumerate(pres):
        if cnt[v] > 1 and res[i] == '3':
            res[i] = '2'

    for i in range(n):
        if res[i] == '3':
            for v in queries[i]:
                q_idx = v % q
                if mx - 1 > ans[q_idx]:
                    ans[q_idx] = mx - 1
        else:
            for v in queries[i]:
                q_idx = v % q
                if mx > ans[q_idx]:
                    ans[q_idx] = mx

    print('\n'.join(map(str, ans)))
    return
