# 二分图带权匹配：给定一张二分图，图的每条边都有一个权值，求该图的一组最大匹配，使得匹配边的权值最大
# 完备匹配：给定一张二分图，其左，右部节点数相同，均为N，若该图的最大匹配包括N条匹配边，则该图具有完备匹配
# KM算法：求解二分图带权匹配，必须要求带权最大匹配是完备匹配
# 交错树：匈牙利算法中，从某个左部节点出发寻找匹配失败，在dfs过程中，所有访问过的节点，以及这些节点经过的边，构成交错树
# 顶标：二分图中，给第i(1<=i<=N)个左部节点一个整数值Ai,第j(1<=j<=N)个右部节点一个整数值Bj。同时满足任意i,j使得Ai+Bj>=w(i,j)
# w(i,j)为第i个左部节点和第j个右部节点之间的边权（没有为-inf）,这些Ai,bj为顶标
# 相等子图：二分图中所有节点满足Ai+Bj=w(i,j) 构成的子图
# 若相等子图中存在完备匹配，则完备匹配是二分图的最大带权匹配

# KM算法思想：在满足任意i,j使得Ai+Bj>=w(i,j)前提下，给每个节点随意赋一个顶标，采取适当策略不断扩大相等子图规模，直到相等子图存在完备匹配
# 初始化时可以令Ai = max(w(i,j)) (1<=j<=N),Bj = 0
# 对于一个相等子图，利用匈牙利算法求它的最大匹配，若匹配不完备，则一定有一个左节点匹配失败，节点失败的那次dfs构成交错树

# 如何使左部节点沿着非匹配边访问更多右部节点？
# 对交错树T中所有左部节点顶标Ai(i属于T)减小delta， T中所有右部节点顶标Bj(j属于T)增大delta

# 节点访问情况变化
# 1. 右部节点j沿着匹配边，递归访问i=match[j]，对于匹配边,（i,j属于T）被访问到，或者（i,j不属于T），Ai+Bj不变，匹配边都是相等子图
# 2.左部节点沿着非匹配边访问右部节点j, 若（i,j属于T）Ai+Bj不变，若j不属于T，Ai+Bj减小，从前i访问不到的j可以访问到了

# 在保证顶标满足任意i,j使得Ai+Bj>=w(i,j)情况下，找到所有i属于T，j不属于T的边，找出最小的（Ai+Bj-w(i,j)）作为delta
# 不断重复上述过程，直到相等子图完备


from math import inf
from typing import List


class Hungarian:
    def __init__(self, n: int, w: List[List[int]]):
        self.n = n
        self.lx = [0] * n
        self.ly = [0] * n  # 顶标
        self.vx = [False] * n
        self.vy = [False] * n  # 访问标记，是否在交错树中
        self.upd = [inf] * n
        self.match = [-1] * n  # 右部点匹配了哪个左部点
        self.w = w  # 边权
        self.ans = 0
        for i in range(n):
            for j in range(n):
                self.lx[i] = max(self.lx[i], w[i][j])

    def dfs(self, x: int) -> bool:
        self.vx[x] = True
        for y in range(self.n):
            if self.vy[y]:
                continue
            delta = self.lx[x] + self.ly[y] - self.w[x][y]
            if delta == 0:
                self.vy[y] = True
                if self.match[y] == -1 or self.dfs(self.match[y]):
                    self.match[y] = x
                    return True
            else:
                self.upd[y] = min(self.upd[y], delta)
        return False

    def updateLabels(self) -> None:
        delta = inf
        for y in range(self.n):
            if not self.vy[y]:
                delta = min(delta, self.upd[y])

        for i in range(self.n):
            if self.vx[i]:
                self.lx[i] -= delta
            if self.vy[i]:
                self.ly[i] += delta

    def solve(self) -> int:
        for i in range(self.n):
            self.upd = [inf] * self.n
            while True:
                self.vx = [False] * self.n
                self.vy = [False] * self.n
                if self.dfs(i):
                    break
                self.updateLabels()

        for y in range(self.n):
            self.ans += self.lx[self.match[y]] + self.ly[y]
        return self.ans
