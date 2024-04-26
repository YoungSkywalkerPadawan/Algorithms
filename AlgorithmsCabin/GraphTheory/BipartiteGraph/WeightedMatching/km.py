from math import inf
from typing import List


class Hungarian:
    def __init__(self, m: int, n: int, L_min: List[int], R_min: List[int], cost: List[List[int]]):
        self.n = max(m, n)
        self.lx = [0] * self.n
        self.ly = [0] * self.n
        self.vx = [False] * self.n
        self.vy = [False] * self.n
        self.slack = [inf] * self.n
        self.matchy = [-1] * self.n
        self.edges = [[0] * self.n for _ in range(self.n)]
        self.res = 0
        for i in range(m):
            for j in range(n):
                self.edges[i][j] = max(-(cost[i][j] - L_min[i] - R_min[j]), 0)
        for i in range(self.n):
            for j in range(self.n):
                self.lx[i] = max(self.lx[i], self.edges[i][j])

    def match(self, x: int) -> bool:
        self.vx[x] = True
        for y in range(self.n):
            if self.vy[y]:
                continue
            delta = self.lx[x] + self.ly[y] - self.edges[x][y]
            if delta == 0:
                self.vy[y] = True
                if self.matchy[y] == -1 or self.match(self.matchy[y]):
                    self.matchy[y] = x
                    return True
            else:
                self.slack[y] = min(self.slack[y], delta)
        return False

    def updateLabels(self) -> None:
        delta = inf
        for y in range(self.n):
            if not self.vy[y]:
                delta = min(delta, self.slack[y])

        for x in range(self.n):
            if self.vx[x]:
                self.lx[x] -= delta
        for y in range(self.n):
            if self.vy[y]:
                self.ly[y] += delta
            else:
                self.slack[y] -= delta

    def solve(self) -> int:
        for i in range(self.n):
            self.slack = [inf] * self.n
            while True:
                self.vx = [False] * self.n
                self.vy = [False] * self.n
                if self.match(i):
                    break
                self.updateLabels()

        for y in range(self.n):
            # if self.matchy[y] != -1:
            self.res += self.lx[self.matchy[y]] + self.ly[y]
        return self.res
