from collections import defaultdict


class DynamicSegmentTree:
    def __init__(self):
        self.cnt = defaultdict(int)
        self.todo = defaultdict(int)

    # 维护区间最大值
    def maintain(self, o: int) -> None:
        self.cnt[o] = max(self.cnt[o * 2], self.cnt[o * 2 + 1])

    def do(self, o: int, val: int) -> None:
        self.cnt[o] = max(self.cnt[o], val)
        self.todo[o] = max(self.todo[o], val)

    def spread(self, o: int) -> None:
        v = self.todo[o]
        if v:
            self.do(o * 2, v)
            self.do(o * 2 + 1, v)
            self.todo[o] = 0

    # 区间 [L,R] 内的数都更新为val   o,l,r=1,1,n
    def update(self, o: int, l: int, r: int, L: int, R: int, val: int) -> None:
        if L <= l and r <= R:
            self.do(o, val)
            return
        self.spread(o)
        m = (l + r) // 2
        if m >= L:
            self.update(o * 2, l, m, L, R, val)
        if m < R:
            self.update(o * 2 + 1, m + 1, r, L, R, val)
        self.maintain(o)

    def query(self, o: int, l: int, r: int, L: int, R: int) -> int:
        if L <= l and r <= R:
            return self.cnt[o]
        self.spread(o)
        m = (l + r) // 2
        res = 0
        if L <= m:
            res = self.query(o * 2, l, m, L, R)
        if m < R:
            res = max(res, self.query(o * 2 + 1, m + 1, r, L, R))
        return res
