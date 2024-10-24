from AlgorithmsCabin.Math.Util.utils import sint, ints, mint


def cf1995C():
    n = int(input())
    a = list(map(int, input().split()))
    cnt = 0
    ans = 0
    for i in range(1, n):
        if a[i] == a[i - 1]:
            ans += cnt
        elif a[i] < a[i - 1]:
            if a[i] == 1:
                print(-1)
                return
            cur = a[i]
            while cur < a[i - 1]:
                cur = cur * cur
                cnt += 1
            ans += cnt
        else:
            cur = a[i - 1]
            if cnt > 0:
                while cur <= a[i] and cnt > 0:
                    cnt -= 1
                    cur = cur * cur
                if a[i] < cur:
                    cnt += 1
            ans += cnt
    print(ans)
    return


def cf1954E():
    n = sint()
    a = ints()
    mx = max(a)
    cnt = [0] * (mx + 1)
    # a[0] 首先需要操作1
    cnt[a[0]] += 1

    for i in range(1, n):
        if a[i] > a[i - 1]:
            cnt[a[i]] += 1
            cnt[a[i - 1]] -= 1

    # 计算前缀和,方便后续按k增加汇总
    for i in range(1, mx + 1):
        cnt[i] += cnt[i - 1]
    ans = []
    for k in range(1, mx + 1):
        res = 0
        for i in range(1, mx + 1, k):
            # 计算[i,i+k-1]的这些数需要的总时间
            res += ((i - 1) // k + 1) * (cnt[min(i + k - 1, mx)] - cnt[i - 1])
        ans.append(res)
    print(*ans)
    return


def cf2030D():
    n, q = mint()
    a = ints()
    s = list(input())
    pre = [0] * n
    pre[0] = a[0]
    bad = [0] * n
    for i in range(1, n):
        pre[i] = max(pre[i - 1], a[i])
        if pre[i - 1] != i:
            bad[i] = 1

    cnt = 0
    for i in range(1, n):
        if bad[i] == 1 and "".join(s[i - 1:i + 1]) == "LR":
            cnt += 1

    for _ in range(q):
        x = sint()
        x -= 1
        if bad[x] == 1 and "".join(s[x - 1:x + 1]) == "LR":
            cnt -= 1
        if bad[x + 1] == 1 and "".join(s[x:x + 2]) == "LR":
            cnt -= 1

        s[x] = 'L' if s[x] == 'R' else 'R'
        if bad[x] == 1 and "".join(s[x - 1:x + 1]) == "LR":
            cnt += 1
        if bad[x + 1] == 1 and "".join(s[x:x + 2]) == "LR":
            cnt += 1
        print("YES" if cnt == 0 else "NO")

    return
