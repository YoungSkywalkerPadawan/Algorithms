import heapq
from heapq import heappush, heappop


def cf730I():
    n, p, s = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    h_a = []
    h_b = []
    h_diff = []
    ans = 0
    g = [0] * n
    for i in range(n):
        heappush(h_a, (-a[i], i))
        heappush(h_b, (-b[i], i))

    # 先选p个
    while p > 0:
        v, i = heappop(h_a)
        heappush(h_diff, (a[i] - b[i], i))
        ans += -v
        g[i] = 1
        p -= 1
    # 再选s个
    while s > 0:
        while g[h_a[0][1]] > 0:
            heappop(h_a)
        while g[h_b[0][1]] > 0:
            heappop(h_b)

        if -h_b[0][0] > -h_a[0][0] - h_diff[0][0]:
            v, index = heappop(h_b)
            ans += -v
            g[index] = 2
        # 反悔
        else:
            v, index = heappop(h_a)
            ans += -v
            g[index] = 1
            v_d, i_d = heappop(h_diff)
            ans += -v_d
            g[i_d] = 2
            heappush(h_diff, (a[index] - b[index], index))
        s -= 1
    print(ans)
    res_a = []
    res_b = []
    for i, x in enumerate(g):
        if x == 1:
            res_a.append(i + 1)
        elif x == 2:
            res_b.append(i + 1)
    print(*res_a)
    print(*res_b)
    return


def cf3D():
    s = list(input())
    h = []
    cnt = ans = 0
    for i, c in enumerate(s):
        if c == '(':
            cnt += 1
            continue
        if c == '?':
            s[i] = ')'
            l, r = map(int, input().split())
            ans += r
            heapq.heappush(h, (l - r, i))

        if cnt > 0:
            cnt -= 1
            continue

        if len(h) == 0:
            print(-1)
            return

        # cnt < 0 反悔，选最小的
        cnt += 1
        v, index = heapq.heappop(h)
        ans += v
        s[index] = '('

    if cnt > 0:
        print(-1)
        return
    print(ans)
    print("".join(s))


def cf1709C():
    s = input()
    # 统计还需要放几个(,）
    tot = len(s) // 2
    c1 = 0
    c2 = 0
    for x in s:
        if x == '(':
            c1 += 1
        elif x == ')':
            c2 += 1

    c1 = tot - c1
    c2 = tot - c2
    flag = False
    # 默认都是(
    cnt = 0
    for x in s:
        if x == '(':
            cnt += 1
        elif x == ')':
            if cnt > 0:
                cnt -= 1
            else:
                # 原先的问号不应该是)
                c2 += 1
                c1 -= 1
                cnt += 1
                flag = False
        else:
            if cnt == 0 or c2 == 0 or flag:
                cnt += 1
                c1 -= 1
            else:
                cnt -= 1
                c2 -= 1
                if c1 > 0:
                    flag = True

    print("YES" if not flag else "NO")
    return
