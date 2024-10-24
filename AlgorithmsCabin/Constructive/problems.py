from collections import Counter, defaultdict

from AlgorithmsCabin.Math.Util.utils import sint, ints


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
