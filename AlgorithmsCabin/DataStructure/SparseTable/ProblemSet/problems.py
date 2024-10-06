from math import gcd

from AlgorithmsCabin.DataStructure.SparseTable.SparseTable import SparseTable
from AlgorithmsCabin.Math.Util.utils import sint, ints


def cf1548B():
    n = sint()
    a = ints()
    b = [abs(a[i] - a[i + 1]) for i in range(n - 1)] + [1]

    st = SparseTable(b, gcd)

    def binary_search(i: int, l: int, r: int) -> int:
        while l < r:
            m = (l + r + 1) // 2
            if st.query(i, m) > 1:
                l = m
            else:
                r = m - 1
        return l

    ans = 1
    for i in range(n - 1):
        if b[i] == 1:
            continue
        j = binary_search(i, i, n)
        ans = max(ans, j - i + 2)
    print(ans)
    return
