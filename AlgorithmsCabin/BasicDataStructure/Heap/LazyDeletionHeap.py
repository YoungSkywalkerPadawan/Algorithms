from collections import Counter
from heapq import heappush, heappop
from typing import List


# lc3092 最高频率的ID
def mostFrequentIDs(nums: List[int], freq: List[int]) -> List[int]:
    n = len(nums)
    cnt = Counter()
    h = []
    ans = [0] * n
    i = 0
    for x, y in zip(nums, freq):
        cnt[x] += y
        heappush(h, (-cnt[x], x))
        while -h[0][0] != cnt[h[0][1]]:  # 堆顶保存的数据已经发生变化
            heappop(h)  # 删除
        ans[i] = -h[0][0]
        i += 1
    return ans
