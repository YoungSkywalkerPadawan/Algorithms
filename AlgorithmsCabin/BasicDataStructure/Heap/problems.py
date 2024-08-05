from heapq import heappop, heapify, heappush

from AlgorithmsCabin.Math.Util.utils import mint


def cf1945A():
    n = int(input())
    v = list(map(int, input().split()))
    a = list(map(int, input().split()))
    h = []
    for i, x in enumerate(v):
        h.append((-x, i))
    heapify(h)
    ans = 0
    res = 0
    cnt = [0] * n
    vis = [0] * n
    c = 0
    mn = -1
    for i in range(1, (n + 1) // 2 + 1):
        # 取 i个,放弃i-1个
        if (i - 1) > 0:
            c -= cnt[a[i - 2] - 1]
            vis[a[i - 2] - 1] = 1
        while c < i:
            cur_v, cur_p = heappop(h)
            cur_v = -cur_v
            if vis[cur_p] == 0:
                c += 1
                cnt[cur_p] += 1
                mn = cur_v
        cur = i * mn
        if cur > ans:
            ans = cur
            res = i

    print(ans, res)

    return


def cf1946E():
    n, d = mint()
    k, s = [0] * n, [0] * n
    for i in range(n):
        k[i], s[i] = mint()
    cnt = 0
    eat = []
    h = []
    suf = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suf[i] = max(k[i], suf[i + 1])
    for t in range(1, d + 1):
        while eat and eat[0][0] < t:
            i = heappop(eat)[1]
            heappush(h, (-k[i], t, s[i], i))

        if h and suf[cnt] < -h[0][0]:
            i = heappop(h)[-1]
        else:
            i = cnt
            cnt += 1

        if cnt == n:
            print(t)
            return

        heappush(eat, (t + s[i], i))
    print(-1)
    return
