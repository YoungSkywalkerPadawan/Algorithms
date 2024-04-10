from itertools import accumulate
from math import inf
from typing import List


#  lc3086 拾起K个1需要的最小行动数
def minimumMoves(nums: List[int], k: int, maxChanges: int) -> int:
    # 先考虑需有足够的交换次数的情况
    # maxChanges >= k -c
    c = 0
    cur = 0
    for i, x in enumerate(nums):
        if x == 1:
            cur += 1
            c = max(cur, c)
        else:
            cur = 0
    c = min(c, k, 3)
    if maxChanges >= k - c:
        return max(c - 1, 0) + (k - c) * 2
    pos = [i for i, x in enumerate(nums) if x == 1]
    # 剩下的情况就是经典的货仓选址问题
    n = len(pos)
    pre_sum = list(accumulate(pos, initial=0))

    def calSumToMedian(l: int, r: int, m: int):
        s1 = pos[m] * (m - l) - (pre_sum[m] - pre_sum[l])
        s2 = pre_sum[r] - pre_sum[m] - pos[m] * (r - m)
        return s1 + s2

    ans = inf
    size = k - maxChanges
    for right in range(size, n + 1):
        left = right - size
        median = left + size // 2
        ans = min(ans, calSumToMedian(left, right, median))
    return ans + maxChanges * 2
