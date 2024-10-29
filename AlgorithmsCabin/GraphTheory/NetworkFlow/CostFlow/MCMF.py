# 费用流
# 一个网络 G = (V, E), 每条边(x,y)除了c(x,y)的容量限制，还有给定的单位费用w(x,y)
# 当边流量为f(x,y)时，要花费f(x,y) * w(x, y)的费用
# 最小费用最大流：网络中花费最小的最大流
# 最大费用最大流：网络中花费最大的最大流
# 费用流的前提时最大流，其次才考虑费用
# 例子： 二分图带权最大匹配可用最大费用最大流解决

# Edmonds-Karp增广路算法
# 在求解最大流的基础上，用SPFA算法找一条单位费用之和最小的增广路
from collections import deque
from math import inf
from typing import List


class MCMF:
    def __init__(self, N: int, M: int, s: int, t: int, ver: List[int], edge: List[int], cost: List[int],
                 Next: List[int], head: List[int]):
        self.N = N
        self.M = M
        self.ver = ver
        self.edge = edge
        self.cost = cost
        self.Next = Next
        self.head = head
        self.d = [-inf] * N
        self.incf = [0] * N
        self.pre = [0] * N
        self.v = [False] * N
        self.ans = 0
        self.maxflow = 0
        self.s = s
        self.t = t

    def spfa(self) -> bool:
        q = deque()
        for i in range(self.N):
            self.d[i] = -inf
        self.v = [False] * self.N
        q.append(self.s)
        self.d[self.s] = 0
        self.v[self.s] = True
        self.incf[self.s] = inf  # 增广路上各边的剩余容量
        # spfa求最长路
        while q:
            x = q.popleft()
            i = self.head[x]
            self.v[x] = False
            while i > 0:
                if self.edge[i] > 0:
                    y = self.ver[i]
                    if self.d[y] < self.d[x] + self.cost[i]:
                        self.d[y] = self.d[x] + self.cost[i]
                        self.incf[y] = min(self.incf[x], self.edge[i])
                        self.pre[y] = i  # 记录前驱，便于找到最长路的实际方案
                        if not self.v[y]:
                            self.v[y] = True
                            q.append(y)
                i = self.Next[i]
        return self.d[self.t] > -inf  # 看汇点可不可达，不可达说明已经求出最大流

    # 更新最长增广路及其反向边的剩余容量
    def update(self) -> None:
        x = self.t
        while x != self.s:
            i = self.pre[x]
            self.edge[i] -= self.incf[self.t]
            self.edge[i ^ 1] += self.incf[self.t]  # 利用成对存储的xor 1技巧
            x = self.ver[i ^ 1]
        self.maxflow += self.incf[self.t]

        self.ans += self.d[self.t] * self.incf[self.t]

    # 计算最大费用最大流
    def solve(self) -> tuple:
        while True:
            if self.spfa():
                self.update()
            else:
                break

        return self.maxflow, self.ans
