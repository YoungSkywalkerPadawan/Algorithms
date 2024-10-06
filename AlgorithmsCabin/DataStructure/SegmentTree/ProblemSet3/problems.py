from AlgorithmsCabin.DataStructure.SegmentTree.ImprovedBinarySegmentTree import SegmentTree
from AlgorithmsCabin.DataStructure.SortedList.SortedList import SortedList

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
