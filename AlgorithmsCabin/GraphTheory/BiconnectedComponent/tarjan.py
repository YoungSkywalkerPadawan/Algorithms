# 割点和桥
# 对于一个无向图，如果把一个点删除后这个图的极大连通分量数增加了，那么这个点就是这个图的割点（又称割顶）。
# 割边/桥
# 对于一个无向图，如果删掉一条边后图中的连通分量数增加了，则称这条边为桥或者割边。
# 严谨来说，就是：假设有连通图 G={V,E}，e 是其中一条边，如果 G-e 是不连通的，则边 e 是图 G 的一条割边（桥）。

# 双连通分量
# 在一张连通的无向图中，对于两个点 u 和 v，如果无论删去哪条边（只能删去一条）都不能使它们不连通，我们就说 u 和 v 边双连通。
# 在一张连通的无向图中，对于两个点 u 和 v，如果无论删去哪个点（只能删去一个，且不能删 u 和 v 自己）都不能使它们不连通，我们就说 u 和 v 点双连通。
# 边双连通具有传递性，即，若 x,y 边双连通，y,z 边双连通，则 x,z 边双连通。
# 点双连通 不 具有传递性，反例如下图，A,B 点双连通，B,C 点双连通，而 A,C 不 点双连通。

# tarjan算法
# dfn(u) 深度优先搜索遍历时结点 u 被搜索的次序。
# low(u) 在 u 的子树中能够回溯到的最早的已经在栈中的结点。设以 u 为根的子树为Subtree。low(u) 定义为以下结点的dfn的最小值：
# Subtree中的结点；从 Subtree 通过一条不在搜索树上的边能到达的结点。
# 一个结点的子树内结点的 dfn 都大于该结点的 dfn。
# 从根开始的一条路径上的 dfn 严格递增，low 严格非降。
# tarjan 求割点和桥
# x 是割点
# case1. 非root节点 && 有儿子 && low(x的儿子) >= dfn(x)
# case2. root节点 && 有大于等于2个儿子
# x - y 是桥：low(x的儿子) > dfn(x)
from typing import List


class TARJAN:
    def __init__(self, n: int, g: List[List[int]]):
        # 记录结点的当前时间戳和最早时间戳,dfn 严格递增，low 严格非降
        self.dfn = [-1] * n
        self.low = [-1] * n
        self.bridge = []  # 桥
        self.flag = [False] * n  # 是否是割点
        self.g = g

    def tarjan(self, o: int, f: int, t: int) -> None:
        self.dfn[o] = t
        self.low[o] = t
        c = 0
        for child in self.g[o]:
            if child != f:
                if self.dfn[child] == -1:
                    c += 1
                    self.tarjan(child, o, t + 1)
                    self.low[o] = min(self.low[o], self.low[child])
                    # 找到割点, 非root,有儿子
                    if self.dfn[o] <= self.low[child] and f != -1 and not self.flag[o]:
                        self.flag[o] = True
                    # 找到桥
                    if self.dfn[o] < self.low[child]:
                        self.bridge.append([o, child])
                else:
                    self.low[o] = min(self.low[o], self.dfn[child])
        # root点 儿子数大于等于2
        if f == -1 and c >= 2 and not self.flag[o]:
            self.flag[o] = True
