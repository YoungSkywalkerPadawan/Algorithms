class LazySegmentTree:
    def __init__(self, n: int):
        self.cnt = [0] * (4 * n)
        self.tomul = [1] * (4 * n)
        self.todo = [0] * (4 * n)
        self.mod = 10 ** 9 + 7

    # 维护区间和
    def maintain(self, o: int) -> None:
        self.cnt[o] = self.cnt[o * 2] + self.cnt[o * 2 + 1]

    # 进行区间求和
    def doSum(self, o: int, l: int, r: int, val: int) -> None:
        self.cnt[o] += (r - l + 1) * val
        self.cnt[o] %= self.mod
        self.todo[o] += val
        self.todo[o] %= self.mod

    # 进行区间求积，注意更改mul标签时需将add标签乘上mul 标签
    def doMul(self, o: int, val: int) -> None:
        self.cnt[o] *= val
        self.cnt[o] %= self.mod
        self.todo[o] *= val
        self.todo[o] %= self.mod
        self.tomul[o] *= val
        self.tomul[o] %= self.mod

    # 先乘再加
    def spread(self, o: int, l: int, r: int) -> None:
        v = self.tomul[o]
        if v > 1:
            self.doMul(o * 2, v)
            self.doMul(o * 2 + 1, v)
            self.tomul[o] = 1
        v = self.todo[o]
        if v:
            m = (l + r) // 2
            self.doSum(o * 2, l, m, v)
            self.doSum(o * 2 + 1, m + 1, r, v)
            self.todo[o] = 0

    # 区间 [L,R] 内的数都加上 val   o,l,r=1,1,n
    def update(self, o: int, l: int, r: int, L: int, R: int, val: int) -> None:
        if L <= l and r <= R:
            self.doSum(o, l, r, val)
            return
        self.spread(o, l, r)
        m = (l + r) // 2
        if m >= L:
            self.update(o * 2, l, m, L, R, val)
        if m < R:
            self.update(o * 2 + 1, m + 1, r, L, R, val)
        self.maintain(o)

    # 区间 [L,R] 内的数都乘上 val   o,l,r=1,1,n
    def update2(self, o: int, l: int, r: int, L: int, R: int, val: int) -> None:
        if L <= l and r <= R:
            self.doMul(o, val)
            return
        self.spread(o, l, r)
        m = (l + r) // 2
        if m >= L:
            self.update2(o * 2, l, m, L, R, val)
        if m < R:
            self.update2(o * 2 + 1, m + 1, r, L, R, val)
        self.maintain(o)

    def query(self, o: int, l: int, r: int, L: int, R: int) -> int:
        if L <= l and r <= R:
            return self.cnt[o]
        self.spread(o, l, r)
        m = (l + r) // 2
        res = 0
        if L <= m:
            res = self.query(o * 2, l, m, L, R)
        if m < R:
            res += self.query(o * 2 + 1, m + 1, r, L, R)
        return res % self.mod
