# dijstra算法模板改进版
from heapq import heappop, heappush
from math import inf
from typing import List

MOD = 10 ** 9 + 7


def dijstra(n: int, g: List[List[int]], start: int) -> List[int]:
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


# 字典序最短路
def dijstraForDic(n: int, g: List[List[tuple]]):
    dis = [0] * n
    vis = [False] * n
    vis[0] = True
    cur = [[0]]
    while cur:
        pre = cur
        cur = []
        for vs in pre:
            nxt = [[] for _ in range(10)]
            for v in vs:
                for e in g[v]:
                    nxt[e[1]].append((v, e[0]))

            for wt, es in enumerate(nxt):
                vs = []
                for e in es:
                    w = e[1]
                    if not vis[w]:
                        vis[w] = True
                        dis[w] = (dis[e[0]] * 10 + wt) % MOD
                        vs.append(w)
                if vs:
                    cur.append(vs)
    return dis
