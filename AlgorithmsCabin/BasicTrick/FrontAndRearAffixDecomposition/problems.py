from typing import List


# lc2552 统计上升四元组
def countQuadruplets(nums: List[int]) -> int:
    n = len(nums)
    g = [[0] * (n + 1) for _ in range(n)]
    g[-1] = [0] * (n + 1)
    for k in range(n - 2, 1, -1):
        g[k] = g[k + 1][:]
        for i in range(1, nums[k + 1]):
            g[k][i] += 1

    l = [[0] * (n + 1) for _ in range(n)]
    l[0] = [0] * (n + 1)
    for j in range(1, n - 1):
        l[j] = l[j - 1][:]
        for i in range(nums[j - 1] + 1, n + 1):
            l[j][i] += 1
    ans = 0
    for j in range(1, n - 2):
        for k in range(j + 1, n - 1):
            if nums[j] > nums[k]:
                ans += l[j][nums[k]] * g[k][nums[j]]
    return ans
