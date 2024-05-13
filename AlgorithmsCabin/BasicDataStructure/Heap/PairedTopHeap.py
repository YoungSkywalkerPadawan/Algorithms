from collections import Counter
from heapq import heappushpop, heappush, heappop
from typing import List


# lc480 滑动窗口中位数
def medianSlidingWindow(nums: List[int], k: int) -> List[float]:
    left = []  # 维护较小的一半，大根堆（小根堆取负号）
    right = []  # 维护较大的一半，小根堆
    dt = Counter()
    ans = []
    # 先加入前k个
    for i in range(k):
        if i % 2 == 0:  # 前缀长度是奇数 两边相等，最后在right,先去left过一下
            t = -heappushpop(left, -nums[i])
            heappush(right, t)

        else:  # 前缀长度是偶数 右边多，最后在left,先去right过一下
            t = -heappushpop(right, nums[i])
            heappush(left, t)

    ans.append((-left[0] + right[0]) / 2 if k % 2 == 0 else right[0])

    n = len(nums)
    index = 0
    for j in range(k, n):
        dt[nums[index]] += 1
        # 需要踢出nums[index] index 是在哪边
        if nums[index] >= right[0]:
            # 删除右边，再加入右边
            # right.remove(nums[index])
            if right and dt[right[0]] >= 1:
                dt[right[0]] -= 1
                heappop(right)
                while right and dt[right[0]] >= 1:
                    dt[right[0]] -= 1
                    heappop(right)
            t = -heappushpop(left, -nums[j])
            if left and dt[-left[0]] >= 1:
                dt[-left[0]] -= 1
                heappop(left)
                while left and dt[-left[0]] >= 1:
                    dt[-left[0]] -= 1
                    heappop(left)
            heappush(right, t)
        else:
            # 删除左边，再加入左边
            # left.remove(-nums[index])
            if left and dt[-left[0]] >= 1:
                dt[-left[0]] -= 1
                heappop(left)
                while left and dt[-left[0]] >= 1:
                    dt[-left[0]] -= 1
                    heappop(left)
            t = -heappushpop(right, nums[j])
            if right and dt[right[0]] >= 1:
                dt[right[0]] -= 1
                heappop(right)
                while right and dt[right[0]] >= 1:
                    dt[right[0]] -= 1
                    heappop(right)
            heappush(left, t)
        ans.append((-left[0] + right[0]) / 2 if k % 2 == 0 else right[0])
        index += 1
    return ans
