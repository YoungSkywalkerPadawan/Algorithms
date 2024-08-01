from collections import defaultdict
from typing import List


class SegmentTree:
    def __init__(self, n: int, nums: List[int]):
        self.sm = [0] * (4 * n)
        self.mx = [0] * (4 * n)
        self.mxIdx = [0] * (4 * n)
        self.ll = [0] * (4 * n)
        self.rr = [0] * (4 * n)
        self.nums = nums
        self.n = n
        self.build(1, 1, n)
        self.dt = defaultdict()

    def update(self, o: int, l: int, val: int, idx: int) -> None:
        if self.ll[o] == self.rr[o] and self.ll[o] == l:
            self.sm[o] = val
            self.mx[o] = val
            self.mxIdx[o] = idx
            return
        m = (self.ll[o] + self.rr[o]) >> 1
        if l <= m:
            self.update(o << 1, l, val, idx)
        else:
            self.update(o << 1 | 1, l, val, idx)
        self.pushup(o)

    def query_max(self, o: int, l: int, r: int) -> int:
        if self.ll[o] >= l and self.rr[o] <= r:
            return self.mx[o]

        res = -1
        m = (self.ll[o] + self.rr[o]) >> 1
        if l <= m:
            res = max(res, self.query_max(o << 1, l, r))
        if m < r:
            res = max(res, self.query_max(o << 1 | 1, l, r))
        return res

    def query_idx(self, o: int, l: int, r: int) -> int:
        if self.ll[o] >= l and self.rr[o] <= r:
            return self.mxIdx[o]

        res = -1
        m = (self.ll[o] + self.rr[o]) >> 1
        if l <= m:
            res = max(res, self.query_idx(o << 1, l, r))
        if m < r:
            res = max(res, self.query_idx(o << 1 | 1, l, r))
        return res

    def query(self, o: int, l: int, r: int) -> int:
        if self.ll[o] >= l and self.rr[o] <= r:
            return self.sm[o]

        res = 0
        m = (self.ll[o] + self.rr[o]) >> 1
        if l <= m:
            res += self.query(o << 1, l, r)
        if m < r:
            res += self.query(o << 1 | 1, l, r)
        return res

    # 初始化线段树   o,l,r=1,1,n
    def build(self, o: int, l: int, r: int) -> None:
        self.ll[o] = l
        self.rr[o] = r
        if l == r:
            self.sm[o] = self.nums[l]
            self.mx[o] = self.nums[l]
            return
        m = (l + r) >> 1
        self.build(o * 2, l, m)
        self.build(o * 2 + 1, m + 1, r)
        self.pushup(o)

    def pushup(self, o) -> None:
        self.sm[o] = self.sm[o << 1] + self.sm[o << 1 | 1]
        self.mx[o] = max(self.mx[o << 1], self.mx[o << 1 | 1])
        self.mxIdx[o] = max(self.mxIdx[o << 1], self.mxIdx[o << 1 | 1])

    def query_ans(self, l: int, r: int) -> int:
        if r - l + 1 < 3:
            return - 1
        mx = self.query_max(1, l, r)
        sm = self.query(1, l, r)
        mxIdx = self.query_idx(1, l, r)
        key = l + "@@" + r
        if sm > 2 * mx:
            self.dt[key] = (mxIdx, r - l + 1)
            return r - l + 1

        if key in self.dt.keys() and self.dt[key][0] == mxIdx:
            return self.dt[key][1]

        L = l
        R = r
        mid = 0
        while L <= R:
            op = (L + R) >> 1
            if self.query_max(1, l, op) == mx:
                R = op - 1
                mid = op
            else:
                L = op + 1
        res = -1
        if mid - 1 >= l:
            res = max(res, self.query_ans(l, mid - 1))
        if mid < r:
            res = max(res, self.query_ans(mid + 1, r))
        self.dt[key] = (mxIdx, res)
        return res
