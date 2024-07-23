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
