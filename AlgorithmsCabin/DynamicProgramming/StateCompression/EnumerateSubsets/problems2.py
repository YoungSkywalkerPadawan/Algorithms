from math import inf

from AlgorithmsCabin.Math.Util.utils import mint


def cf1955H():
    R = 12
    n, m, k = mint()
    g = [input() for _ in range(n)]
    p = [0] * k
    cord = []
    for i in range(k):
        u, v, w = mint()
        u -= 1
        v -= 1
        cord.append((u, v))
        p[i] = w

    cover = [[0] * (R + 1) for _ in range(k)]
    for i in range(k):
        x, y = cord[i]
        for r in range(1, R + 1):
            for dx in range(-r, r + 1):
                for dy in range(-r, r + 1):
                    nx = x + dx
                    ny = y + dy
                    if 0 <= nx < n and 0 <= ny < m:
                        if (x - nx) * (x - nx) + (y - ny) * (y - ny) <= r * r and g[nx][ny] == '#':
                            cover[i][r] += 1

    # 开始状压DP,枚举所有子集
    dp = [[-inf] * (1 << R) for _ in range(k + 1)]
    dp[0][0] = 0
    for i in range(1, k + 1):
        for mask in range(1 << R):
            dp[i][mask] = dp[i - 1][mask]  # 当前不选
            for r in range(1, R + 1):
                j = r - 1
                if (1 << j) & mask > 0:
                    dp[i][mask] = max(dp[i][mask], dp[i - 1][mask ^ (1 << j)] + p[i - 1] * cover[i - 1][r])

    ans = 0
    for mask in range(1 << R):
        hp = 0
        mlt = 3
        for j in range(R):
            if (1 << j) & mask > 0:
                hp += mlt
            mlt *= 3
        for i in range(k + 1):
            ans = max(ans, dp[i][mask] - hp)
    print(ans)
    return
