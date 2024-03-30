# 利用树状数组求逆序对的个数
from bisect import bisect_left
from typing import List
from AlgorithmsCabin.DataStructure.BinaryIndexedTree.BIT import BIT


def reversePairs(record: List[int]) -> int:
    # 先进行数据离散化
    nums = sorted(set(record))
    mx = len(nums)
    b = BIT(mx + 1)
    ans = 0
    for i, x in enumerate(record):
        j = bisect_left(nums, x) + 1
        ans += (i - b.query(j))
        b.add(j, 1)
    return ans
