# 最小权边覆盖问题：可转化为最大带权匹配
# 匹配：一条边覆盖两个点
# 额外边：只覆盖一个点
# 边覆盖由匹配和额外边构成
# 求解最小权值匹配：先选择每个节点的最小额外边，然后考虑加入匹配边
# 设左节点Ai,右节点Bj,其额外边代价和匹配边代价分别为cost[i],cost[j],cost[i][j]
# 则引入匹配边后，原先的值减少了 -（cost[i][j]-cost[i]-cost[j]）
# 令w[i][j] = -（cost[i][j]-cost[i]-cost[j]）
# 问题转化在边权为w的情况下的最大权值匹配，原解（选择每个节点的最小额外边）减去这个最大权值匹配就是最小权边覆盖

from math import inf
from typing import List

from AlgorithmsCabin.GraphTheory.BipartiteGraph.WeightedMatching.km import Hungarian


# lc1595 连通两组点点最小成本
def connectTwoGroups(cost: List[List[int]]) -> int:
    n = len(cost)  # n >= m
    m = len(cost[0])
    L_min = [inf] * n
    R_min = [inf] * m

    ans = 0
    for i in range(n):
        for j in range(m):
            L_min[i] = min(L_min[i], cost[i][j])

        ans += L_min[i]

    for j in range(m):
        for i in range(n):
            R_min[j] = min(R_min[j], cost[i][j])
        ans += R_min[j]

    w = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(m):
            w[i][j] = max(-(cost[i][j] - L_min[i] - R_min[j]), 0)

    h = Hungarian(n, w)
    return ans - h.solve()
