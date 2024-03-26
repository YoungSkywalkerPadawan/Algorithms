from collections import defaultdict


class DynamicSegmentTree:
    def __init__(self):
        self.tree = defaultdict()

    def update(self, o: int, l: int, r: int, i: int, val: int) -> None:
        if l == r:
            if o not in self.tree.keys():
                self.tree[o] = val
            else:
                self.tree[o] = max(self.tree[o], val)
            return
        m = (l + r) // 2
        if i <= m:
            self.update(o * 2, l, m, i, val)
        else:
            self.update(o * 2 + 1, m + 1, r, i, val)
        if o * 2 not in self.tree.keys():
            self.tree[o * 2] = -1
        if o * 2 + 1 not in self.tree.keys():
            self.tree[o * 2 + 1] = -1
        self.tree[o] = max(self.tree[o * 2], self.tree[o * 2 + 1])

    def query(self, o: int, l: int, r: int, L: int, R: int) -> int:
        if L <= l and r <= R:
            if o not in self.tree.keys():
                self.tree[o] = -1
            return self.tree[o]
        res = -1
        m = (l + r) // 2
        if L <= m:
            res = self.query(o * 2, l, m, L, R)
        if R > m:
            res = max(res, self.query(o * 2 + 1, m + 1, r, L, R))
        return res
