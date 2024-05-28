from typing import List


class LazySegmentTree:
    def __init__(self, n: int):
        self.cnt = [0] * (4 * n)
        self.todo = [0] * (4 * n)

    # 初始化线段树   o,l,r=1,1,n
    def build(self, o: int, l: int, r: int, nums: List[int]) -> None:
        if l == r:
            self.cnt[o] = nums[l - 1]
            return
        m = (l + r) // 2
        self.build(o * 2, l, m, nums)
        self.build(o * 2 + 1, m + 1, r, nums)
        self.maintain(o)

    # 维护区间 1 的个数
    def maintain(self, o: int) -> None:
        self.cnt[o] = self.cnt[o * 2] + self.cnt[o * 2 + 1]

    def do(self, o: int, l: int, r: int) -> None:
        self.cnt[o] = r - l + 1 - self.cnt[o]
        self.todo[o] = 1 if self.todo[o] == 0 else 0

    def spread(self, o: int, l: int, r: int) -> None:
        v = self.todo[o]
        if v:
            m = (l + r) // 2
            self.do(o * 2, l, m)
            self.do(o * 2 + 1, m + 1, r)
            self.todo[o] = 0

    # 区间 [L,R] 内的数都加上 v   o,l,r=1,1,n
    def update(self, o: int, l: int, r: int, L: int, R: int) -> None:
        if L <= l and r <= R:
            self.do(o, l, r)
            return
        self.spread(o, l, r)
        m = (l + r) // 2
        if m >= L:
            self.update(o * 2, l, m, L, R)
        if m < R:
            self.update(o * 2 + 1, m + 1, r, L, R)
        self.cnt[o] = self.cnt[o * 2] + self.cnt[o * 2 + 1]

    def query(self, o: int, l: int, r: int, L: int, R: int) -> int:
        if L <= l and r <= R:
            return self.cnt[o]
        self.spread(o, l, r)
        m = (l + r) // 2
        res = 0
        if L <= m:
            res = self.query(o * 2, l, m, L, R)
        if m < R:
            res = max(res, self.query(o * 2 + 1, m + 1, r, L, R))
        return res
