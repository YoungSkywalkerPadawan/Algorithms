from typing import List

INF = 10 ** 9 + 1


class BinarySegmentTree:
    def __init__(self, n: int, nums: List[int]):
        self.mx = [-INF] * (4 * n)  # 最大值
        self.mn = [INF] * (4 * n)  # 最小值
        self.nums = nums

    def update(self, o: int, l: int, r: int, i: int, val: int) -> None:
        if l == r:
            self.mx[o] = val
            self.mn[o] = val
            return
        m = (l + r) // 2
        if i <= m:
            self.update(o * 2, l, m, i, val)
        else:
            self.update(o * 2 + 1, m + 1, r, i, val)
        self.mx[o] = max(self.mx[o * 2], self.mx[o * 2 + 1])
        self.mn[o] = min(self.mn[o * 2], self.mn[o * 2 + 1])

    def queryMx(self, o: int, l: int, r: int, L: int, R: int) -> int:
        if L <= l and r <= R:
            return self.mx[o]
        res = -INF
        m = (l + r) // 2
        if L <= m:
            res = self.queryMx(o * 2, l, m, L, R)
        if R > m:
            res = max(res, self.queryMx(o * 2 + 1, m + 1, r, L, R))
        return res

    def queryMn(self, o: int, l: int, r: int, L: int, R: int) -> int:
        if L <= l and r <= R:
            return self.mn[o]
        res = INF
        m = (l + r) // 2
        if L <= m:
            res = self.queryMn(o * 2, l, m, L, R)
        if R > m:
            res = min(res, self.queryMn(o * 2 + 1, m + 1, r, L, R))
        return res

    # 查询区间[L:]值为v的最大下标
    def BinaryQuery(self, o: int, l: int, r: int, L: int, v: int) -> int:
        if self.mx[o] == 0:
            return -1
        if l == r:
            return l if self.mx[o] == v else -1
        m = (l + r) // 2
        res = self.BinaryQuery(o * 2 + 1, m + 1, r, L, v)
        if res >= 0:
            return res
        if L <= m:
            return self.BinaryQuery(o * 2, l, m, L, v)

    # 查询区间[:R]值为v的最小下标
    def BinaryQuery2(self, o: int, l: int, r: int, R: int, v: int) -> int:
        if self.mx[o] == 0:
            return -1
        if l == r:
            return l if self.mx[o] == v else -1
        m = (l + r) // 2
        res = self.BinaryQuery2(o * 2, l, m, R, v)
        if res >= 0:
            return res
        if R > m:
            return self.BinaryQuery2(o * 2 + 1, m + 1, r, R, v)

    # 查询区间[:R]值为v的最大下标
    def BinaryQueryMn(self, o: int, l: int, r: int, R: int, v: int) -> int:
        if self.mx[o] < v:
            return -1
        if l == r:
            return l if self.mx[o] >= v else -1
        m = (l + r) // 2
        res = self.BinaryQueryMn(o * 2, l, m, R, v)
        if res >= 0:
            return res
        if R > m:
            return self.BinaryQueryMn(o * 2 + 1, m + 1, r, R, v)

    # 查询区间[L:]值为v的最小下标
    def BinaryQueryMx(self, o: int, l: int, r: int, L: int, v: int) -> int:
        if self.mn[o] >= v:
            return -1
        if l == r:
            return l if self.mn[o] < v else -1
        m = (l + r) // 2
        res = self.BinaryQueryMx(o * 2 + 1, m + 1, r, L, v)
        if res >= 0:
            return res
        if L <= m:
            return self.BinaryQueryMx(o * 2, l, m, L, v)

    # 初始化线段树   o,l,r=1,1,n
    def build(self, o: int, l: int, r: int) -> None:
        if l == r:
            self.mx[o] = self.nums[l - 1]
            self.mn[o] = self.nums[l - 1]
            return
        m = (l + r) // 2
        self.build(o * 2, l, m)
        self.build(o * 2 + 1, m + 1, r)
        self.mx[o] = max(self.mx[o * 2], self.mx[o * 2 + 1])
        self.mn[o] = min(self.mn[o * 2], self.mn[o * 2 + 1])
