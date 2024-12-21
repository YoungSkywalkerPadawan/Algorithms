def cf2045H():
    s = input()
    n = len(s)
    # s[i] s[j] 最长公共前缀
    lcp = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if s[i] == s[j]:
                lcp[i][j] = lcp[i + 1][j + 1] + 1

    def check(l1: int, r1: int, l2: int, r2: int) -> bool:
        len1, len2 = r1 - l1, r2 - l2
        ll = lcp[l1][l2]
        mn = len1 if len1 < len2 else len2
        if ll >= mn:
            return len1 < len2

        return s[l1 + ll] < s[l2 + ll]

    dp = [[0] * n for _ in range(n)]
    # 记录dp[i] 后置最大值下标
    suf_mx = [[0] * n for _ in range(n)]
    nxt = [[0] * n for _ in range(n)]

    # 开始DP
    for i in range(n - 1, -1, -1):
        dp[i][n - 1] = 1
        nxt[i][n - 1] = n
        k = n - 1
        for j in range(n - 1, i - 1, -1):
            if check(i, j + 1, j + 1, n):
                lp = lcp[i][j + 1]
                l = lp if lp < j - i + 1 else j - i + 1
                k2 = suf_mx[j + 1][j + 1 + l]
                nxt[i][j] = k2
                dp[i][j] = dp[j + 1][k2] + 1
                if dp[i][j] > dp[i][k]:
                    k = j
            suf_mx[i][j] = k

    print(dp[0][suf_mx[0][0]])
    i = 0
    j = suf_mx[0][0]
    while i < n:
        print(s[i:j + 1])
        i, j = j + 1, nxt[i][j]

    return
