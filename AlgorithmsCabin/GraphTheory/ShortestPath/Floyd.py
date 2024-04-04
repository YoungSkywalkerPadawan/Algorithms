# Floyd算法: 用来求任意两个结点之间的最短路的。
# 复杂度比较高，但是常数小，容易实现（只有三个 for）。
# 适用于任何图，不管有向无向，边权正负，但是最短路必须存在。（不能有个负环）
# 定义一个数组 f[k][i][j]，表示只允许经过结点 1 到 k（也就是说，在子图 V'={1, 2, ... , k} 中的路径
# 注意，i 与 j 不一定在这个子图中），结点 i 到结点 k 的最短路长度。
# 分类讨论
# 1. 从i到j的最短路中至多为k-1
# 2. 从i到j的最短路至多为k,k是中间节点
# f[k][i][j] = min(f[k-1][i][j],f[k-1][i][k] + f[k-1][k][j])
# f[i][j] = min(f[i][j],f[i][k] + f[k][j])
from math import inf
from typing import List


class FloydGraph:
    def __init__(self, n: int, edges: List[List[int]]):
        f = [[inf] * n for _ in range(n)]
        for i in range(n):
            f[i][i] = 0
        for x, y, w in edges:
            f[x][y] = w  # 添加一条边（题目保证没有重边和自环）
        for k in range(n):
            for i in range(n):
                if f[i][k] == inf:
                    continue
                for j in range(n):
                    f[i][j] = min(f[i][j], f[i][k] + f[k][j])
        self.f = f

    def addEdge(self, edge: List[int]) -> None:
        f = self.f
        x, y, w = edge
        if w >= f[x][y]:  # 无需更新
            return
        n = len(f)
        for i in range(n):
            for j in range(n):
                f[i][j] = min(f[i][j], f[i][x] + w + f[y][j])

    def shortestPath(self, start: int, end: int) -> int:
        ans = self.f[start][end]
        return ans if ans < inf else -1



