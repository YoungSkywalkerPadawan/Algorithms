from collections import deque
from math import inf

from AlgorithmsCabin.Math.Util.utils import sint, ints

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
    # inf = 10 ** 9
    # dp[l][r]移除子段al...ar而需要在l左边进行的最小操作数
    dp = [[inf] * (n + 2) for _ in range(n + 2)]
    for i in range(1, n + 2):
        dp[i][i - 1] = 0

    # 被移除必须 必须 i >= ai 且(i-ai)%2 == 0,下标从1开始
    for k in range(1, n):
        for l in range(1, n - k + 1):
            # 不可能被移除
            if a[l - 1] > l:
                continue
            if (l - a[l - 1]) % 2 != 0:
                continue

            # a[l] 被移除首先前面必须要操作的次数
            v = (l - a[l - 1]) // 2
            r = l + k
            # 看 al, am能否操作,即dp[l+1][m-1] <= v否则,a[l]能被移除的时候,al,am之间还有元素
            for m in range(l + 1, r + 1, 2):
                if dp[l + 1][m - 1] <= v:
                    # dp[l][m]能被移除了,操作次数为（m-l+1)//2
                    new_val = max(v, dp[m + 1][r] - (m - l + 1) // 2)
                    dp[l][r] = min(dp[l][r], new_val)

    # 对前缀a1,,,an执行操作的最大次数
    dp2 = [0] * (n + 1)

    for i in range(1, n + 1):
        dp2[i] = dp2[i - 1]

        for j in range(1, i):
            # [j, i]这一段可以j前面操作后被移除,操作次数为(i-j+1)//2
            if dp[j][i] <= dp2[j - 1]:
                dp2[i] = max(dp2[i], dp2[j - 1] + (i - j + 1) // 2)

    print(dp2[-1])
    return


def cf1956D():
    n = int(input())
    a = list(map(int, input().split()))
    # 0 0 0 0 0 => 5 5 5 5 5
    # 0 0 0 0 0 => 0 1 0 0 0 => 2 2 2 0 0 => 0 1 2 0 0 => 3 3 3 3 0 => 0 1 2 3 0 => 4 4 4 4 4 => 0 1 2 3 4 => 5 5 5 5 5
    # [1,1]       [0,2]         [0,1][1,1]   [0,3]       [0,2][1,1][0,2][0,1][1,1][0,3]  [0,4]  [0,3]
    # 类似汉诺塔
    # 先计算每一阶段的最大值,在构造答案的过程中,如果当前值小于之前统计的最大值，则这一段需要进行构造
    dp = [[0] * 2 for _ in range(n + 1)]
    for i in range(n):
        dp[i + 1][0] = max(dp[i]) + a[i]  # 这一阶段最大值ai不变
        for j in range(i + 1):
            dp[i + 1][1] = max(dp[i + 1][1], dp[j][0] + (i - j + 1) ** 2)

    ans = []
    i = n - 1
    while i >= 0:
        if dp[i + 1][0] < dp[i + 1][1]:
            # 需要找到一段进行改造[j, i]
            for j in range(i + 1):
                if dp[i + 1][1] == dp[j][0] + (i - j + 1) ** 2:
                    # 开始构造
                    pre = []
                    for k in range(j, i + 1):
                        if a[k] != k - j:
                            ans.append((j + 1, k + 1))
                            ans.extend(pre)
                        pre.append((j + 1, k + 1))
                        pre.extend(pre[:-1])
                    ans.append((j + 1, i + 1))
                    i = j - 1
                    break
        else:
            i -= 1
    print(max(dp[n]), len(ans))
    for x, y in ans:
        print(x, y)
    return


def cf1928E():
    n, x, y, s = map(int, input().split())
    # 计算通过若干段(0, 1, 2, ... ) 构成和k的最小数组长度
    dp = [inf] * (s + 1)
    p = [0] * (s + 1)
    dp[0] = 0
    for k in range(1, s + 1):
        l, m = 2, 1
        while m <= k:
            if dp[k - m] + l < dp[k]:
                dp[k] = dp[k - m] + l
                p[k] = l
            l += 1
            m = l * (l - 1) // 2

    for k in range(n):
        pre = x * (k + 1) + k * (k + 1) // 2 * y
        if pre > s:
            break

        sub = s - pre - (n - k - 1) * (x % y)
        if sub < 0 or sub % y:
            continue

        cnt = sub // y
        if dp[cnt] > n - k - 1:
            continue

        ans = list(range(x, x + k * y + 1, y)) + [x % y] * (n - k - 1 - dp[cnt])
        # 开始构造答案
        while cnt:
            l = p[cnt]
            cnt -= l * (l - 1) // 2
            ans.extend(range(x % y, x % y + (l - 1) * y + 1, y))

        print("YES")
        print(*ans)
        return

    print("NO")
    return


def cf1921G():
    n, m, k = map(int, input().split())
    g = [list(int(c == '#') for c in input()) for _ in range(n)]

    k = min(k, n + m - 2)
    ans = 0

    def check():
        nonlocal ans
        dia = deque([0] * (m + k))
        col = [0] * m

        for i in range(n):
            dia.pop()
            dia.appendleft(0)
            dp = [0] * m

            for j in range(m - 1, -1, -1):
                dia[j] += g[i][j]

                if i > k and j < m - 1 and j + k + 1 >= m:
                    dia[j + k + 1] -= g[i - k - 1][j]

                if i > k and j > k:
                    dia[j] -= g[i - k - 1][j - k - 1]

                col[j] += g[i][j]
                if i > k:
                    col[j] -= g[i - k - 1][j]

                dp[j] = col[j]
                if j < m - 1:
                    dp[j] += dp[j + 1]
                    dp[j] -= dia[j + k + 1]
                ans = max(ans, dp[j])

    check()
    g.reverse()
    check()
    for row in g:
        row.reverse()
    check()
    g.reverse()
    check()
    print(ans)
    return


def cf1927G():
    n = sint()
    a = ints()
    # dp[i][j][k]为从i到左边最远的未绘制单元格的距离为j到右边最近的未绘制单元格的距离为k(包括自身)所需的最小操作次数
    dp = [[[inf] * (n + 1) for _ in range(n + 1)] for _ in range(n + 1)]
    dp[0][0][0] = 0
    for i in range(n):
        for j in range(n):
            for k in range(n + 1):
                if dp[i][j][k] == inf:
                    continue
                ni = i + 1
                # 不选
                nj = j + 1 if j > 0 else 1 if k == 0 else 0
                nk = max(0, k - 1)
                dp[ni][nj][nk] = min(dp[ni][nj][nk], dp[i][j][k])

                # L
                nj = j + 1 if j > 0 else 0
                if nj <= a[i]:
                    nj = 0
                nk = max(0, k - 1)
                dp[ni][nj][nk] = min(dp[ni][nj][nk], dp[i][j][k] + 1)

                # R
                nj = j + 1 if j > 0 else 0
                nk = max(a[i] - 1, k - 1)
                dp[ni][nj][nk] = min(dp[ni][nj][nk], dp[i][j][k] + 1)
    print(min(dp[n][0]))
    return
