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


def cf1987F():
    n = int(input())
    a = list(map(int, input().split()))
    inf = 10 ** 9
    # dp[l][r]移除子段al...ar而需要在l左边进行的最小操作数
    dp = [[inf] * (n + 2) for _ in range(n + 2)]
    for i in range(1, n + 2):
        dp[i][i-1] = 0

    # 被移除必须 必须 i >= ai 且(i-ai)%2 == 0,下标从1开始
    for k in range(1, n):
        for l in range(1, n - k + 1):
            # 不可能被移除
            if a[l-1] > l:
                continue
            if (l - a[l-1]) % 2 != 0:
                continue

            # a[l] 被移除首先前面必须要操作的次数
            v = (l - a[l-1]) // 2
            r = l + k
            # 看 al, am能否操作,即dp[l+1][m-1] <= v否则,a[l]能被移除的时候,al,am之间还有元素
            for m in range(l + 1, r + 1, 2):
                if dp[l + 1][m-1] <= v:
                    # dp[l][m]能被移除了,操作次数为（m-l+1)//2
                    new_val = max(v, dp[m + 1][r] - (m - l + 1) // 2)
                    dp[l][r] = min(dp[l][r], new_val)

    # 对前缀a1,,,an执行操作的最大次数
    dp2 = [0] * (n + 1)

    for i in range(1, n+1):
        dp2[i] = dp2[i-1]

        for j in range(1, i):
            # [j, i]这一段可以j前面操作后被移除,操作次数为(i-j+1)//2
            if dp[j][i] <= dp2[j-1]:
                dp2[i] = max(dp2[i], dp2[j-1] + (i - j + 1) // 2)

    print(dp2[-1])
    return
