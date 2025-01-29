from collections import defaultdict, Counter
from typing import List

from AlgorithmsCabin.DataStructure.UnionFind.UnionFind2 import UnionFind
from AlgorithmsCabin.Math.Util.utils import mint

MOD = 10 ** 9 + 7


def cf1983F():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    ans = 0
    f = [n] * n
    for d in range(29, -1, -1):
        p = defaultdict()
        nf = f.copy()
        for i in range(n):
            cur = (a[i] ^ ans) >> d
            if cur in p.keys():
                j = p[cur]
                if nf[j] > i:
                    nf[j] = i
            p[a[i] >> d] = i

        for i in range(n - 2, -1, -1):
            if nf[i] > nf[i + 1]:
                nf[i] = nf[i + 1]

        sm = 0
        for i in range(n):
            sm += n - nf[i]

        if sm < k:
            ans |= (1 << d)
            for i, x in enumerate(nf):
                f[i] = x

    print(ans)
    return


def cf241B():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    ans = 0
    mask = 0
    for d in range(29, -1, -1):
        p = Counter()
        mask |= 1 << d
        cnt = 0
        for i in range(n):
            cur = (a[i] ^ mask) >> d
            cnt += p[cur]
            p[a[i] >> d] += 1

        # 需要里面细分了
        if cnt <= m:
            p1 = Counter()
            p2 = defaultdict()
            for i in range(n):
                cur = (a[i] ^ mask) >> d
                if p1[cur] > 0:
                    for j in range(d):
                        ans += (1 << j) * abs(((a[i] >> j) & 1) * p1[cur] - p2[cur][j])
                    ans += mask * p1[cur]
                    ans %= MOD
                cur = a[i] >> d
                p1[cur] += 1
                if cur not in p2.keys():
                    p2[cur] = Counter()
                for j in range(d):
                    p2[cur][j] += (a[i] >> j) & 1
            m -= cnt
            mask ^= 1 << d

    ans += m * mask
    ans %= MOD
    print(ans)
    return


# lc3022 给定操作次数内使剩余元素的或值最小
def minOrAfterOperations(nums: List[int], k: int) -> int:
    ans = mask = 0
    for b in range(max(nums).bit_length() - 1, -1, -1):
        mask |= 1 << b
        cnt = 0
        and_res = -1
        for x in nums:
            and_res &= x & mask
            if and_res:
                cnt += 1
            else:
                and_res = -1
        if cnt > k:
            ans |= 1 << b
            mask ^= 1 << b
    return ans


def cf1624G():
    input()
    n, m = mint()
    edges = []
    for _ in range(m):
        u, v, w = mint()
        u -= 1
        v -= 1
        edges.append((u, v, w))

    ans = 0
    msk = 0
    for i in range(29, -1, -1):
        uf = UnionFind(n)
        for u, v, w in edges:
            if ((msk | (1 << i)) & w) == 0:
                uf.union(u, v)

        if uf.part != 1:
            ans |= 1 << i
        else:
            msk |= 1 << i

    print(ans)
    return
