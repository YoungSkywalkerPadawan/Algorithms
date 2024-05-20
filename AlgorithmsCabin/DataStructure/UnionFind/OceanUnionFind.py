from typing import List


class OceanUnionFind:
    def __init__(self, grid: List[List[int]]):
        self.m = len(grid)
        self.n = len(grid[0])
        size = self.m * self.n
        self.fa = list(range(size))
        # 当前连通的val值
        self.val = [0] * size
        # 当前连通能达到的边界情况
        self.border = [[0] * 4 for _ in range(size)]
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                self.val[i * self.n + j] = x
                self.border[i * self.n + j] = [j, i, j, i]

    def find(self, x: int) -> int:
        if self.fa[x] != x:
            self.fa[x] = self.find(self.fa[x])
        return self.fa[x]

    def union(self, x: int, y: int) -> None:
        fx = self.find(x)
        fy = self.find(y)
        if self.val[fy] > self.val[fx] or fy == fx:
            return
        l1, u1, r1, d1 = self.border[fx]
        l2, u2, r2, d2 = self.border[fy]
        self.border[fx] = [min(l1, l2), min(u1, u2), max(r1, r2), max(d1, d2)]
        if self.val[fy] == self.val[fx]:
            self.fa[fy] = fx

    def check(self, x: int) -> bool:
        fx = self.find(x)
        l, u, r, d = self.border[fx]
        return (l == 0 or u == 0) and (r == self.n - 1 or d == self.m - 1)
