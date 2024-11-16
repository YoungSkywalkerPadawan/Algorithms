from AlgorithmsCabin.DataStructure.SegmentTree.DivideAndConquer.SegmentTree import SegmentTree
from AlgorithmsCabin.Math.Util.utils import sint, mint


def cf380C():
    s = input()
    n = len(s)
    st = SegmentTree(n, s)
    q = sint()
    for _ in range(q):
        u, v = mint()
        print(v - u + 1 - sum(st.query(1, 1, n, u, v)))

    return
