from collections import defaultdict

from AlgorithmsCabin.DataStructure.SortedList.SortedList import SortedList
from AlgorithmsCabin.Math.Util.utils import sint, ints


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
