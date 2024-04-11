from collections import deque, Counter
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


# lc2030 含特定字母的最小子序列
def smallestSubsequence(s: str, k: int, letter: str, repetition: int) -> str:
    cnt = Counter(s)
    dq = deque()
    n = len(s)
    # 在满足选择的数量大于等于k的情况下，且letter足够的情况下，栈顶的元素大于当前元素则弹出
    for i, x in enumerate(s):
        while n - i > k - len(dq) and dq and dq[-1] > x:
            if dq[-1] == letter and cnt[letter] == repetition:
                break
            y = dq.pop()
            cnt[y] -= 1
        dq.append(x)
    # 完成一次遍历，选择的元素可能大于k,需要弹出，若弹出的是letter,考虑当前letter是否足够，不够后续要补,因为要补，所以k额外减少
    while len(dq) > k:
        y = dq.pop()
        cnt[y] -= 1
        if y == letter and cnt[letter] < repetition:
            k -= 1
    # 补不够的letter
    while cnt[letter] < repetition:
        dq.append(letter)
        cnt[letter] += 1
    return "".join(dq)
