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
