from _heapq import heappop
from heapq import heappush, heapreplace
from typing import List


# lc630 课程表III
def scheduleCourse(courses: List[List[int]]) -> int:
    courses.sort(key=lambda p: p[1])
    end = 0
    ans = 0
    h = []
    for x, y in courses:
        if end + x <= y:
            ans += 1
            heappush(h, -x)
            end += x
        else:
            if h and -h[0] > x:
                end -= (-h[0] - x)
                heapreplace(h, -x)
    return ans


# lc3049 标记所有下标的最早秒数II
def earliestSecondToMarkIndices(nums: List[int], changeIndices: List[int]) -> int:
    n = len(nums)
    m = len(changeIndices)
    tot = n + sum(nums)

    # 靠左的时间用来快速下降，方便后面进行标记
    # changeIndices 中每个i最早的下标，如果遇到，必须用了，因为前面没有了
    first_t = [-1] * n
    for t_ in range(m):
        if first_t[changeIndices[t_] - 1] < 0:
            first_t[changeIndices[t_] - 1] = t_

    def check(x: int) -> bool:
        cnt = 0
        slow = tot
        h = []
        for t in range(x - 1, -1, -1):
            i = changeIndices[t] - 1
            v = nums[i]
            if v <= 1 or t != first_t[i]:
                cnt += 1  # 不到最左不用
                continue

            if cnt == 0:
                if not h or v <= h[0]:
                    cnt += 1
                    continue
                slow += heappop(h) + 1
                cnt += 2  # 反悔：一次下降一次标记

            slow -= v + 1
            cnt -= 1
            heappush(h, v)
        return cnt >= slow

    l = n
    r = m
    while l < r:
        mid = (l + r) // 2
        if check(mid):
            r = mid - 1
        else:
            l = mid + 1
    if l > m:
        return -1
    ans = l if check(l) else l + 1
    return ans if ans <= m else -1


# lc2813 子序列最大优雅度
def findMaximumElegance(items: List[List[int]], k: int) -> int:
    items.sort(key=lambda p: -p[0])  # 把利润从大到小排序
    ans = total_profit = 0
    vis = set()
    duplicate = []  # 重复类别的利润
    for i, (profit, category) in enumerate(items):
        if i < k:
            total_profit += profit
            if category not in vis:
                vis.add(category)
            else:  # 重复类别
                duplicate.append(profit)
        elif duplicate and category not in vis:
            vis.add(category)
            total_profit += profit - duplicate.pop()  # 用最小利润替换
        # else: 比前面的利润小，而且类别还重复了，选它只会让 total_profit 变小，len(vis) 不变，优雅度不会变大
        ans = max(ans, total_profit + len(vis) * len(vis))

    return ans

