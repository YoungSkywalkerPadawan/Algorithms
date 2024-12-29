# 狄尔沃斯定理, 亦称偏序集分解定理
# 对于任意有限偏序集,其最大反链中元素的数目必等于最小链划分中链的数目.
# 对偶形式也成立:对于任意有限偏序集,其最长链中元素的数目必等于其最小反链划分中反链的数目.
# 这个定理的理解可以是这样的:对于一个偏序集来说，最大反链的元素个数等于划分成全序集最小个数.
import sys

from AlgorithmsCabin.Math.Util.utils import mint


def myPrint(s):
    sys.stdout.write(s + '\n')
    sys.stdout.flush()


def query(mode, out):
    if mode:
        myPrint("! " + ' '.join(map(str, out)))
    else:
        myPrint("? " + ' '.join(map(str, out)))
        res = input().rstrip()
        if res == '-1':
            exit()
        return int(res == "YES")


def cf1977E():
    n = int(input())
    res0 = []
    res1 = []
    res2 = []
    for i in range(n):
        if not res0:
            res0.append(i)
            continue
        if not res1:
            if query(0, (res0[-1] + 1, i + 1)):
                res0.append(i)
            else:
                res1.append(i)
            continue
        # 0,1列表都有元素了,需要询问了
        # 先看有没有公共元素
        if res2:
            if query(0, (res2[-1] + 1, i + 1)):
                res2.append(i)
            else:
                if query(0, (res0[-1] + 1, i + 1)):
                    # 0可达
                    res0.append(i)
                    res1 += res2
                    res2 = []
                else:
                    # 1可达
                    res1.append(i)
                    res0 += res2
                    res2 = []
        else:
            catch0 = query(0, (res0[-1] + 1, i + 1))
            catch1 = query(0, (res1[-1] + 1, i + 1))
            if catch0 and catch1:
                # 0, 1可达
                res2.append(i)
                continue

            if catch0:
                # 0可达
                res0.append(i)
            else:
                res1.append(i)

    ans = [0] * n
    for x in res1:
        ans[x] = 1
    query(1, ans)
    return


def cf2048E():
    n, m = mint()
    if m >= 2 * n:
        print("NO")
        return
    print("YES")
    for i in range(2 * n):
        res = []
        for j in range(m):
            res.append(((i + j) % (2 * n)) // 2 + 1)
        print(*res)

    return
