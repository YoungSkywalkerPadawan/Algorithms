from collections import deque, Counter
from itertools import accumulate
from random import getrandbits
from typing import List

# lc2281 巫师的总力量和
from AlgorithmsCabin.Math.Util.utils import sint, ints, mint


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


def cf2001D():
    n = sint()
    a = ints()
    # 单调递增栈，如果该数字只剩一次，必须留下
    # 如果该元素之前出现过，直接跳过，次数减一
    # 正常情况如果栈里是大小依此排列，如果当前更大，则找到最大位置，若当前小则找到小位置，间隔往前跳
    dq = deque()
    cnt = Counter(a)
    vis = [0] * (n + 1)
    for x in a:
        if vis[x] == 1:
            cnt[x] -= 1
            continue
        if dq and dq[-1] > x:
            while dq and dq[-1] > x and cnt[dq[-1]] > 1:
                if len(dq) % 2 == 0:
                    cur = dq.pop()
                    cnt[cur] -= 1
                    vis[cur] = 0
                else:
                    # 小，看倒数第二在不在
                    if len(dq) > 1 and cnt[dq[-2]] > 1 and dq[-2] > x:
                        cur = dq.pop()
                        cnt[cur] -= 1
                        vis[cur] = 0
                        cur = dq.pop()
                        cnt[cur] -= 1
                        vis[cur] = 0
                    else:
                        break
        elif dq and dq[-1] < x:
            while dq and dq[-1] < x and cnt[dq[-1]] > 1:
                if len(dq) % 2:
                    cur = dq.pop()
                    cnt[cur] -= 1
                    vis[cur] = 0
                else:
                    # 大，看倒数第二在不在
                    if len(dq) > 1 and cnt[dq[-2]] > 1 and dq[-2] < x:
                        cur = dq.pop()
                        cnt[cur] -= 1
                        vis[cur] = 0
                        cur = dq.pop()
                        cnt[cur] -= 1
                        vis[cur] = 0
                    else:
                        break
        dq.append(x)
        vis[x] = 1
    print(len(dq))
    print(*dq)
    return


def cf2009G():
    n, k, q = mint()
    a = ints()
    for i in range(n):
        a[i] -= i

    h = getrandbits(30)
    cnt = Counter()
    cnt_mx = Counter()
    mx = 0
    for i in range(k):
        x = a[i]
        cnt[x ^ h] += 1
        cnt_mx[cnt[x ^ h]] += 1
        if cnt[x ^ h] > 1:
            cnt_mx[cnt[x ^ h] - 1] -= 1
        mx = max(mx, cnt[x ^ h])

    res = [k - mx]

    l = 0
    for r in range(k, n):
        x = a[r]
        cnt[x ^ h] += 1
        cnt_mx[cnt[x ^ h]] += 1
        if cnt[x ^ h] > 1:
            cnt_mx[cnt[x ^ h] - 1] -= 1
        mx = max(mx, cnt[x ^ h])
        x = a[l]
        cnt[x ^ h] -= 1
        cnt_mx[cnt[x ^ h]] += 1
        cnt_mx[cnt[x ^ h] + 1] -= 1
        if cnt[x ^ h] + 1 == mx and cnt_mx[cnt[x ^ h] + 1] == 0:
            mx -= 1
        l += 1
        res.append(k - mx)

    queries = [[] for _ in range(n)]
    for i in range(q):
        l, r = mint()
        l -= 1
        r -= 1
        r -= k - 1
        queries[l].append(r * q + i)

    # 单调栈
    # 若res[i-1] < res[i],显然后面的不如前面,用前面的结果即可
    res.append(0)  # 加入哨兵，方便判断
    m = len(res)
    dq = [m - 1]
    acc = [0]
    ans = [-1] * q

    def check(x_: int, y: int) -> bool:
        return dq[x_] <= y

    for i in range(m - 2, -1, -1):
        while res[i] < res[dq[-1]]:
            dq.pop()
            acc.pop()

        acc.append(acc[-1] + res[i] * (dq[-1] - i))
        dq.append(i)

        for query in queries[i]:
            r, idx = divmod(query, q)

            # 在单调栈中 找到<=r的最近位置，左边直接用acc的前缀和计算，右边用单调栈中该索引对应的值计算
            left = 0
            right = len(dq) - 1
            while left < right:
                mid = (left + right) >> 1
                if check(mid, r):
                    right = mid - 1
                else:
                    left = mid + 1
            left = left if check(left, r) else left + 1
            ans[idx] = acc[-1] - acc[left] + res[dq[left]] * (r - dq[left] + 1)
    for x in ans:
        print(x)

    return
