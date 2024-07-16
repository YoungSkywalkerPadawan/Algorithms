from heapq import heappop, heappush
from math import inf
from typing import List


def dijstra(n: int, g: List[List[int]], start: int):
    dis = [[inf] * 2 for _ in range(n)]
    dis[start] = [0, 0]
    h = [(0, start, 0)]
    while h:
        dx, x, curFlag = heappop(h)
        if dx > dis[x][curFlag]:  # x 之前出堆过
            continue
        for y, wt, targetFlag in g[x]:
            new_dis = dx + wt
            if new_dis < dis[y][targetFlag] and (targetFlag == 1 or curFlag == 0):
                dis[y][targetFlag] = new_dis  # 更新 x 的邻居的最短路
                heappush(h, (new_dis, y, targetFlag))
    return dis


def cf1725M():
    n, m = map(int, input().split())
    g = [[] for _ in range(n)]
    for _ in range(m):
        x, y, w = map(int, input().split())
        x -= 1
        y -= 1
        g[x].append((y, w, 0))
        g[y].append((x, w, 1))  # 反边
    dis = dijstra(n, g, 0)
    ans = [-1] * (n - 1)
    for i in range(1, n):
        if min(dis[i]) < inf:
            ans[i - 1] = min(dis[i])
    print(*ans)
    return
