from collections import deque
from typing import List

from sortedcontainers import SortedList

from AlgorithmsCabin.DataStructure.SegmentTree.SegmentTree import SegmentTree

# lc2298 使数组按非递减顺序排序
# 使用线段树进行单点更新和区间最大值查询
from AlgorithmsCabin.Math.Util.utils import sint


def totalSteps(nums: List[int]) -> int:
    # 若当前元素nums[i]需要被删除，找到左边第一个比它大的元素nums[j]
    # 看这段区间[j+1,i-1]内被删的元素的最大时间，该元素被删除的时间为最大时间+1
    # 用单调栈维护左边第一个比它大的元素
    mx = len(nums) + 1
    t = SegmentTree(mx)
    dq = deque()
    ans = 0
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        if dq:
            j = dq[-1]  # 左边第一个比它大的元素
            time = t.query(1, 1, mx, j + 2, i)  # 线段树下标从1开始[j+1,i-1] ->[j+2, i]
            ans = max(ans, time + 1)
            t.update(1, 1, mx, i + 1, time + 1)
        dq.append(i)

    return ans


# lc131双周赛T4 物块放置查询
def getResults(queries: List[List[int]]) -> List[bool]:
    mx = max(q[1] for q in queries) + 1
    sl = SortedList((0, mx))  # 哨兵
    ans = []
    st = SegmentTree(mx)
    for row in queries:
        x = row[1]
        i = sl.bisect_right(x)
        nxt = sl[i]
        pre = sl[i - 1]
        cur = max(x - pre, st.query(1, 0, mx, 0, pre))
        if row[0] == 1:
            st.update(1, 0, mx, x, x - pre)
            st.update(1, 0, mx, nxt, nxt - x)
            sl.add(x)
        else:
            ans.append(cur >= row[2])

    return ans


# lc2940 找到Alice和Bob可以相遇的建筑
def leftmostBuildingQueries(heights: List[int], queries: List[List[int]]) -> List[int]:
    # 在线方式 线段树二分
    mx = len(heights)
    t = SegmentTree(mx)
    n = len(heights)
    for i in range(n):
        t.update(1, 1, mx, i + 1, heights[i])
    ans = []
    for i, j in queries:
        if i > j:
            i, j = j, i
        if i == j or heights[i] < heights[j]:
            ans.append(j)
        else:
            pos = t.BinaryQuery(1, 1, n, j + 1, heights[i])
            ans.append(pos - 1)  # 不存在时刚好得到 -1
    return ans


def cf1535D():
    k = sint()
    s = list(input())
    s = s[::-1]

    n = 1 << k
    cnt = [1] * (2 * n)

    def upd(i: int) -> None:
        c1 = cnt[i * 2 + 1] if s[i] != '0' else 0
        c2 = cnt[i * 2 + 2] if s[i] != '1' else 0
        cnt[i] = c1 + c2

    for i_ in range(n - 2, -1, -1):
        upd(i_)

    q = sint()
    while q:
        p, c = map(str, input().split())
        p = int(p)
        p = n - p - 1
        s[p] = c
        while p:
            upd(p)
            p = (p - 1) // 2
        upd(0)
        print(cnt[0])
        q -= 1
    return
