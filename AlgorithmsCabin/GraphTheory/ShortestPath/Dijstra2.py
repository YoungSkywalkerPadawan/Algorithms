# dijstra算法模板改进版
from heapq import heappop, heappush
from math import inf
from typing import List


def dijstra(n: int, edges: List[List[int]], start: int) -> List[int]:
    g = [[] for _ in range(n)]  # 稀疏图用邻接表
    for i, (x, y, wt) in enumerate(edges):
        g[x].append((y, wt))
        g[y].append((x, wt))
    dis = [inf] * n
    dis[start] = 0
    h = [(0, start)]
    while h:
        dx, x = heappop(h)
        if dx > dis[x]:  # x 之前出堆过
            continue
        for y, wt in g[x]:
            new_dis = dx + wt
            if new_dis < dis[y]:
                dis[y] = new_dis  # 更新 x 的邻居的最短路
                heappush(h, (new_dis, y))
    return dis
