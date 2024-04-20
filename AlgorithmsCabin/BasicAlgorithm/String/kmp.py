# 在字符串中查找子串：Knuth–Morris–Pratt 算法
# 给定一个文本 t 和一个字符串 s，我们尝试找到并展示 s 在 t 中的所有出现
from typing import List


def kmp(text: str, pattern: str) -> List[int]:
    m = len(pattern)
    pi = [0] * m
    c = 0
    for i in range(1, m):
        v = pattern[i]
        while c and pattern[c] != v:
            c = pi[c - 1]
        if pattern[c] == v:
            c += 1
        pi[i] = c

    res = []
    c = 0
    for i, v in enumerate(text):
        v = text[i]
        while c and pattern[c] != v:
            c = pi[c - 1]
        if pattern[c] == v:
            c += 1
        if c == len(pattern):
            res.append(i - m + 1)
            c = pi[c - 1]
    return res
