# 单调队列优化DP：一般用来维护一段转移来源的最值。
# 前提：区间右端点变大时，左端点也在变大(同滑动窗口)。
# 1.转移前，去掉队首无用数据。
# 2.计算转移（直接从队首转移）。
# 3.把数据（一般是f[i]）插入队尾前，去掉队尾无用数据。
from collections import deque
from itertools import pairwise, accumulate
from math import inf
from typing import List


# lc1425 带限制的子序列和
def constrainedSubsetSum(nums: List[int], k: int) -> int:
    q = deque([(0, nums[0])])
    n = len(nums)
    dp = [0] * n
    dp[0] = nums[0]
    for i in range(1, n):
        l = max(0, i - k)
        while q[-1][0] < l:  # 右边离开窗口
            q.pop()
        f = nums[i] + q[-1][1] if q[-1][1] > 0 else nums[i]
        dp[i] = f
        while q and f >= q[0][1]:
            q.popleft()
        q.appendleft((i, f))  # 左边进入窗口
    return max(dp)


# lc1687 从仓库到码头运输箱子
def boxDelivering(boxes: List[List[int]], maxBoxes: int, maxWeight: int) -> int:
    n = len(boxes)
    c = [int(a != b) for a, b in pairwise(box[0] for box in boxes)]
    cs = list(accumulate(c, initial=0))
    ws = list(accumulate((box[1] for box in boxes), initial=0))
    f = [inf] * (n + 1)
    f[0] = 0
    q = deque([(0, 0)])
    for i in range(1, n + 1):
        l = max(0, i - maxBoxes)
        while q and (q[-1][0] < l or ws[i] - ws[q[-1][0]] > maxWeight):  # 右边离开窗口
            q.pop()
        f[i] = cs[i - 1] + q[-1][1] + 2
        if i < n:
            while q and f[i] - cs[i] <= q[0][1]:
                q.popleft()
            q.appendleft((i, f[i] - cs[i]))  # 左边进入窗口

    return f[n]
