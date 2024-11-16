from operator import sub, xor

from AlgorithmsCabin.DataStructure.SegmentTree.LazySegTree2 import LazySegTree
from AlgorithmsCabin.Math.Util.utils import ints, mint


def cf242E():
    # n = sint()
    a = ints()
    S = [LazySegTree(lambda x, y: x + y, 0, sub, xor, 0, [(x >> i) & 1 for x in a]) for i in range(20)]
    m = int(input())
    for _ in range(m):
        t, *p = mint()
        if t == 1:
            l, r = p
            res = 0
            for i in range(20):
                res += S[i].prod(l-1, r) * (1 << i)
            print(res)
        else:
            assert t == 2
            l, r, x = p
            for i in range(20):
                if (x >> i) & 1:
                    S[i].apply(l-1, r, 1)

    return

