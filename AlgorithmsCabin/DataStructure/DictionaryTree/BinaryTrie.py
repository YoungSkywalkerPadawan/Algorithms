class BinaryTrie:
    def __init__(self, max_bit: int = 30):
        self.inf = 1 << 63
        self.to = [[-1], [-1]]
        self.cnt = [0]
        self.max_bit = max_bit

    def insert(self, num: int) -> None:
        cur = 0
        self.cnt[cur] += 1
        for k in range(self.max_bit, -1, -1):
            bit = (num >> k) & 1
            if self.to[bit][cur] == -1:
                self.to[bit][cur] = len(self.cnt)
                self.to[0].append(-1)
                self.to[1].append(-1)
                self.cnt.append(0)
            cur = self.to[bit][cur]
            self.cnt[cur] += 1

    def delete(self, num: int) -> bool:
        if self.cnt[0] == 0: return False
        cur = 0
        rm = [0]
        for k in range(self.max_bit, -1, -1):
            bit = (num >> k) & 1
            cur = self.to[bit][cur]
            if cur == -1 or self.cnt[cur] == 0: return False
            rm.append(cur)
        for cur in rm: self.cnt[cur] -= 1
        return True

    # Get max result for constant x ^ element in array
    def query(self, x: int) -> int:
        if self.cnt[0] == 0: return -self.inf
        res = cur = 0
        for k in range(self.max_bit, -1, -1):
            bit = (x >> k) & 1
            nxt = self.to[bit ^ 1][cur]
            if nxt == -1 or self.cnt[nxt] == 0:
                cur = self.to[bit][cur]
            else:
                cur = nxt
                res |= 1 << k
        return res
