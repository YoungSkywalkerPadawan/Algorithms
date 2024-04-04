from math import inf
from typing import List


# lc2662 前往目标的最小代价
def minimumCost(source: str, target: str, original: List[str], changed: List[str], cost: List[int]) -> int:
    dis = [[inf] * 26 for _ in range(26)]
    for i in range(26):
        dis[i][i] = 0

    for x, y, c in zip(original, changed, cost):
        x = ord(x) - ord('a')
        y = ord(y) - ord('a')
        dis[x][y] = min(dis[x][y], c)

    for k in range(26):
        for i in range(26):
            for j in range(26):
                dis[i][j] = min(dis[i][j], dis[i][k] + dis[k][j])

    ans = sum(dis[ord(x) - ord('a')][ord(y) - ord('a')] for x, y in zip(source, target))
    return ans if ans < inf else -1
