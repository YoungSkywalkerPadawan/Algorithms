from collections import deque
from math import inf


class AC:

    def __init__(self, N: int):
        self.tot = 0
        self.tr = [[0] * 26 for _ in range(N)]
        self.e = [0] * N
        self.cost = [inf] * N
        self.len = [0] * N
        self.fail = [0] * N

    def insert(self, word: str, cost: int) -> None:
        u = 0
        for ch in word:
            ch = ord(ch) - ord("a")
            if self.tr[u][ch] == 0:
                self.tot += 1
                self.tr[u][ch] = self.tot
            u = self.tr[u][ch]

        if cost < self.cost[u]:
            self.cost[u] = cost
        self.len[u] = len(word)
        self.e[u] += 1

    def build(self) -> None:

        dq = deque()
        for i in range(26):
            if self.tr[0][i] != 0:
                dq.append(self.tr[0][i])

        while dq:
            u = dq.popleft()
            for i in range(26):
                if self.tr[u][i] != 0:
                    self.fail[self.tr[u][i]] = self.tr[self.fail[u]][i]
                    dq.append(self.tr[u][i])
                else:
                    self.tr[u][i] = self.tr[self.fail[u]][i]

    def search(self, word: str) -> int:
        n = len(word)
        dp = [inf] * (n + 1)
        dp[0] = 0
        u = 0
        for i in range(1, n + 1):
            ch = ord(word[i - 1]) - ord("a")
            u = self.tr[u][ch]
            j = u
            while j != 0:
                if self.e[j] != 0:
                    if dp[i - self.len[j]] + self.cost[j] < dp[i]:
                        dp[i] = dp[i - self.len[j]] + self.cost[j]
                j = self.fail[j]

        return dp[-1] if dp[-1] < inf else -1
