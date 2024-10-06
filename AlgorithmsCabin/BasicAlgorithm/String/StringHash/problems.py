# 定义一个把字符串映射到整数的函数 f，这个 f 称为是 Hash 函数。
# 这个函数 f 可以方便地帮我们判断两个字符串是否相等。
import random

# lc3031 将单词恢复初始状态所需的最短时间II
from collections import defaultdict

from AlgorithmsCabin.Math.Util.utils import sint


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


def cf1977D():
    n, m = map(int, input().split())
    g = [input() for _ in range(n)]
    rands = [random.getrandbits(64) for _ in range(n)]
    dt = defaultdict(int)
    # 遍历每一列, 统计每一列的0,1的位置,并改变其中一个0,1的值(这样xor后值为1)后的所有0,1的位置的哈希值的个数,最大值极为答案
    # 记录当前位置(i，j),xor序列中只要和改列异或只有1个1 就行,其中这个1就是第i行
    ind = [-1, -1]
    res = 0
    for j in range(m):
        sm = 0
        for i in range(n):
            if g[i][j] == '1':
                sm ^= rands[i]

        for i in range(n):
            dt[sm ^ rands[i]] += 1
            if dt[sm ^ rands[i]] > res:
                res = dt[sm ^ rands[i]]
                ind = [i, j]
    print(res)
    ans = ['0'] * n
    j = ind[1]
    for i in range(n):
        if i != ind[0] and g[i][j] == '1':
            ans[i] = '1'
        if i == ind[0] and g[i][j] == '0':
            ans[i] = '1'
    print("".join(ans))
    return


def cf1363C():
    MOD1 = 998244353
    MOD2 = 10 ** 9 + 7
    s = input()
    a = list(map(int, input()))
    k = sint()
    res = [1 - a[ord(c) - ord('a')] for c in s]

    st = set()
    n = len(s)
    b1 = 27
    b2 = 13331

    for i in range(n):
        c = 0
        hash1 = hash2 = 0
        for j in range(i, n):
            c += res[j]
            if c > k:
                break
            hash1 = (hash1 * b1 + (ord(s[j]) - 96)) % MOD1
            hash2 = (hash2 * b2 + (ord(s[j]) - 96)) % MOD2
            st.add((hash1, hash2))

    print(len(st))

    return
