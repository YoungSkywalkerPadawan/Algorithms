MOD = 998244353


def cf1989D():
    # n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    c = list(map(int, input().split()))
    mx = max(a)
    best = [10 ** 9] * (mx + 1)
    for x, y in zip(a, b):
        best[x] = min(best[x], x - y)
    for i in range(1, mx + 1):
        best[i] = min(best[i], best[i - 1])

    dp = [0] * (mx + 1)
    for i in range(1, mx + 1):
        if i - best[i] >= 0:
            dp[i] = 2 + dp[i - best[i]]

    res = 0
    for x in c:
        if x > mx:
            k = (x - mx) // best[mx] + 1
            res += 2 * k + dp[x - k * best[mx]]
        else:
            res += dp[x]
    print(res)
    return


def cf1989E():
    n, k = map(int, input().split())
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    sm = [0] * (k + 1)
    # sm[0] = 1
    # dp[i][j] = dp[i-1, j-1] +... + dp[0,j-1]
    for i in range(1, n + 1):
        for j in range(k + 1):
            if i >= 3:
                sm[j] += dp[i - 3][j]
                sm[j] %= MOD
            d = sm[max(j - 1, 0)] + dp[i - 1][max(j - 1, 0)]
            if i == n or i == 2:
                d += dp[i - 2][max(j - 1, 0)]
            d %= MOD
            dp[i][j] = d
    print(dp[-1][-1])
    return
