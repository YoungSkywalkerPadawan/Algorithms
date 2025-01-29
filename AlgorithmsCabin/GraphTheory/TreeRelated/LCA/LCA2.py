class LCA:
    def __init__(self, n):
        # g[v]: (cost, u)
        self.n = n
        self.num = n.bit_length()
        self.depth = [0] * n
        self.parent = [[-1] * n for _ in range(self.num)]
        self.g = [[] for _ in range(n)]
        self.t_in = [0] * n
        self.t_out = [0] * n
        self.cur = 0

    def addEdge(self, u, v):
        self.g[u].append(v)
        self.g[v].append(u)

    def work(self):
        dq = [0]

        while dq:
            u = dq.pop()
            if u >= 0:
                self.cur += 1
                self.t_in[u] = self.cur
                dq.append(~u)
                for v in self.g[u]:
                    if self.parent[0][u] != v:
                        self.parent[0][v] = u
                        self.depth[v] = self.depth[u] + 1
                        dq.append(v)
            else:
                self.t_out[~u] = self.cur

        for k in range(self.num - 1):
            for v in range(self.n):
                if self.parent[k][v] == -1:
                    self.parent[k + 1][v] = -1
                else:
                    self.parent[k + 1][v] = self.parent[k][self.parent[k][v]]

    def getLCA(self, u, v):
        if self.depth[u] > self.depth[v]:
            u, v = v, u
        for k in range(self.num):
            if ((self.depth[v] - self.depth[u]) >> k) & 1:
                v = self.parent[k][v]
        if u == v:
            return u

        for k in reversed(range(self.num)):
            if self.parent[k][u] != self.parent[k][v]:
                u = self.parent[k][u]
                v = self.parent[k][v]
        return self.parent[0][u]

    def is_ancestor(self, u: int, v: int) -> bool:
        return self.t_in[u] <= self.t_in[v] <= self.t_out[u]

    def search(self, v, x):
        for k in reversed(range(self.num)):
            if x >> k & 1:
                v = self.parent[k][v]
        return v

    def getDis(self, u, v):
        return self.depth[u] + self.depth[v] - self.depth[self.getLCA(u, v)] * 2

    def addNode(self, cur, v):
        self.parent[0][cur] = v
        self.depth[cur] = self.depth[v] + 1
        for k in range(self.num - 1):
            if self.parent[k][cur] == -1:
                self.parent[k + 1][cur] = -1
            else:
                self.parent[k + 1][cur] = self.parent[k][self.parent[k][cur]]