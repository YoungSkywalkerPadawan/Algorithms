from AlgorithmsCabin.GraphTheory.TreeRelated.TreeChainSegmentation.TreeChainSegmentation import TreeChainSegmentation


def p3384():
    n, m, r, mod = map(int, input().split())
    w = [0] + list(map(int, input().split()))
    to = [0] * (2 * n + 10)
    nxt = [0] * (2 * n + 10)
    beg = [0] * (2 * n + 10)
    e = 0

    def add(x: int, y: int) -> None:
        nonlocal e
        e += 1
        to[e] = y
        nxt[e] = beg[x]
        beg[x] = e

    for _ in range(n - 1):
        a, b = map(int, input().split())
        add(a, b)
        add(b, a)

    st = TreeChainSegmentation((2 * n + 10), to, nxt, beg, mod, w, r)
    for _ in range(m):
        op = list(map(int, input().split()))
        k = op[0]
        if k == 1:
            st.updRange(op[1], op[2], op[3])
        elif k == 2:
            print(st.qRange(op[1], op[2]))
        elif k == 3:
            st.updSon(op[1], op[2])
        else:
            print(st.qSon(op[1]))

    return
