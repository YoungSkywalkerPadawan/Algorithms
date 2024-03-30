from bisect import bisect_left
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
