from AlgorithmsCabin.Math.Util.utils import sint, ints
from types import GeneratorType


def bootstrap(f, stack=None):
    if stack is None:
        stack = []

    def func(*args, **kwargs):
        if stack:
            return f(*args, **kwargs)
        else:
            to = f(*args, **kwargs)
            while True:
                if type(to) is GeneratorType:
                    stack.append(to)
                    to = next(to)
                else:
                    stack.pop()
                    if not stack:
                        break
                    to = stack[-1].send(to)
            return to

    return func


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


def cf1913D():
    n = sint()
    a = ints()
    left = [-1] * n
    right = [-1] * n

    stack = []
    for i in range(n):
        x = a[i]
        idx = -1
        while len(stack) and a[stack[-1]] > x:
            new_idx = stack.pop()
            right[new_idx] = idx
            idx = new_idx
        if idx != -1:
            left[i] = idx
        stack.append(i)

    idx = -1
    while len(stack):
        new_idx = stack.pop()
        right[new_idx] = idx
        idx = new_idx
    dp = [0] * n
    root = a.index(min(a))

    @bootstrap
    def dfs(o: int, f: int):
        l = left[o]
        r = right[o]
        ll = rr = 1
        if l >= 0:
            yield dfs(l, f | 1)
            ll = dp[l]
        if r >= 0:
            yield dfs(r, f | 2)
            rr = dp[r]

        dp[o] = ll * rr
        if f & 1:
            dp[o] += ll
        if f & 2:
            dp[o] += rr
        if f == 3:
            dp[o] -= 1
        dp[o] %= MOD
        yield

    dfs(root, 0)
    print(dp[root])
    return
