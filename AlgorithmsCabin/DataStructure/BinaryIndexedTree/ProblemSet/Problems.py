from bisect import bisect_left, bisect_right
from collections import defaultdict
from itertools import accumulate
from math import inf
from typing import List
from AlgorithmsCabin.DataStructure.BinaryIndexedTree.BIT import BIT


# 利用树状数组求逆序对的个数
def reversePairs(record: List[int]) -> int:
    # 先进行数据离散化
    nums = sorted(set(record))
    mx = len(nums)
    b = BIT(mx + 1)
    ans = 0
    for i, x in enumerate(record):
        j = bisect_left(nums, x) + 1
        ans += (i - b.query(j))
        b.add(j, 1)
    return ans


# 排列的逆序对的期望值
# 输入n和一个 1～n 的排列a, a有n*(n+1)/2 个非空连续子数组，从中等概率选择子数组b
# 设b的长度为k, b有k!种排列， 从中等概率随机挑选一个，替换a中的子数组b, 输出替换后a的逆序对的期望住

# 公式推导
# 考虑重排前（i，j）点对对答案的贡献 i < j
# 1. i,j 都在选中的段内, 选中段为[l, r] 满足 l ∈ [1,i],r ∈ [j,n], 易知全部可能的选法有 n*(n+1)/2种
# 选中的满足要求的概率为 2*i*(n-j+1)/n/(n+1）, （i, j）重排后有1/2的概率构成逆序对，对答案的贡献为i*(n-j+1)/n/(n+1）
# 这种情况的总贡献为 ∑（i=1,n）∑（j=i+1,n）i*(n-j+1)/n/(n+1） = ∑（i=1,n）i*(n-j+1)*(n-i)/2/n/(n+1）
# 2. i,j 不都在选中段内, 概率为1-2*i*(n-j+1)/n/(n+1）
# 由于 i,j 不都在选中段内，重排后i,j 的相对位置不变，则当且仅当ai > aj,(i,j) 对答案有贡献
# 这种情况的总贡献为∑（i=1,n）∑（j=i+1,n）（ai > aj）1-2*i*(n-j+1)/n/(n+1）

def cf749E(nums: List[int]):
    n = len(nums)
    b = BIT(n + 1)
    sm = 0
    ans = 0
    for i in range(1, n + 1):
        sm += 1.0 * i * (n - i + 1) * (n - i)
        ans += (b.query(n) - b.query(nums[i - 1])) * n * (n + 1)
        ans -= (b.askTr(n) - b.askTr(nums[i - 1])) * 2 * (n - i + 1)
        b.addTr(nums[i - 1], i)
    print(ans / n / (n + 1) + sm / 2 / n / (n + 1))
    return


# lc1505 最多K次交换相邻数位后得到的最小整数
def minInteger(num: str, k: int) -> str:
    # 贪心 加 树状数组
    # 每次移动最小的，如果距离允许移动
    # 不行，统计能移动最近的
    n = len(num)
    b = BIT(n + 1)
    dt = defaultdict(list)
    for i, x in enumerate(num):
        dt[int(x)].append(i)
        b.add(i + 1, 1)

    index = inf
    ans = ""
    vis = [0] * n
    keys = list(dt.keys())
    keys.sort()
    for x in keys:
        if k == 0:
            break
        for y in dt[x]:
            if k == 0:
                break
            dis = b.query(y)
            if dis > k:
                index = min(index, y)
                break
            else:
                if y < index:
                    ans += str(x)
                    vis[y] = 1
                    k -= dis
                    b.add(y + 1, -1)
    for i, x in enumerate(num):
        if vis[i] == 0:
            if i == index and k > 0:
                ans = ans[:len(ans) - k] + x + ans[len(ans) - k:]
            else:
                ans += x
    return ans


# lc493 翻转对
def reversePairs2(record: List[int]) -> int:
    # 先进行数据离散化
    nums = sorted(record)
    mx = len(nums)
    b = BIT(mx + 1)
    ans = 0
    # 对每一个x,在右边寻找< x / 2的个数，注意，把自己除外，如果自己也在其中，需要将计数-1
    for i, x in enumerate(record):
        v = x // 2 if x % 2 == 0 else x // 2 + 1
        j = bisect_left(nums, x) + 1
        j2 = bisect_left(nums, v) + 1
        ans += (j2 - 1 - b.query(j2 - 1))
        b.add(j, 1)
        if v > x:
            ans -= 1
    return ans


# lc327 区间和的个数
def countRangeSum(nums: List[int], lower: int, upper: int) -> int:
    pre = list(accumulate(nums, initial=0))
    nums = sorted(pre)
    mx = len(nums)
    b = BIT(mx + 1)
    ans = 0
    # 统计[x-upper,x-lower]的个数
    for i, x in enumerate(pre):
        j = bisect_left(nums, x) + 1
        r = bisect_right(nums, x - lower)    # <= x - lower , 注意原先应该-1，但是下标从1开始再+1
        l = bisect_left(nums, x - upper)     # < x - lower , 注意原先应该-1，但是下标从1开始再+1
        ans += b.query(r) - b.query(l)
        b.add(j, 1)
    return ans
