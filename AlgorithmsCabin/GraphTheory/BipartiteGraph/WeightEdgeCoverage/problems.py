from math import inf
from typing import List

from AlgorithmsCabin.GraphTheory.BipartiteGraph.WeightedMatching.km import Hungarian


# lc1595 连通两组点点最小成本
def connectTwoGroups(cost: List[List[int]]) -> int:
    m = len(cost)
    n = len(cost[0])
    L_min = [inf] * m
    R_min = [inf] * n

    ans = 0
    for i in range(m):
        for j in range(n):
            L_min[i] = min(L_min[i], cost[i][j])

        ans += L_min[i]

    for j in range(n):
        for i in range(m):
            R_min[j] = min(R_min[j], cost[i][j])
        ans += R_min[j]

    h = Hungarian(m, n, L_min, R_min, cost)
    return ans - h.solve()
