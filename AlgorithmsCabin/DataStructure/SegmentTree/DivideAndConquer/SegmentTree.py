class SegmentTree:
    def __init__(self, n: int, s: str):
        self.cntl = [0] * (2 << n.bit_length())
        self.cntr = [0] * (2 << n.bit_length())
        self.s = s
        self.build(1, 1, n)

    # 初始化线段树   o,l,r=1,1,n
    def build(self, o: int, l: int, r: int) -> None:
        if l == r:
            self.cntl[o] = 0 if self.s[l - 1] == ')' else 1
            self.cntr[o] = 1 if self.s[l - 1] == ')' else 0
            return
        m = (l + r) // 2
        self.build(o * 2, l, m)
        self.build(o * 2 + 1, m + 1, r)
        self.maintain(o)

    def maintain(self, o: int) -> None:
        # 左边的左括号可以和右边的右括号合并
        mn = self.cntl[o * 2] if self.cntl[o * 2] < self.cntr[o * 2 + 1] else self.cntr[o * 2 + 1]
        self.cntr[o] = self.cntr[o * 2] + self.cntr[o * 2 + 1] - mn
        self.cntl[o] = self.cntl[o * 2] + self.cntl[o * 2 + 1] - mn

    def update(self, o: int, l: int, r: int, i: int, val: int) -> None:
        if l == r:
            self.cntl[o] = 0 if self.s[l - 1] == ')' else 1
            self.cntr[o] = 1 if self.s[l - 1] == ')' else 0
            return
        m = (l + r) // 2
        if i <= m:
            self.update(o * 2, l, m, i, val)
        else:
            self.update(o * 2 + 1, m + 1, r, i, val)
        self.maintain(o)

    def query(self, o: int, l: int, r: int, L: int, R: int) -> tuple:
        if L <= l and r <= R:
            return self.cntl[o], self.cntr[o]
        # res = 0
        resl = 0
        resr = 0
        m = (l + r) // 2
        if L <= m:
            resl, resr = self.query(o * 2, l, m, L, R)
        if R > m:
            resl2, resr2 = self.query(o * 2 + 1, m + 1, r, L, R)
            mn = resl if resl < resr2 else resr2
            resl += resl2 - mn
            resr += resr2 - mn
        return resl, resr
