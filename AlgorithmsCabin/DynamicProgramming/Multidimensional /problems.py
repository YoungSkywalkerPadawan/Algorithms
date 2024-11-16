from collections import Counter
from math import inf

from AlgorithmsCabin.Math.Util.utils import mint, ints, sint


def cf2025E():
    mod = 998244353
    n, m = mint()
    # 括号序列，匹配
    f = [[0] * (m + 1) for _ in range(m + 1)]
    f[0][0] = 1
    for i in range(m):
        for j in range(i + 1):
            # 用上一个左括号，未匹配数加一
            f[i + 1][j + 1] = (f[i + 1][j + 1] + f[i][j]) % mod
            if j:
                # 用上一个右括号，未匹配数减一
                f[i + 1][j - 1] = (f[i + 1][j - 1] + f[i][j]) % mod

    dp = [[0] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    for i in range(n):
        # 第一个必须要有多余的，后面的可以少，用前面第一次多的去减
        if i == 0:
            for j in range(m + 1):
                dp[i + 1][j] = f[m][j]
        else:
            for j in range(m + 1):
                for k in range(j + 1):
                    dp[i + 1][j - k] = (dp[i + 1][j - k] + dp[i][j] * f[m][k]) % mod
    print(dp[n][0])


def cf1363C():
    n, m = mint()
    a = ints()
    # DP，遇到可以分配的时候，枚举选哪个
    cnt1 = Counter()
    cnt2 = Counter()
    dp = [[0] * (m + 1) for _ in range(m + 1)]

    for x in a:
        if x > 0:
            cnt1[x] += 1
        elif x < 0:
            cnt2[-x] += 1
    cnt = 0
    ans = 0
    for x in a:
        if x > 0:
            cnt1[x] -= 1
            continue
        elif x < 0:
            cnt2[-x] -= 1
            continue
        cnt += 1
        for i in range(cnt + 1):
            j = cnt - i
            if i > 0:
                if dp[i - 1][j] + cnt1[i] > dp[i][j]:
                    dp[i][j] = dp[i - 1][j] + cnt1[i]
            if j > 0:
                if dp[i][j - 1] + cnt2[j] > dp[i][j]:
                    dp[i][j] = dp[i][j - 1] + cnt2[j]
            if dp[i][j] > ans:
                ans = dp[i][j]
    print(ans)

    return


def cf1517D():
    n, m, k = mint()
    row = [ints() for _ in range(n)]
    col = [ints() for _ in range(n - 1)]

    if k % 2:
        ans = [[-1] * m for _ in range(n)]
        for x in ans:
            print(*x)
    else:
        dp = [[0] * m for _ in range(n)]
        for _ in range(k // 2):
            ndp = [[inf] * m for _ in range(n)]
            for i in range(n):
                for j in range(m):
                    for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
                        if 0 <= x < n and 0 <= y < m:
                            # w = 0
                            if i == x:
                                w = row[i][min(j, y)]
                            else:
                                w = col[min(i, x)][j]

                            if dp[x][y] + w < ndp[i][j]:
                                ndp[i][j] = dp[x][y] + w
            dp = ndp
        for x in dp:
            print(*(v * 2 for v in x))

    return


def cf903F():
    n = sint()
    a = ints()
    g = [list(input()) for _ in range(4)]

    memo = [[[[[0] * 16 for _ in range(16)] for _ in range(16)] for _ in range(4)] for _ in range(n)]

    def dfs(j, i, cur, pre, pre2) -> int:
        if j < 0:
            if pre > 0 or pre2 > 0:
                return a[3]
            return 0

        if i > 3:
            if pre2 > 0:
                nxt = dfs(j - 2, 0, 0, 0, 0)
                return nxt + a[3]
            nxt = dfs(j - 1, 0, 0, cur, pre)
            return nxt

        p = memo[j][i][cur][pre][pre2]
        if p > 0:
            return p - 1
        v = 1 if g[i][j] == '*' else 0
        res = dfs(j, i + 1, (cur << 1) | v, pre, pre2)
        res1 = dfs(j, i + 1, cur << 1, pre, pre2)
        if res1 + a[0] < res:
            res = res1 + a[0]
        res2 = dfs(j, i + 2, cur << min(4 - i, 2), pre & (~(3 << max(2 - i, 0))), pre2)
        if res2 + a[1] < res:
            res = res2 + a[1]

        res3 = dfs(j, i + 3, cur << min(4 - i, 3), pre & (~(7 << max(1 - i, 0))), pre2 & (~(7 << max(1 - i, 0))))
        if res3 + a[2] < res:
            res = res3 + a[2]

        memo[j][i][cur][pre][pre2] = res + 1
        return res

    ans = dfs(n - 1, 0, 0, 0, 0)
    print(ans)
    return
