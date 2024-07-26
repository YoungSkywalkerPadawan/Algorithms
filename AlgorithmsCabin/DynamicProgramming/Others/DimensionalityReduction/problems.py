from AlgorithmsCabin.Math.Util.utils import mint


def cf1994G():
    n, k = mint()
    s = input()
    target = [0] * k
    for i, x in enumerate(s):
        target[i] = int(x)
    cnt = [0] * k
    for _ in range(n):
        cur = input()
        for i, x in enumerate(cur):
            if x == '1':
                cnt[i] += 1

    dp = [-1] * (k * (n + 1))
    pre = [-1] * (k * (n + 1))
    if cnt[0] <= target[0]:
        dp[target[0] - cnt[0]] = 0
    if n - cnt[0] <= target[0]:
        dp[target[0] - n + cnt[0]] = 1

    for i in range(k - 1):
        for j in range(n + 1):
            cur = i * (n+1) + j
            if dp[cur] != -1:
                sub = 2 * j + target[i + 1] - cnt[i + 1]
                if 0 <= sub <= n:
                    nxt = (i+1) * (n+1) + sub
                    dp[nxt] = 0
                    pre[nxt] = cur
                sub = 2 * j + target[i + 1] - n + cnt[i + 1]
                if 0 <= sub <= n:
                    nxt = (i + 1) * (n + 1) + sub
                    dp[nxt] = 1
                    pre[nxt] = cur

    if dp[(k - 1) * (n+1)] == -1:
        print('-1')
    else:
        ans = []
        cur = (k - 1) * (n+1)
        for _ in range(k):
            ans.append(dp[cur])
            cur = pre[cur]
        print(''.join(map(str, reversed(ans))))
    return
