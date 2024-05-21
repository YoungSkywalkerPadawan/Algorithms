# 异或字典树
from collections import defaultdict
from functools import cache


class Trie:

    def __init__(self):
        self.children = defaultdict()
        self.cnt = 0

    def search(self, word: str) -> int:
        node = self
        pre = ""
        for ch in word:
            s = str(1 - int(ch))
            if s in node.children.keys() and node.children[s].cnt > 0:
                node = node.children[s]
                pre += "1"
            else:
                node = node.children[ch]
                pre += "0"
        return int('0b' + pre, 2)

    def searchNum(self, word: str, limit: str) -> int:
        node = self

        @cache
        def dfs(i: int, f: bool, cur) -> int:
            if i == 16:
                return cur.cnt
            s = word[i]
            t = limit[i]
            if f:
                return cur.cnt
            res = 0
            if t == '0':
                if s not in cur.children.keys():
                    return res
                else:
                    return dfs(i + 1, False, cur.children[s])
            else:
                s_ = str(1 - int(s))
                if s in cur.children.keys():
                    res += dfs(i + 1, True, cur.children[s])
                if s_ in cur.children.keys():
                    res += dfs(i + 1, False, cur.children[s_])
                return res

        ans = dfs(0, False, node)
        dfs.cache_clear()
        return ans

    def insert(self, word: str) -> None:
        node = self
        for ch in word:
            if ch not in node.children.keys():
                node.children[ch] = Trie()
            node = node.children[ch]
            node.cnt += 1

    def delete(self, word: str) -> None:
        node = self
        for ch in word:
            node = node.children[ch]
            node.cnt -= 1
