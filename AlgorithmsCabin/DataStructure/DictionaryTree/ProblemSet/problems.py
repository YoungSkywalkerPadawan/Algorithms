from typing import List

from AlgorithmsCabin.DataStructure.DictionaryTree.Trie import Trie


# lc3093 最长公共后缀查询
def stringIndices(wordsContainer: List[str], wordsQuery: List[str]) -> List[int]:
    t = Trie()
    for i, x in enumerate(wordsContainer):
        t.insert(x, i)
    n = len(wordsQuery)
    ans = [0] * n
    for i, x in enumerate(wordsQuery):
        ans[i] = t.search(x)
    return ans
