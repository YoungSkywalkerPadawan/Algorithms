from math import gcd

from AlgorithmsCabin.DataStructure.SparseTable.SparseTable2 import SparseTable
from AlgorithmsCabin.Math.Util.utils import sint, ints


def cf1572A():
    n = sint()
    a = ints()

    st_gcd = SparseTable(a, gcd)
    st_min = SparseTable(a, min)

    def check(x: int) -> bool:
        for i in range(n - x + 1):
            if st_gcd.query(i, i + x - 1) == st_min.query(i, i + x - 1):
                return True
        return False

    l = 1
    r = n
    while l < r:
        mid = (l + r) >> 1
        if check(mid):
            l = mid + 1
        else:
            r = mid - 1

    l = l if check(l) else l - 1
    ans = [i + 1 for i in range(n - l + 1) if st_gcd.query(i, i + l - 1) == st_min.query(i, i + l - 1)]
    print(len(ans), l - 1)
    print(*ans)
    return
