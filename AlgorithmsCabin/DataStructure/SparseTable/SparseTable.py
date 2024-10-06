from math import gcd


class SparseTable:
    def __init__(self, nums: list, op) -> None:
        self.pow2 = [1]
        for _ in range(20):
            self.pow2.append(2 * self.pow2[-1])
        self.op = op
        self.st = []
        s, l = nums, 1
        self.st.append(s)
        while l * 2 <= len(nums):
            ns = []
            for i in range(len(s) - l):
                ns.append(gcd(s[i], s[i + l]))
            s = ns
            self.st.append(s)
            l *= 2

    def query(self, l: int, r: int):
        # s = log2(r - l + 1)
        s = len(bin(r - l + 1)) - 3
        res = self.op(self.st[s][l], self.st[s][r - self.pow2[s] + 1])
        return res
