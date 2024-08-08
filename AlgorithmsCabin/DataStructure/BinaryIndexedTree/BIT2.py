class BIT:
    def __init__(self, n: int):
        self.tree = [0] * n  # 树状数组
        self.n = n
        self.m = len(bin(n)[2:])

    def add(self, x: int, val: int) -> None:
        while x < self.n:
            self.tree[x] += val
            x |= x + 1

    # 维护权值和
    def sm(self, x: int) -> int:
        res = 0
        while x > 0:
            res += self.tree[x-1]
            x &= x - 1
        return res

    def range_sm(self, l: int, r: int) -> int:
        return self.sm(r) - self.sm(l)

    def select(self, k: int):
        x = 0
        cur = 0
        i = 1 << self.m
        while i > 0:
            if x + i <= self.n and cur + self.tree[x + i - 1] <= k:
                x += i
                cur += self.tree[x - 1]
            i //= 2
        return x
