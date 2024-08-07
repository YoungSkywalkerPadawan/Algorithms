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


def cf797F():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()
    h = [list(map(int, input().split())) for _ in range(m)]
    h.sort()
    dp = [inf] * (n + 1)

    dp[0] = 0
    s = [0] * (n + 1)
    for i, (x, c) in enumerate(h, 1):
        q = [(0, 0)]
        l = 0
        r = 1
        for j, y in enumerate(a, 1):
            s[j] = s[j - 1] + abs(x - y)
            cur = dp[j] - s[j]
            # 右边更大的先弹出
            while r - l > 0 and q[-1][0] >= cur:
                q.pop()
                r -= 1
            q.append((cur, j))
            r += 1
            # 左边超出范围的也弹出
            while q[l][1] < j - c:
                l += 1
            dp[j] = q[l][0] + s[j]

    ans = dp[-1] if dp[-1] < inf else -1
    print(ans)
    return


def cf1941E():
    n, m, k, d = map(int, input().split())
    # 单调队列优化DP
    cost = [0] * (n + 1)
    ans = inf
    for i in range(1, n + 1):
        a = list(map(int, input().split()))
        h = deque([(1, 0)])
        for j in range(1, m):
            while h and h[0][1] < j - d - 1:
                h.popleft()
            cur = h[0][0] + a[j] + 1
            while h and h[-1][0] >= cur:
                h.pop()
            h.append((cur, j))
        cost[i] = cost[i - 1] + h[-1][0]
        if i >= k:
            ans = min(ans, cost[i] - cost[i - k])
    print(ans)
    return
