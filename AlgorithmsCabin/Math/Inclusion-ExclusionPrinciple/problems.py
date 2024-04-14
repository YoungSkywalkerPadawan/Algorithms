from math import lcm
from typing import List


# lc393周赛T4 单面值组合的第k小金额
def findKthSmallest(coins: List[int], k: int) -> int:
    def check(x: int) -> bool:
        cnt = 0
        for mask in range(1, 1 << len(coins)):
            cur = 1
            for i, v in enumerate(coins):
                if mask >> i & 1:
                    cur = lcm(cur, v)
                    if cur > x:
                        break
            else:
                cnt += x // cur if mask.bit_count() % 2 else -(x // cur)
        return cnt >= k

    l = k - 1
    r = min(coins) * k
    while l < r:
        mid = (l + r) // 2
        if check(mid):
            r = mid - 1
        else:
            l = mid + 1
    return l if check(l) else l + 1
