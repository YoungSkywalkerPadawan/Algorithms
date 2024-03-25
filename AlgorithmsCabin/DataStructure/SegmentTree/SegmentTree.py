class SegmentTree:
    def __init__(self, n: int):
        self.tree = [0] * (4 * n)

    def update(self, o: int, l: int, r: int, i: int, val: int) -> None:
        if l == r:
            self.tree[o] = val
            return
        m = (l + r) // 2
        if i <= m:
            self.update(o * 2, l, m, i, val)
        else:
            self.update(o * 2 + 1, m + 1, r, i, val)
        self.tree[o] = max(self.tree[o * 2], self.tree[o * 2 + 1])

    def query(self, o: int, l: int, r: int, L: int, R: int) -> int:
        if L <= l and r <= R: return self.tree[o]
        res = 0
        m = (l + r) // 2
        if L <= m: res = self.query(o * 2, l, m, L, R)
        if R > m: res = max(res, self.query(o * 2 + 1, m + 1, r, L, R))
        return res
