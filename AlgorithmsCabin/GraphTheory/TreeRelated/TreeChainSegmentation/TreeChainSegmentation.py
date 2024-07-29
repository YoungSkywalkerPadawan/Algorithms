class TreeChainSegmentation:
    def __init__(self, n, to, nxt, beg, mod, w, r):
        self.cnt = [0] * (n << 1)
        self.todo = [0] * (n << 1)
        self.to = to
        self.nxt = nxt
        self.beg = beg
        self.mod = mod
        self.w = w
        self.r = r
        # 重链剖分
        self.wt = [0] * (n << 1)
        self.son = [0] * n
        self.id = [0] * n
        self.fa = [0] * n
        self.c = 0
        self.dep = [0] * n
        self.siz = [0] * n
        self.top = [0] * n
        self.dfs1(r, 0, 1)
        self.dfs2(r, r)
        self.n = len(w) - 1
        self.build(1, 1, self.n)

    def build(self, o: int, l: int, r: int):
        if l == r:
            self.cnt[o] = self.wt[l] % self.mod
            return
        mid = (l + r) >> 1
        self.build(o << 1, l, mid)
        self.build(o << 1 | 1, mid + 1, r)
        self.maintain(o)

    # 维护区间和
    def maintain(self, o: int) -> None:
        self.cnt[o] = self.cnt[o * 2] + self.cnt[o * 2 + 1]

    def do(self, o: int, val: int, lenn: int) -> None:
        self.cnt[o] += val * lenn
        self.cnt[o] %= self.mod
        self.todo[o] += val

    def spread(self, o: int, lenn: int) -> None:
        v = self.todo[o]
        if v:
            self.do(o * 2, v, lenn - (lenn >> 1))
            self.do(o * 2 + 1, v, lenn >> 1)
            self.todo[o] = 0

    # 区间 [L,R] 内的数都加为val   o,l,r=1,1,n
    def update(self, o: int, l: int, r: int, L: int, R: int, val: int) -> None:
        if L <= l and r <= R:
            self.do(o, val, r - l + 1)
            return
        self.spread(o, r - l + 1)
        m = (l + r) // 2
        if m >= L:
            self.update(o * 2, l, m, L, R, val)
        if m < R:
            self.update(o * 2 + 1, m + 1, r, L, R, val)
        self.maintain(o)

    def query(self, o: int, l: int, r: int, L: int, R: int) -> int:
        if L <= l and r <= R:
            return self.cnt[o] % self.mod
        self.spread(o, r - l + 1)
        m = (l + r) // 2
        res = 0
        if L <= m:
            res += self.query(o * 2, l, m, L, R)
        if m < R:
            res += self.query(o * 2 + 1, m + 1, r, L, R)
        return res % self.mod

    def qRange(self, x: int, y: int) -> int:
        res = 0
        while self.top[x] != self.top[y]:
            if self.dep[self.top[x]] < self.dep[self.top[y]]:
                x, y = y, x
            res += self.query(1, 1, self.n, self.id[self.top[x]], self.id[x])
            res %= self.mod
            x = self.fa[self.top[x]]

        if self.dep[x] > self.dep[y]:
            x, y = y, x
        res += self.query(1, 1, self.n, self.id[x], self.id[y])
        return res % self.mod

    def updRange(self, x: int, y: int, k: int) -> None:
        k %= self.mod
        while self.top[x] != self.top[y]:
            if self.dep[self.top[x]] < self.dep[self.top[y]]:
                x, y = y, x
            self.update(1, 1, self.n, self.id[self.top[x]], self.id[x], k)
            x = self.fa[self.top[x]]
        if self.dep[x] > self.dep[y]:
            x, y = y, x
        self.update(1, 1, self.n, self.id[x], self.id[y], k)

    def qSon(self, x: int) -> int:
        return self.query(1, 1, self.n, self.id[x], self.id[x] + self.siz[x] - 1)

    def updSon(self, x: int, k: int) -> None:
        self.update(1, 1, self.n, self.id[x], self.id[x] + self.siz[x] - 1, k)

    def dfs1(self, x: int, f: int, deep: int) -> None:
        self.dep[x] = deep
        self.fa[x] = f
        self.siz[x] = 1
        maxson = -1
        i = self.beg[x]
        while i > 0:
            y = self.to[i]
            if y != f:
                self.dfs1(y, x, deep + 1)
                self.siz[x] += self.siz[y]
                if self.siz[y] > maxson:
                    maxson = self.siz[y]
                    self.son[x] = y
            i = self.nxt[i]

    def dfs2(self, x: int, topf: int) -> None:
        self.c += 1
        self.id[x] = self.c
        self.wt[self.c] = self.w[x]
        self.top[x] = topf
        if self.son[x] == 0:
            return
        self.dfs2(self.son[x], topf)
        i = self.beg[x]
        while i > 0:
            y = self.to[i]
            if y != self.fa[x] and y != self.son[x]:
                self.dfs2(y, y)
            i = self.nxt[i]
