from AlgorithmsCabin.Math.Util.utils import sint, ints

mod = 10 ** 9 + 7
inv = pow(10 ** 4, -1, mod)


def cf2020E():
    n = sint()
    a = ints()
    p = ints()
    prob = [x * inv % mod for x in p]
    ans = 0
    # (a + b + c) ^ 2 = a ^ 2 + b ^ 2 + c ^ 2 + 2ab + 2ac + 2bc
    for i in range(10):
        for j in range(i, 10):
            dp = [0] * 4
            dp[0] = 1
            ndp = [0] * 4
            for k in range(n):
                v = (a[k] >> i & 1) * 2 + (a[k] >> j & 1)
                for idx in range(4):
                    ndp[idx] = (dp[idx] * (1 - prob[k]) % mod + dp[idx ^ v] * prob[k] % mod) % mod
                for idx in range(4):
                    dp[idx] = ndp[idx]
                    ndp[idx] = 0
            ans += (1 << (i + j)) * dp[3] % mod * (2 if i != j else 1) % mod
            ans %= mod
    print(ans)
    return
