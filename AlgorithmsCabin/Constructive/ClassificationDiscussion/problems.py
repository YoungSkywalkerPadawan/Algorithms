from itertools import permutations
from math import factorial

from AlgorithmsCabin.Math.Util.utils import mint


def cf1966D():
    n, k = map(int, input().split())
    # 分为左右两块

    # 如果k = 1
    # 则从2开始 [2, reach] => reach + 1 => [2, reach+1], [reach + 3, 2*reach +1]
    # 缺少 reach + 2 => 补上reach +2 => [2, 2*reach +3] [2*reach+5,reach * 3 + 3]
    # 缺少 2 * reach +4 => [2, 4 * reach + 7] [4*reach +9, 5 * reach + 7]
    # 缺少 4 * reach +8 => [2, 8 * reach + 15]
    res = []
    if k == 1:
        res.append(2)
        res.append(3)
        sl = 1
        reach = sl * 4 - 1
        while reach < n:
            res.append(reach + 1)
            sl *= 2
            reach = sl * 4 - 1
        print(len(res))
        print(*res)
        return

    # 先构造左边
    reach = 0
    while reach + 1 < k:
        if 2 * reach + 1 < k:
            res.append(reach + 1)
            reach = 2 * reach + 1
        else:
            res.append(k - 1 - reach)
            reach = k

    # 开始右半边
    reach = k
    # 左边包含(1,k-1),右边不能有(1,k-1) 从k+1开始，注意reach
    # [1, k-1] => k+1 => [1, k-1][k+1,2*k]
    # 2 * k + 1 => [1, 3*k] [3*k+2, 4*k+1]
    # 3 * k + 1 => [1, 6*k+1]
    # 6 * k + 2 => [1, 12 * k+3]
    # 12 * k  + 4 => [1, 24*k + 7]
    if reach == n:
        print(len(res))
        print(*res)
        return

    res.append(reach + 1)
    reach = 2 * k

    if reach >= n:
        print(len(res))
        print(*res)
        return

    res.append(reach + 1)
    reach = 3 * k
    sl = 3
    while reach < n:
        res.append(reach + 1)
        reach = (sl * k + sl // 3) * 2 - 1
        sl *= 2
    print(len(res))
    print(*res)
    return


def cf1966D2():
    n, k = map(int, input().split())
    i = 0
    while (1 << (i + 1)) <= k:
        i = i + 1

    ans = [k - (1 << i), k + 1, k + 1 + (1 << i)]

    for j in range(20):
        if j != i:
            ans.append(1 << j)

    print(len(ans))
    print(*ans)


def cf2034E():
    n, k = mint()
    ans = []
    if n % 2 == 0:
        if k % 2:
            print("NO")
            return
        else:
            if n >= 10 or k <= factorial(n):
                print("YES")
                cnt = 0
                for p in permutations(range(1, n + 1)):
                    cnt += 2
                    ans.append(' '.join(map(str, p)))
                    ans.append(' '.join(str(n + 1 - x) for x in p))
                    if cnt == k:
                        break
            else:
                print("NO")
                return
    else:
        if n == 1:
            if k == 1:
                print("YES")
                ans.append('1')
            else:
                print("NO")
                return
        else:
            if k == 1:
                print("NO")
                return
            elif n <= 9 and (k == factorial(n) - 1 or k > factorial(n)):
                print("NO")
                return
            else:
                print("YES")
                if k % 2 == 0:
                    cnt = 0
                    for p in permutations(range(1, n + 1)):
                        cnt += 2
                        ans.append(' '.join(map(str, p)))
                        ans.append(' '.join(str(n + 1 - x) for x in p))
                        if cnt == k:
                            break
                else:
                    v = [[] for _ in range(3)]
                    v[0] = list(range(1, n + 1))
                    v[1] = list(range(n // 2 + 1, n + 1)) + list(range(1, n // 2 + 1))
                    v[2] = [3 * (n + 1) // 2 - v[0][i] - v[1][i] for i in range(n)]
                    ans.append(' '.join(map(str, v[0])))
                    ans.append(' '.join(map(str, v[1])))
                    ans.append(' '.join(map(str, v[2])))
                    k -= 3
                    cnt = 0
                    for p in permutations(range(1, n + 1)):
                        flg = True
                        for i in range(3):
                            vs = [p[j] + v[i][j] for j in range(n)]
                            flg1 = True
                            for j in range(1, n):
                                if vs[j] != vs[j - 1]:
                                    flg1 = False
                            if flg1:
                                flg = False
                                break
                            vs = [p[j] - v[i][j] for j in range(n)]
                            flg1 = True
                            for j in range(1, n):
                                if vs[j] != vs[j - 1]:
                                    flg1 = False
                            if flg1:
                                flg = False
                                break
                        if not flg:
                            continue
                        if cnt == k:
                            break
                        cnt += 2
                        ans.append(' '.join(map(str, p)))
                        ans.append(' '.join(str(n + 1 - x) for x in p))
    for x in ans:
        print(x)
    return
