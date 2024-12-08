from math import gcd

from AlgorithmsCabin.DataStructure.SegmentTree.ImprovedBinarySegmentTree import SegmentTree
from AlgorithmsCabin.DataStructure.SortedList.SortedList import SortedList
from AlgorithmsCabin.Math.Util.utils import mint, ints

inf = 10 ** 18
MX = 2 * 10 ** 6
sl = SortedList()
sl.add([inf, 0])
seg = SegmentTree([0] * (MX + 1), 0, lambda a, b: a if a > b else b)


def cf2000H():
    n = int(input())
    a = [0] + list(map(int, input().split())) + [inf]
    # 间隔
    for i in range(n + 1):
        cur = a[i + 1] - a[i] - 1
        # 将间隔大小维护在左端点
        sl.add([a[i], cur])
        seg.update(a[i], cur)

    ans = []
    q = int(input())
    for _ in range(q):
        p, x = input().split()
        x = int(x)
        if p == '+':
            idx = sl.bisect_left([x, 0])
            pre, nxt = sl[idx - 1][0], sl[idx][0]
            sl[idx - 1][1] = x - pre - 1
            seg.update(pre, x - pre - 1)
            sl.add([x, nxt - x - 1])
            seg.update(x, nxt - x - 1)
        elif p == '-':
            idx = sl.bisect_left([x, 0])
            pre, nxt = sl[idx - 1][0], sl[idx + 1][0]
            sl[idx - 1][1] = nxt - pre - 1
            seg.update(pre, nxt - pre - 1)
            # 删除idx
            sl.pop(idx)
            seg.update(x, 0)
        else:
            idx = seg.bisect_left(0, lambda v: v >= x)
            ans.append(idx + 1)

    for _ in range(len(sl) - 1):
        seg.update(sl[0][0], 0)
        sl.pop(0)
    return ans


def cf2050F():
    n, q = mint()
    a = ints()
    res = []
    for i in range(n - 1):
        res.append(abs(a[i + 1] - a[i]))
    seg1 = SegmentTree([0] * (n + 1), 0, lambda x1, y1: x1 if x1 > y1 else x1)
    for i, x in enumerate(a):
        seg1.update(i + 1, x)
    seg2 = SegmentTree([0] * n, 0, lambda x1, y1: gcd(x1, y1))
    for i, x in enumerate(res):
        seg2.update(i + 1, x)
    ans = [0] * q
    for i in range(q):
        l, r = mint()
        if l == r:
            ans[i] = 0
            continue
        mx = seg1.query(l, r)
        gd = seg2.query(l, r - 1)
        if gd == mx:
            ans[i] = 0
        else:
            ans[i] = gd
    print(*ans)

    return
