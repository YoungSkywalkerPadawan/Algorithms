from AlgorithmsCabin.DataStructure.DictionaryTree.BinaryTrie import BinaryTrie
from AlgorithmsCabin.Math.Util.utils import sint


def cf1363C():
    n = sint()
    t = BinaryTrie()
    t.insert(0)
    for _ in range(n):
        op, x = map(str, input().split())
        if op == '+':
            t.insert(int(x))
        elif op == '-':
            t.delete(int(x))
        else:
            print(t.query(int(x)))

    return
