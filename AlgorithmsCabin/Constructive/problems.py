from collections import Counter, defaultdict

from AlgorithmsCabin.Math.Util.utils import sint, ints, mint


def cf1227G():
    n = int(input())
    a = list(map(int, input().split()))
    ans = [['0'] * n for _ in range(n + 1)]
    res = sorted(enumerate(a), key=lambda p: -p[1])
    for i, (idx, x) in enumerate(res):
        for j in range(i, n + 1):
            if x == 0:
                break
            x -= 1
            ans[j][idx] = '1'
        for j in range(i):
            if x == 0:
                break
            x -= 1
            ans[j][idx] = '1'

    print(n + 1)
    for row in ans:
        print("".join(row))
    return


def cf1375D():
    n = sint()
    a = ints()
    st = set(a)
    cur = 0
    while cur in st:
        cur += 1

    cnt = Counter(a)
    idx = defaultdict()
    ans = []

    for i in range(n):
        x = a[i]
        if x < n and cnt[x] == 1:
            idx[x] = i
        else:
            cnt[x] -= 1
            ans.append(i + 1)
            a[i] = cur
            idx[cur] = i
            cur += 1
            while cur in st:
                cur += 1

    for i in range(n):
        if a[i] == i:
            continue

        # 先找到i在哪里，然后循环迭代，直到回到自身
        ans.append(idx[i] + 1)
        a[idx[i]] = cur
        j = i
        while j < n:
            ans.append(j + 1)
            nxt = a[j]
            a[j] = j
            j = nxt
            if a[j] == cur:
                ans.append(j + 1)
                a[j] = j
                break

    print(len(ans))
    print(*ans)

    return


def cf1363C():
    n, m = mint()
    g = [ints() for _ in range(n)]

    #  判断一个格子是不是好格子，自己是1 或者有一个小于自己的邻居
    def ok(x_: int, y_: int) -> bool:
        return (g[x_][y_] == 1) or (y_ > 0 and g[x_][y_ - 1] < g[x_][y_]) or \
               (y_ + 1 < m and g[x_][y_ + 1] < g[x_][y_]) or (x_ > 0 and g[x_ - 1][y_] < g[x_][y_]) or\
               (x_ + 1 < n and g[x_ + 1][y_] < g[x_][y_])

    # 判断（x,y） 和它的邻居是不是都是好格子
    def ok2(x_: int, y_: int) -> bool:
        return ok(x_, y_) and (y_ == 0 or ok(x_, y_ - 1)) and (y_ + 1 == m or ok(x_, y_ + 1)) \
               and (x_ == 0 or ok(x_ - 1, y_)) and (x_ + 1 == n or ok(x_ + 1, y_))

    # 收集坏格子
    badPos = []
    for i in range(n):
        for j in range(m):
            if not ok(i, j):
                badPos.append((i, j))

    if not badPos:
        print(0)
        return

    ans = set()
    bi, bj = badPos[0][0], badPos[0][1]

    for pi, pj in (bi, bj), (bi, bj - 1), (bi, bj + 1), (bi - 1, bj), (bi + 1, bj):
        if pi < 0 or pi == n or pj < 0 or pj == m:
            continue

        for i in range(n):
            for j in range(m):
                g[pi][pj], g[i][j] = g[i][j], g[pi][pj]
                flag = False
                for x, y in badPos:
                    if not ok(x, y):
                        flag = True
                        break

                if flag:
                    g[pi][pj], g[i][j] = g[i][j], g[pi][pj]
                    continue

                if ok2(i, j) and ok2(pi, pj):
                    ans.add((min(pi * m + pj, i * m + j), max(pi * m + pj, i * m + j)))
                g[pi][pj], g[i][j] = g[i][j], g[pi][pj]

    if ans:
        print(1, len(ans))
    else:
        print(2)

    return
