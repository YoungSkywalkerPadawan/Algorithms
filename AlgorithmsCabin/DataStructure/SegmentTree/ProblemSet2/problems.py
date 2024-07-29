from AlgorithmsCabin.DataStructure.SegmentTree.ImprovedSegmentTree import SegmentTree
from AlgorithmsCabin.Math.Util.utils import mint, ints


def cf1990F():
    n, m = mint()
    a = [0] + ints()
    st = SegmentTree(n, a)
    for i in range(m):
        op = ints()
        if op[0] == 1:
            print(st.query_ans(op[1], op[2]))
        else:
            st.update(1, op[1], op[2], i+1)
