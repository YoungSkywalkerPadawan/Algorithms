class SegmentTree:
    def __init__(self, n: int, nums: str):
        self.a = [0] * (2 << n.bit_length())
        self.b = [0] * (2 << n.bit_length())
        self.c = [0] * (2 << n.bit_length())
        self.ab = [0] * (2 << n.bit_length())
        self.bc = [0] * (2 << n.bit_length())
        self.abc = [0] * (2 << n.bit_length())
        self.nums = nums

    # 初始化线段树   o,l,r=1,0,n-1
    def build(self, o: int, l: int, r: int) -> None:
        if l == r:
            if self.nums[l - 1] == 'a':
                self.a[o] = 1
            if self.nums[l - 1] == 'b':
                self.b[o] = 1
            if self.nums[l - 1] == 'c':
                self.c[o] = 1
            return
        m = (l + r) // 2
        self.build(o * 2, l, m)
        self.build(o * 2 + 1, m + 1, r)
        self.maintain(o)

    def maintain(self, o: int) -> None:
        self.a[o] = self.a[o * 2] + self.a[o * 2 + 1]
        self.b[o] = self.b[o * 2] + self.b[o * 2 + 1]
        self.c[o] = self.c[o * 2] + self.c[o * 2 + 1]
        self.ab[o] = min(self.a[o * 2] + self.ab[o * 2 + 1], self.ab[o * 2] + self.b[o * 2 + 1])
        self.bc[o] = min(self.b[o * 2] + self.bc[o * 2 + 1], self.bc[o * 2] + self.c[o * 2 + 1])
        self.abc[o] = min(self.a[o * 2] + self.abc[o * 2 + 1], self.ab[o * 2] + self.bc[o * 2 + 1],
                          self.abc[o * 2] + self.c[o * 2 + 1])

    def update(self, o: int, l: int, r: int, i: int, val: str) -> None:
        if l == r:
            if val == 'a':
                self.a[o] = 1
                self.b[o] = 0
                self.c[o] = 0
                self.ab[o] = 0
                self.bc[o] = 0
                self.abc[o] = 0
            if val == 'b':
                self.b[o] = 1
                self.a[o] = 0
                self.c[o] = 0
                self.ab[o] = 0
                self.bc[o] = 0
                self.abc[o] = 0
            if val == 'c':
                self.c[o] = 1
                self.b[o] = 0
                self.a[o] = 0
                self.ab[o] = 0
                self.bc[o] = 0
                self.abc[o] = 0
            return
        m = (l + r) // 2
        if i <= m:
            self.update(o * 2, l, m, i, val)
        else:
            self.update(o * 2 + 1, m + 1, r, i, val)
        self.maintain(o)

    # def query(self, o: int, l: int, r: int, L: int, R: int) -> int:
    #     if L <= l and r <= R:
    #         return self.f11[o]
    #     res = 0
    #     m = (l + r) // 2
    #     if L <= m:
    #         res = self.query(o * 2, l, m, L, R)
    #     if R > m:
    #         res = max(res, self.query(o * 2 + 1, m + 1, r, L, R))
    #     return res
