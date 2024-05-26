# 能否分治解决不带修改的版本？
# 能 => 线段树动态维护带修改的版本
from typing import List


class SegmentTree:
    def __init__(self, n: int, nums: List[int]):
        self.f00 = [0] * (2 << n.bit_length())
        self.f01 = [0] * (2 << n.bit_length())
        self.f10 = [0] * (2 << n.bit_length())
        self.f11 = [0] * (2 << n.bit_length())
        self.nums = nums

    # 初始化线段树   o,l,r=1,1,n
    def build(self, o: int, l: int, r: int) -> None:
        if l == r:
            self.f11[o] = max(self.nums[l - 1], 0)
            return
        m = (l + r) // 2
        self.build(o * 2, l, m)
        self.build(o * 2 + 1, m + 1, r)
        self.maintain(o)

    def maintain(self, o: int) -> None:
        self.f11[o] = max(self.f10[o * 2] + self.f11[o * 2 + 1], self.f11[o * 2] + self.f01[o * 2 + 1])
        self.f10[o] = max(self.f10[o * 2] + self.f10[o * 2 + 1], self.f11[o * 2] + self.f00[o * 2 + 1])
        self.f01[o] = max(self.f00[o * 2] + self.f11[o * 2 + 1], self.f01[o * 2] + self.f01[o * 2 + 1])
        self.f00[o] = max(self.f00[o * 2] + self.f10[o * 2 + 1], self.f01[o * 2] + self.f00[o * 2 + 1])

    def update(self, o: int, l: int, r: int, i: int, val: int) -> None:
        if l == r:
            self.f11[o] = max(val, 0)
            return
        m = (l + r) // 2
        if i <= m:
            self.update(o * 2, l, m, i, val)
        else:
            self.update(o * 2 + 1, m + 1, r, i, val)
        self.maintain(o)

    def query(self, o: int, l: int, r: int, L: int, R: int) -> int:
        if L <= l and r <= R:
            return self.f11[o]
        res = 0
        m = (l + r) // 2
        if L <= m:
            res = self.query(o * 2, l, m, L, R)
        if R > m:
            res = max(res, self.query(o * 2 + 1, m + 1, r, L, R))
        return res
