from AlgorithmsCabin.Math.Util.utils import sint, ints

MOD = 10 ** 9 + 7


def cf1466E():
    n = sint()
    a = ints()
    cnt = [0] * 60
    for i in range(60):
        for x in a:
            if x >> i & 1:
                cnt[i] += 1
    ans = 0
    for x in a:
        sm_and = 0
        sm_or = 0
        for i in range(60):
            if x >> i & 1:
                sm_and += cnt[i] << i
                sm_or += n << i
            else:
                sm_or += cnt[i] << i
        ans += sm_and * sm_or % MOD
    print(ans % MOD)
    return
