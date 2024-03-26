from collections import defaultdict
from math import inf


class Trie:

    def __init__(self):
        self.children = defaultdict()
        self.len = inf
        self.index = 0

    def insert(self, word: str, index: int) -> None:
        node = self
        curL = len(word)
        if curL < node.len:
            node.len = curL
            node.index = index
        for i in range(curL - 1, -1, -1):
            ch = word[i]
            ch = ord(ch) - ord("a")
            if ch not in node.children.keys():
                node.children[ch] = Trie()
            node = node.children[ch]
            if curL < node.len:
                node.len = curL
                node.index = index

    def search(self, word: str) -> int:
        node = self
        curL = len(word)
        for i in range(curL - 1, -1, -1):
            ch = word[i]
            ch = ord(ch) - ord("a")
            if ch not in node.children.keys():
                return node.index
            node = node.children[ch]
        return node.index
