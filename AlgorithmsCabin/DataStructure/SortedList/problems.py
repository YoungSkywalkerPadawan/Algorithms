from collections import defaultdict
from math import inf

from AlgorithmsCabin.DataStructure.SortedList.SortedList import SortedList
from AlgorithmsCabin.Math.Util.utils import sint, ints, mint


def cf459D():
    n = sint()
    a = ints()
    pre = [0] * n
    dt = defaultdict(int)
    for i in range(n):
        dt[a[i]] += 1
        pre[i] = dt[a[i]]

    suf = [0] * n
    dt = defaultdict(int)
    for i in range(n - 1, -1, -1):
        dt[a[i]] += 1
        suf[i] = dt[a[i]]

    lst = SortedList(suf)
    ans = 0
    for i in range(n):
        lst.discard(suf[i])
        ans += lst.bisect_left(pre[i])
    print(ans)
    return


def cf2021C():
    n, m, q = mint()
    a = ints()
    b = ints()

    pos = [0] * n
    for i, x in enumerate(a):
        pos[x - 1] = i

    b = [pos[x - 1] for x in b]

    idx = [SortedList() for _ in range(n)]
    for i, x in enumerate(b):
        idx[x].add(i)

    fir = [inf] * n
    for i in range(n):
        if idx[i]:
            fir[i] = idx[i][0]
    cnt = sum(1 for i in range(n - 1) if fir[i] > fir[i + 1])

    if cnt > 0:
        print("TIDAK")
    else:
        print("YA")

    for _ in range(q):
        s, t = mint()
        s -= 1
        t -= 1
        # 原来的位置
        pre = b[s]
        # 现在的位置
        cur = pos[t]

        # 考虑移除原来的位置
        if pre - 1 >= 0:
            if fir[pre - 1] > fir[pre]:
                cnt -= 1
        if pre + 1 < n:
            if fir[pre] > fir[pre + 1]:
                cnt -= 1

        idx[pre].remove(s)
        fir[pre] = idx[pre][0] if idx[pre] else inf
        # 重新计算
        if pre - 1 >= 0:
            if fir[pre - 1] > fir[pre]:
                cnt += 1
        if pre + 1 < n:
            if fir[pre] > fir[pre + 1]:
                cnt += 1

        # 考虑新换的值
        if cur - 1 >= 0:
            if fir[cur - 1] > fir[cur]:
                cnt -= 1
        if cur + 1 < n:
            if fir[cur] > fir[cur + 1]:
                cnt -= 1

        b[s] = cur
        idx[cur].add(s)
        fir[cur] = idx[cur][0]

        if cur - 1 >= 0:
            if fir[cur - 1] > fir[cur]:
                cnt += 1
        if cur + 1 < n:
            if fir[cur] > fir[cur + 1]:
                cnt += 1

        if cnt > 0:
            print("TIDAK")
        else:
            print("YA")
    return
