class SparseTable:
    def __init__(self, nums: list, op) -> None:
        self.note = [0] * (len(nums) + 1)
        self.op = op
        l, r, v = 1, 2, 0
        while True:
            for i in range(l, r):
                if i >= len(self.note):
                    break
                self.note[i] = v
            else:
                l *= 2
                r *= 2
                v += 1
                continue
            break
        self.ST = [[0] * len(nums) for _ in range(self.note[-1] + 1)]
        self.ST[0] = nums
        for i in range(1, len(self.ST)):
            for j in range(len(nums) - (1 << i) + 1):
                self.ST[i][j] = op(self.ST[i - 1][j], self.ST[i - 1][j + (1 << (i - 1))])

    def query(self, l: int, r: int):
        pos = self.note[r - l + 1]
        return self.op(self.ST[pos][l], self.ST[pos][r - (1 << pos) + 1])