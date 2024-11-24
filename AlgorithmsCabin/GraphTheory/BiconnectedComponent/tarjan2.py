from types import GeneratorType
from typing import List


def bootstrap(f, stack=None):
    if stack is None:
        stack = []

    def wrappedfunc(*args, **kwargs):
        if stack:
            return f(*args, **kwargs)
        else:
            to = f(*args, **kwargs)
            while True:
                if type(to) is GeneratorType:
                    stack.append(to)
                    to = next(to)
                else:
                    stack.pop()
                    if not stack:
                        break
                    to = stack[-1].send(to)
            return to

    return wrappedfunc


class TARJAN2:
    def __init__(self, n: int, g: List[List[int]]):
        # 记录结点的当前时间戳和最早时间戳,dfn 严格递增，low 严格非降
        self.dfn = [0] * n
        self.low = [0] * n
        self.bridge = []  # 桥
        self.flag = [False] * n  # 是否是割点
        self.g = g
        self.n = n
        self.res = []
        self.parent = [-1] * n
        self.t = 0
        self.tarjan(0)

    def find_SCC(self):
        SCC, S, P = [], [], []
        depth = [0] * self.n

        stack = list(range(self.n))
        while stack:
            node = stack.pop()
            if node < 0:
                d = depth[~node] - 1
                if P[-1] > d:
                    SCC.append(S[d:])
                    del S[d:], P[-1]
                    for node in SCC[-1]:
                        depth[node] = -1
            elif depth[node] > 0:
                while P[-1] > depth[node]:
                    P.pop()
            elif depth[node] == 0:
                S.append(node)
                P.append(len(S))
                depth[node] = len(S)
                stack.append(~node)
                stack.extend(self.g[node])
        return SCC[::-1]

    @bootstrap
    def tarjan(self, o: int) -> None:
        if self.dfn[o] > 0:
            yield
        self.t += 1
        self.dfn[o] = self.t
        self.low[o] = self.t
        c = 0
        childs = []
        for child in self.g[o]:
            if child != self.parent[o]:
                if self.dfn[child] == 0:
                    c += 1
                    self.parent[child] = o
                    # yield self.tarjan(child, t + 1)
                    childs.append(child)
                    # self.low[o] = min(self.low[o], self.low[child])
                    # # 找到割点, 非root,有儿子
                    # if self.dfn[o] <= self.low[child] and self.parent[o] != -1 and not self.flag[o]:
                    #     self.flag[o] = True
                    # # 找到桥
                    # if self.dfn[o] < self.low[child]:
                    #     self.bridge.append([o, child])
                else:
                    self.res.append([o, child])
                    self.low[o] = min(self.low[o], self.dfn[child])
        for child in childs:
            yield self.tarjan(child)

        p = self.parent[o]
        if p != -1:
            self.res.append([p, o])
            if self.low[p] > self.low[o]:
                self.low[p] = self.low[o]
            if self.dfn[p] < self.low[o]:  # 割边判定
                self.bridge.append([p, o])
        # root点 儿子数大于等于2
        if self.parent[o] == -1 and c >= 2 and not self.flag[o]:
            self.flag[o] = True
        yield
