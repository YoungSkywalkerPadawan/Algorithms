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
