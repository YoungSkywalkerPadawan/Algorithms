from math import inf

from AlgorithmsCabin.Math.Util.utils import sint


def cf1950G():
    n = sint()
    g = []
    w = []
    for _ in range(n):
        gi, wi = input().split()
        g.append(gi)
        w.append(wi)

    f = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if g[i] == g[j] or w[i] == w[j]:
                f[i][j] = f[j][i] = True

    dp = [[0] * n for _ in range(1 << n)]
    for i in range(n):
        dp[1 << i][i] = 1
    ans = 0
    for mask in range(1, 1 << n):
        for i in range(n):
            if dp[mask][i] == 0:
                continue
            ans = max(ans, mask.bit_count())
            for j in range(n):
                if (mask >> j) & 1 or not f[i][j]:
                    continue
                dp[mask | (1 << j)][j] = 1
    print(n - ans)

    return


def cf2051G():
    n, q = [int(x) for x in input().split()]
    # def getDis(s: int, t: int) -> int:
    #     sm, mn = 0, 0
    #     for i in range(q):
    #         if idx[i] == t:
    #             sm += int(ch[i] < 0)
    #         if idx[i] == s:
    #             sm -= int(ch[i] > 0)
    #         mn = min(mn, sm)
    #     return -mn + 1

    # 相邻两条蛇的最小距离
    mnDis = [[0] * n for _ in range(n)]
    # 每条蛇最大长度
    ll = [0] * n
    rr = [0] * n
    for _ in range(q):
        u, v = input().split()
        u = int(u) - 1
        if v == '+':
            ll[u] += 1
        else:
            rr[u] += 1
        for i in range(n):
            if u == i:
                continue
            mnDis[i][u] = max(mnDis[i][u], ll[u] - rr[i])

    dp = [inf for _ in range((1 << n) * n)]
    for i in range(n):
        dp[n * (1 << i) + i] = 0
    ctz = [0] * (1 << n)
    for i in range(1 << n):
        ctz[i] = (i & -i).bit_length() - 1
    for mask in range(1, 1 << n):
        cur = mask
        while cur:
            i = ctz[cur]
            sub = (1 << n) - 1 - mask
            cur &= cur - 1
            pre = sub
            while pre:
                j = ctz[pre]
                dp[n * (mask | 1 << j) + j] = min(dp[n * (mask | 1 << j) + j], dp[n * mask + i] + mnDis[j][i])
                pre &= pre - 1
    # dp = [inf] * (n * (1 << n))
    # for i in range(n):
    #     dp[(1 << i) + (i << n)] = 0
    #
    # for msk in range(1 << n):
    #     for i in range(n):
    #         if (msk >> i) & 1 == 0:
    #             continue
    #
    #         for j in range(n):
    #             new_mask = msk | (1 << j) | (j << n)
    #             if dp[msk + (i << n)] + mnDis[i][j] < dp[new_mask]:
    #                 dp[new_mask] = dp[msk + (i << n)] + mnDis[i][j]

    ans = inf
    for i in range(n):
        ans = min(ans, dp[n*((1 << n) - 1)+i] + ll[i] + n)
    print(ans)
    return
