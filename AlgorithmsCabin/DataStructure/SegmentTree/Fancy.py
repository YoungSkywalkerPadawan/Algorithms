from AlgorithmsCabin.DataStructure.SegmentTree.LazySegmentTree3 import LazySegmentTree


# lc1622 奇妙序列
class Fancy:

    def __init__(self):
        self.c = 0
        self.mx = 10 ** 5 + 1
        self.st = LazySegmentTree(self.mx)

    def append(self, val: int) -> None:
        self.st.update(1, 0, self.mx, self.c, self.c, val)
        self.c += 1

    def addAll(self, inc: int) -> None:
        if self.c >= 1:
            self.st.update(1, 0, self.mx, 0, self.c - 1, inc)

    def multAll(self, m: int) -> None:
        if self.c >= 1:
            self.st.update2(1, 0, self.mx, 0, self.c - 1, m)

    def getIndex(self, idx: int) -> int:
        if idx + 1 > self.c:
            return -1
        return self.st.query(1, 0, self.mx, idx, idx)
