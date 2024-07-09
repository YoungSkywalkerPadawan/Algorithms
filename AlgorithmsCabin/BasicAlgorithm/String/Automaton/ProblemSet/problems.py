from functools import reduce
from typing import List

from AlgorithmsCabin.BasicAlgorithm.String.Automaton.AC import AC


# lc3213 最小代价构造字符串
def minimumCost(target: str, words: List[str], costs: List[int]) -> int:
    n = reduce(lambda a, b: a + len(b), words, 1)
    ac = AC(n)
    for i, word in enumerate(words):
        ac.insert(word, costs[i])
    ac.build()
    ans = ac.search(target)
    return ans
