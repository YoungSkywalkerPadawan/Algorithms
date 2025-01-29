from collections import Counter
from functools import cache
from math import inf
from typing import List

# lc1815 得到新鲜甜甜圈的最多组数
# 状态压缩，相同余数的一起考虑
from AlgorithmsCabin.Math.Util.utils import mint, ints


def maxHappyGroups(batchSize: int, groups: List[int]) -> int:
    @cache
    def dfs(x: int, y: int) -> int:
        if x == 0:
            return 0
        pre = 0 if y > 0 else 1
        res = 0
        for j in range(1, batchSize):
            if (x >> (j * 5)) & 31:
                cur = dfs(x - (1 << (j * 5)), (y + j) % batchSize)
                if cur > res:
                    res = cur
        return res + pre

    f = 0
    ans = 0
    for v in groups:
        if v % batchSize == 0:
            ans += 1
        else:
            i = v % batchSize
            f += 1 << (i * 5)
    ans += dfs(f, 0)
    return ans


# lc691 贴纸拼词
# 反复使用某个对象
def minStickers(stickers: List[str], target: str) -> int:
    n = len(target)
    m = len(stickers)
    t = Counter(target)
    s = []
    for stick in stickers:
        c = Counter()
        for w in stick:
            if t[w] > 0:
                c[w] += 1
        s.append(c)

    @cache
    def dfs(x: int) -> int:
        if x == 0:
            return 0
        res = inf
        idx = [i for i in range(n) if (1 << i) & x]
        for i in range(m):
            cur = x
            cnt = s[i].copy()
            for j in idx:
                if cnt[target[j]]:
                    cnt[target[j]] -= 1
                    cur ^= (1 << j)
            if cur < x:
                res1 = 1 + dfs(cur)
                if res1 < res:
                    res = res1
        return res

    ans = dfs((1 << n) - 1)
    return ans if ans < inf else -1


# lc1434 每个人戴不同帽子的方案数
# 对较小数量的一方进行状态压缩
def numberWays(hats: List[List[int]]) -> int:
    n = len(hats)
    g = [[] for _ in range(40)]
    for i, row in enumerate(hats):
        for v in row:
            v -= 1
            g[v].append(i)
    MOD = 10 ** 9 + 7

    @cache
    def dfs(x: int, y: int) -> int:
        if y == 0:
            return 1
        if x == 40:
            return 0
        res = dfs(x + 1, y)
        for j in g[x]:
            if (1 << j) & y > 0:
                res += dfs(x + 1, y ^ (1 << j))
        return res % MOD

    ans = dfs(0, (1 << n) - 1)
    dfs.cache_clear()
    return ans % MOD


# luoguP5369
# 枚举该序列中一些元素构成的集合S
# S 的最大前缀和为 sum(S)， all−S 所有的前缀和都得小于0
# 记 S 构成的序列中有𝑓(𝑆)，f(S) 个序列满足最大前缀和为 sum(S)，g(S) 个序列满足所有前缀和小于0
# ans = ∑ f(S)g(all−S)sum(S)
def P5369():
    n = int(input())
    a = list(map(int, input().split()))

    MOD = 998244353

    N = (1 << n)
    s = [0] * N
    g = [0] * N
    f = [0] * N
    g[0] = 1
    for i in range(n):
        s[1 << i] = a[i]
        f[1 << i] = 1

    # 利用lowbit计算各个状态的和（动态规划）
    for i in range(N):
        s[i] = s[i & -i] + s[i ^ (i & -i)]

    for i in range(N):
        if s[i] < 0:
            for j in range(n):
                if (1 << j) & i:
                    g[i] = (g[i] + g[i ^ (1 << j)]) % MOD
        else:
            for j in range(n):
                if (1 << j) & i == 0:
                    f[i | (1 << j)] = (f[i | (1 << j)] + f[i]) % MOD

    ans = 0
    for i in range(1, N):
        ans = (ans + s[i] * f[i] * g[(N - 1) ^ i]) % MOD
    print(ans % MOD)
    return


def cf1391D():
    n, m = mint()
    g = [input() for _ in range(n)]
    if min(n, m) > 3:
        print(-1)
        return
    cnt = [0, 1, 1, 2, 1, 2, 2, 3]
    res = []
    if m > 3:
        for i in range(m):
            cur = 0
            for j in range(n):
                if g[j][i] == '1':
                    cur += 1 << j
            res.append(cur)
    else:
        for i in range(n):
            cur = 0
            for j in range(m):
                if g[i][j] == '1':
                    cur += 1 << j
            res.append(cur)
    if m > n:
        n, m = m, n
    # 开始状压DP
    dp = [cnt[i ^ res[0]] for i in range(1 << m)]
    for i in range(1, n):
        ndp = [inf] * (1 << m)
        for pre in range(1 << m):
            for nxt in range(1 << m):
                f = False
                for j in range(m - 1):
                    # 统计各偶数个数时1个数
                    v1 = pre >> j & 3
                    v2 = nxt >> j & 3
                    if (cnt[v1] + cnt[v2]) % 2 == 0:
                        f = True
                        break
                if not f:
                    if dp[pre] + cnt[res[i] ^ nxt] < ndp[nxt]:
                        ndp[nxt] = dp[pre] + cnt[res[i] ^ nxt]
        dp = ndp
    print(min(dp))

    return


def cf2061E():
    n, m, k = mint()
    a = ints()
    b = ints()
    ans = sum(a)
    f = [0] * (1 << m)
    # 对b的各项排列进行状态压缩，计算&
    f[0] = (1 << 30) - 1
    bit_count = [0] * (1 << m)
    for msk in range(1, 1 << m):
        bit_count[msk] = msk.bit_count()
    for i in range(m):
        msk = 1 << i
        for j in range(msk):
            f[j | msk] = f[j] & b[i]

    # 对a运用每一种b，看变化量
    res = []
    for x in a:
        # 下标操作次数，对应具体减少的值
        loss = [0] * (m + 1)
        for msk in range(1 << m):
            c = bit_count[msk]
            cur = x - (x & f[msk])
            if cur > loss[c]:
                loss[c] = cur
        for i in range(m):
            res.append(loss[i + 1] - loss[i])

    res.sort(reverse=True)
    i = min(k, len(res))
    ans -= sum(res[:i])
    print(ans)

    return
