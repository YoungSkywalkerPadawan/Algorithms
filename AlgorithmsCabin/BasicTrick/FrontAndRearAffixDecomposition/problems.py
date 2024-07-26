from collections import defaultdict
from itertools import accumulate
from math import inf
from operator import xor
from random import getrandbits
from typing import List

# lc2552 统计上升四元组
from AlgorithmsCabin.Math.Util.utils import sint, ints


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


def cf1986E():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()
    # 先按同余分组
    g = defaultdict(list)
    h = getrandbits(30)
    for x in a:
        g[(x % k) ^ h].append(x)
    # 统计奇数个的个数，如果n为偶数，不能有奇数个个数，n为奇数，可以存在一个
    cnt = 0
    for v in g.values():
        if len(v) % 2:
            cnt += 1
    if cnt > 1 or (cnt == 1 and n % 2 == 0):
        print(-1)
        return

    ans = 0
    for v in g.values():
        sl = len(v)
        if sl == 1:
            continue
        if sl % 2 == 0:
            i = 0
            while i < sl:
                ans += (v[i + 1] - v[i]) // k
                i += 2
        else:
            # 前后缀分解
            suf = [0] * (sl // 2 + 1)
            i = sl - 1
            j = sl // 2 - 1
            while i > 0:
                cur = (v[i] - v[i - 1]) // k
                suf[j] = suf[j + 1] + cur
                j -= 1
                i -= 2

            res = inf
            i = 0
            j = 0
            cur = 0
            while i < sl:
                res = min(res, cur + suf[j])
                if i == sl - 1:
                    break
                cur += (v[i + 1] - v[i]) // k
                i += 2
                j += 1
            ans += res

    print(ans)
    return


def cf1957D():
    n = sint()
    a = ints()
    # 主要在中间,如果两边同号则中间必须是0
    # 如果两边不同,则中间必须,可0可1,但注意0是两者相等
    # 前后缀分解,分别统计前缀各位1的个数和后缀各位是1的个数
    s = list(accumulate(a, func=xor, initial=0))
    res = 0
    for j in range(30):
        pre = 0
        suf = sum(x >> j & 1 for x in s)
        for i, x in enumerate(a):
            suf -= (s[i] >> j & 1)
            pre += (s[i] >> j & 1)
            if j == x.bit_length() - 1:
                res += pre * suf + (i + 1 - pre) * (n - i - suf)
    print(res)
    # for i in range(30):
    #     suf[i][n][0] = suf[i][n][1] = 0
    #
    # for i in range(30):
    #     for j in range(n):
    #         t = 1 if (1 << i) & a[j] > 0 else 0
    #         for k in range(2):
    #             pre[i][j + 1][k] = (t == k) + pre[i][j][k ^ t]
    #
    # for i in range(30):
    #     for j in range(n - 1, -1, -1):
    #         t = 1 if (1 << i) & a[j] > 0 else 0
    #         for k in range(2):
    #             suf[i][j][k] = (t == k) + suf[i][j + 1][k ^ t]
    #
    # ans = 0
    # for i in range(n):
    #     j = a[i].bit_length() - 1
    #     ans += pre[j][i][1] * (1 + suf[j][i + 1][0])
    #     ans += (1 + pre[j][i][0]) * (suf[j][i + 1][1])
    # print(ans)
    return


def cf1863F():
    n = sint()
    a = ints()
    sm = [0] * (n + 1)
    for i, x in enumerate(a):
        sm[i + 1] = sm[i] ^ x

    # 前后缀分解
    # 对于每个区间[i,j]看能不能从前缀[L,j]或后缀[i,R]转移过来
    # 设区间[i,j]异或和为s1,后缀[i,R]为s2,则s1 >= s1 ^ s2
    # 转移的化需要 s1最高位为1，然后s2是1,或者s2 == 0
    pre = [0] * n
    ans = []
    for i in range(n):
        suf = 0
        for j in range(n - 1, i - 1, -1):
            cur = sm[j + 1] ^ sm[i]
            flag = (i == 0 and j == n - 1) or suf < 0 or (suf & cur) != 0 or pre[j] < 0 or (pre[j] & cur) != 0
            if flag:
                if cur == 0:
                    pre[j] = -1
                    suf = -1
                else:
                    idx = cur.bit_length() - 1
                    pre[j] |= (1 << idx)
                    suf |= (1 << idx)
            if i == j:
                if flag:
                    ans.append("1")
                else:
                    ans.append("0")
    print("".join(ans))
    return
