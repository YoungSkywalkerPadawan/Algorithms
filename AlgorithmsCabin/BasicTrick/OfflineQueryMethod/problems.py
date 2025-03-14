# 离线查询：通过改变回答询问的顺序，使问题更容易处理
# 相应的，在线算法就是按照输入的顺序处理，来一个处理一个
from heapq import heappush, heappop
from math import inf
from typing import List
from sortedcontainers import SortedList
from AlgorithmsCabin.DataStructure.UnionFind.UnionFind import UnionFind


# lc1847 最近的房间ls
def closestRoom(rooms: List[List[int]], queries: List[List[int]]) -> List[int]:
    # 离线查询
    n = len(rooms)
    rooms.sort(key=lambda v: -v[1])
    m = len(queries)
    ans = [-1] * m
    sl = SortedList((-inf, inf))
    j = 0
    for i, (p, s) in sorted(enumerate(queries), key=lambda v: -v[1][1]):

        while j < n and rooms[j][1] >= s:
            sl.add(rooms[j][0])
            j += 1
        if len(sl) > 2:
            idx = sl.bisect_left(p)
            val = sl[idx] - p
            cur = sl[idx]
            val2 = p - sl[idx - 1]
            if val2 <= val:
                cur = sl[idx - 1]
            ans[i] = cur
    return ans


# lc1851 包含每个查询的最小区间
def minInterval(intervals: List[List[int]], queries: List[int]) -> List[int]:
    h = []
    n = len(intervals)
    intervals.sort(key=lambda p: p[0])
    m = len(queries)
    ans = [-1] * m
    j = 0
    for i, x in sorted(enumerate(queries), key=lambda p: p[1]):
        while j < n and intervals[j][0] <= x:
            heappush(h, (intervals[j][1] - intervals[j][0] + 1, intervals[j][1]))
            j += 1
        while h and h[0][1] < x:
            heappop(h)
        if h:
            ans[i] = h[0][0]
    return ans


# lc1697 检查边长度限制的路径是否存在
def distanceLimitedPathsExist(n: int, edgeList: List[List[int]], queries: List[List[int]]) -> List[bool]:
    m = len(edgeList)
    edgeList.sort(key=lambda p: p[2])
    ans = [False] * len(queries)
    j = 0
    uf = UnionFind(n)
    for i, (x, y, z) in sorted(enumerate(queries), key=lambda p: p[1][2]):
        while j < m and edgeList[j][-1] < z:
            uf.union(edgeList[j][0], edgeList[j][1])
            j += 1

        if uf.connected(x, y):
            ans[i] = True
    return ans


def cf1985E():
    n, m = map(int, input().split())
    h = list(map(int, input().split()))
    g = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        if h[u] >= h[v]:
            g[u].append(v)
        if h[v] >= h[u]:
            g[v].append(u)

    q = int(input())
    queries = []
    for _ in range(q):
        a, b, e = map(int, input().split())
        a -= 1
        b -= 1
        queries.append([a, b, e])
    uf = UnionFind(n)
    ans = [False] * len(queries)
    h_index = []
    for i, x in sorted(enumerate(h), key=lambda p: p[1]):
        h_index.append([i, x])
    j = 0
    for i, (x, y, z) in sorted(enumerate(queries), key=lambda p: p[1][2] + h[p[1][0]]):
        cur = h[x] + z
        while j < n and h_index[j][1] <= cur:
            pre = h_index[j][0]
            for child in g[pre]:
                uf.union(pre, child)
            j += 1

        if uf.connected(x, y):
            ans[i] = True
    for x in ans:
        if x:
            print("YES")
        else:
            print("NO")

    return
