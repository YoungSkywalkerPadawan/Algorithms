# 定义一个把字符串映射到整数的函数 f，这个 f 称为是 Hash 函数。
# 这个函数 f 可以方便地帮我们判断两个字符串是否相等。
import random


# lc3031 将单词恢复初始状态所需的最短时间II
def minimumTimeToInitialState(word: str, k: int) -> int:
    n = len(word)
    # 字符串哈希模板
    random.seed()
    BASE = 37 + random.randint(0, 106)
    MOD = 998244353 + random.randint(0, 10006)
    P = [0] * (n + 1)
    P[0] = 1
    for i in range(1, n + 1):
        P[i] = P[i - 1] * BASE % MOD
    h = [0] * (n + 1)
    for i in range(1, n + 1):
        h[i] = (h[i - 1] * BASE + ord(word[i - 1]) - ord('a')) % MOD

    def calc(L, R):
        return (h[R] - h[L - 1] * P[R - L + 1] % MOD + MOD) % MOD

    res = 0
    for i in range(0, n, k):
        res += 1  # 删掉前缀，添加后缀
        if i + k < n:
            m = n - (i + k)  # 后缀的长度
            if calc(1, m) == calc(i + k + 1, n):
                break  # 前后缀相等
    return res
