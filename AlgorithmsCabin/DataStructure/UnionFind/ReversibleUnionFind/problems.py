def cf1416D():
    n, m, q = map(int, input().split())
    num = [0] + list(map(int, input().split()))
    lian = [[] for _ in range(n + 1)]
    p = [0] * (n + 1)
    sz = [0] * (n + 1)
    for i in range(1, n + 1):
        p[i] = i
        sz[i] = 1
        lian[i].append(num[i])
    l = [0] * (m + 1)
    r = [0] * (m + 1)
    for i in range(1, m + 1):
        l1, r1 = map(int, input().split())
        l[i] = l1
        r[i] = r1

    op = [0] * (q + 1)
    opi = [0] * (q + 1)
    dl = [0] * (m + 1)
    of = [0] * (q + 1)
    belong = [0] * (n + 1)
    delPos = [False] * (n + 1)
    for i in range(1, q + 1):
        p1, q1 = map(int, input().split())
        op[i] = p1
        opi[i] = q1
        if p1 == 2:
            dl[q1] = 1

    def find(x: int) -> int:
        if x != p[x]:
            return find(p[x])
        return p[x]

    def merge(x: int, y: int, back: int, idx: int) -> None:
        x = find(x)
        y = find(y)
        if x == y:
            return
        if sz[x] > sz[y]:
            x, y = y, x
        if back == 1:
            of[idx] = x

        for v in lian[x]:
            lian[y].append(v)

        p[x] = y
        sz[y] += sz[x]
        return

    def roll(x: int) -> None:
        for v in lian[x]:
            belong[v] = x
        p[x] = x

    def query(x: int):
        x = find(x)
        while lian[x] and (belong[lian[x][-1]] != x or delPos[lian[x][-1]]):
            lian[x].pop()

        if not lian[x]:
            return 0

        ans = lian[x][-1]
        lian[x].pop()
        delPos[ans] = True
        return ans

    for i in range(1, m + 1):
        if dl[i] == 0:
            merge(l[i], r[i], 0, i)

    for i in range(q, 0, -1):
        if op[i] == 2:
            merge(l[opi[i]], r[opi[i]], 1, i)

    for i in range(1, n + 1):
        lian[i].sort()
        belong[num[i]] = find(i)

    for i in range(1, q + 1):
        if op[i] == 1:
            print(query(opi[i]))
        else:
            if of[i] > 0:
                roll(of[i])
