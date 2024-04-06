from collections import deque
from itertools import accumulate
from typing import List


# lc2281 巫师的总力量和
def totalStrength(strength: List[int]) -> int:
    MOD = 10 ** 9 + 7
    # 先用单调栈维护每个点左边第一个小于等于它的元素，以及右边第一个比它小点元素
    n = len(strength)
    left = [-1] * n
    dq = deque()
    for i, x in enumerate(strength):
        while dq and dq[-1][0] > x:
            dq.pop()
        if dq:
            left[i] = dq[-1][1]
        dq.append((x, i))
    right = [n] * n
    dq = deque()
    for i in range(n - 1, -1, -1):
        x = strength[i]
        while dq and dq[-1][0] >= x:
            dq.pop()
        if dq:
            right[i] = dq[-1][1]
        dq.append((x, i))
    # print(left)
    # print(right)
    # 计算前缀和，前缀和的前缀和
    # 考虑当前点strength[i]点左右边界[left,right]
    # left+1 <= l <= i, i<=r<=right-1
    # 固定r, (s[r+1] - s[i]) + ... + (s[r+1] - s[left+1]) = (i - left)*(s[r+1]) - (ss[i+1] - (ss[left+1])
    # 总和 = (i - left)*(ss[right+1] - ss[i+1]) - (right-i)*(ss[i+1] - (ss[left+1])
    s = list(accumulate(strength, initial=0))
    ss = list(accumulate(s, initial=0))
    # print(s)
    # print(ss)
    ans = 0
    for i, x in enumerate(strength):
        ans += x * ((i - left[i]) * (ss[right[i] + 1] - ss[i + 1]) - (right[i] - i) * (ss[i + 1] - ss[left[i] + 1]))
    return ans % MOD
