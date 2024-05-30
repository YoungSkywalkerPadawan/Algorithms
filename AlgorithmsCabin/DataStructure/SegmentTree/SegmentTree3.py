from typing import List


class SegmentTree:
    def __init__(self, n: int, nums: List[int]):
        self.cnt = [0] * (4 * n)
        self.index = [0] * (4 * n)
        self.nums = nums

    def update(self, o: int, l: int, r: int, i: int, val: int) -> None:
        if l == r:
            self.cnt[o] = val
            return
        m = (l + r) // 2
        if i <= m:
            self.update(o * 2, l, m, i, val)
        else:
            self.update(o * 2 + 1, m + 1, r, i, val)
        self.cnt[o] = max(self.cnt[o * 2], self.cnt[o * 2 + 1])

    def query(self, o: int, l: int, r: int, L: int, R: int) -> int:
        if L <= l and r <= R:
            return self.cnt[o]
        res = 0
        m = (l + r) // 2
        if L <= m:
            res = self.query(o * 2, l, m, L, R)
        if R > m:
            res = max(res, self.query(o * 2 + 1, m + 1, r, L, R))
        return res

    # 查询区间[L:]值为v的最小下标
    def BinaryQuery(self, o: int, l: int, r: int, L: int, v: int) -> int:
        if self.cnt[o] == 0:
            return -1
        if l == r:
            return self.index[o] if self.cnt[o] == v else -1
        m = (l + r) // 2
        if L <= m:
            res = self.BinaryQuery(o * 2, l, m, L, v)
            if res >= 0:
                return res
        return self.BinaryQuery(o * 2 + 1, m + 1, r, L, v)

    # 查询区间[:R]值为v的最小下标
    def BinaryQuery2(self, o: int, l: int, r: int, R: int, v: int) -> int:
        if self.cnt[o] == 0:
            return -1
        if l == r:
            return self.index[o] if self.cnt[o] == v else -1
        m = (l + r) // 2
        res = self.BinaryQuery2(o * 2, l, m, R, v)
        if res >= 0:
            return res
        if R > m:
            return self.BinaryQuery2(o * 2 + 1, m + 1, r, R, v)

    # 初始化线段树   o,l,r=1,1,n
    def build(self, o: int, l: int, r: int) -> None:
        if l == r:
            self.index[o] = self.nums[l - 1]
            return
        m = (l + r) // 2
        self.build(o * 2, l, m)
        self.build(o * 2 + 1, m + 1, r)
