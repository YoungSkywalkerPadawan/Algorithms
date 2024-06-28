MOD = 10 ** 9 + 7


def cal(x):
    return (x * (x + 1) // 2) % MOD


def cf1982E():
    n, k = map(int, input().split())

    def dfs(x: int, y: int) -> tuple:
        m = x.bit_length()
        if m <= y:
            return x + 1, x + 1, cal(x + 1)
        if x == 0:
            return 1, 1, cal(1)
        if y == 0:
            return 1, 0, cal(1)

        m -= 1
        l1, r1, ans1 = dfs((1 << m) - 1, y)
        l2, r2, ans2 = dfs(x - (1 << m), y - 1)
        ans1 -= cal(r1)
        ans2 -= cal(l2)
        res = ans1 + ans2 + cal(r1 + l2)
        res = res % MOD
        if l1 == 1 << m and l2 == x - (1 << m) + 1:
            return l1 + l2, l1 + l2, res
        elif l1 == 1 << m:
            return l1 + l2, r2, res
        elif l2 == x - (1 << m) + 1:
            return l1, r1 + l2, res

        else:
            return l1, r2, res

    ans = dfs(n - 1, k)[-1]
    print(ans)
    return
