# dijstra 算法
# 解决没有负边权的有向图的单源最短路，也可用于多源最短路（跑多次dijstra算法）
# 1.设dis[x] 表示从起点到x的最短路，设y -> x，考虑所有y，当更新dis[x]的时候，如果dis[y]已经算好了，那么dis[x]一定可以正确地算出来
# 2.怎么保证算出来的一定是最短路？ 使用数学归纳法
# 一开始只有一个起点st dis[st] = 0， 从st 开始，把st的邻居dis[]都更新(此时不一定是算好的)
# 从没有算好的dis里面，去一个最小的 >> 这个取出来的一定是算好的
import heapq
from collections import defaultdict
from math import inf
from typing import List


# lc2662 前往目标的最小代价
def minimumCost(start: List[int], target: List[int], specialRoads: List[List[int]]) -> int:
    # dijstra算法
    dist = {}  # 本次dijstra统计的距离
    q = [(0, start[0], start[1])]
    # 初始化除起点外所有节点为无穷大
    unvisited_nodes = {}
    for x0, y0, x1, y1, cost in specialRoads:
        unvisited_nodes[(x1, y1)] = float("inf")
    unvisited_nodes[tuple(start)] = 0
    unvisited_nodes[tuple(target)] = float("inf")
    seen = set()

    # 开始最小路径搜索
    while unvisited_nodes:
        current_distance, x, y = heapq.heappop(q)
        if (x, y) in seen:
            continue
        seen.add((x, y))
        # 先更新终点
        if (x, y) != tuple(target):
            if current_distance + target[0] - x + target[1] - y < unvisited_nodes[tuple(target)]:
                unvisited_nodes[tuple(target)] = current_distance + target[0] - x + target[1] - y
                heapq.heappush(q, (current_distance + target[0] - x + target[1] - y, target[0], target[1]))
        else:
            dist[tuple(target)] = current_distance
            break

        dist[(x, y)] = current_distance
        unvisited_nodes.pop((x, y))
        for x0, y0, x1, y1, cost in specialRoads:
            if (x1, y1) not in unvisited_nodes:
                continue
            new_distance = current_distance + abs(x0 - x) + abs(y0 - y) + cost
            if new_distance < unvisited_nodes[(x1, y1)]:
                unvisited_nodes[(x1, y1)] = new_distance
                heapq.heappush(q, (new_distance, x1, y1))
            # dist[nx * n + ny] = max(d, abs(heights[x][y] - heights[nx][ny]))
    return dist[tuple(target)]


# lc2976 转换字符串的最小成本
def minimumChangeCost(source: str, target: str, original: List[str], changed: List[str], cost: List[int]) -> int:
    # 先建图,有向图（26个字母映射到0-25）
    g = [[] for _ in range(26)]
    dt = defaultdict()
    for i, x_o in enumerate(original):
        y_c = changed[i]
        c = cost[i]
        x0 = ord(x_o) - ord('a')
        y0 = ord(y_c) - ord('a')
        if (x0, y0) not in dt.keys():
            dt[(x0, y0)] = c
            g[x0].append(y0)
        else:
            dt[(x0, y0)] = min(c, dt[(x0, y0)])

    # 运行dijstra 算法，统计所有点（26个字母）能到达的其他点的最短距离
    final_dt = defaultdict()

    # dijstra算法 统计x能到达的所有点点最短距路
    def dfs(x: int) -> None:
        dist = {}  # 本次dijstra统计的距离，后续加到final_dt中
        unvisited_nodes = {}  # 先用广度优先搜索将x能达到的点初始化到inf
        q = [(0, x, x)]
        vis = [0] * 26
        cur = [x]
        vis[x] = 1
        while cur:
            pre = cur
            cur = []
            for el in pre:
                for y in g[el]:
                    if vis[y] == 0:
                        unvisited_nodes[(x, y)] = inf
                        vis[y] = 1
                        cur.append(y)
        # 开始最小路径搜索
        unvisited_nodes[(x, x)] = 0
        seen = set()
        # 使用 dijstra算法计算达到各点的最短值
        while unvisited_nodes:
            current_distance, x1, y1 = heapq.heappop(q)
            if y1 in seen:
                continue
            seen.add(y1)
            for el in g[y1]:
                if (x, el) not in unvisited_nodes:
                    continue
                new_distance = current_distance + dt[(y1, el)]
                if new_distance < unvisited_nodes[(x, el)]:
                    unvisited_nodes[(x, el)] = new_distance
                    heapq.heappush(q, (new_distance, x, el))
            dist[(x, y1)] = current_distance
            unvisited_nodes.pop((x, y1))
        for k, v in dist.items():
            final_dt[k] = v

    # 对每个字母运行dijstra算法
    for i in range(26):
        dfs(i)
    ans = 0
    # 统计完，开始对每个字母改变计算答案，如果达不到，返回-1
    for i, x_s in enumerate(source):
        x0 = ord(x_s) - ord('a')
        y0 = ord(target[i]) - ord('a')
        if x0 != y0:
            if (x0, y0) not in final_dt.keys():
                return - 1
            else:
                ans += final_dt[(x0, y0)]
    return ans
