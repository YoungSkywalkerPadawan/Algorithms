from AlgorithmsCabin.BasicAlgorithm.String.PalindromeString.manacher import manacher
from AlgorithmsCabin.Math.Util.utils import mint


def cf1944D():
    n, q = mint()
    s = input()

    f1 = [0] * n
    f2 = [0] * n
    for i in range(n - 1, -1, -1):
        f1[i] = f1[i + 1] if i + 1 < n and s[i] == s[i + 1] else i + 1
        f2[i] = f2[i + 2] if i + 2 < n and s[i] == s[i + 2] else i + 2

    rad = manacher(s)
    while q > 0:
        q -= 1
        l, r = mint()
        l -= 1
        ans = 0
        cur_l = r - l
        if f1[l] < r:
            mx = (cur_l - 1) - (cur_l - 1) % 2
            ans += (mx // 2) * (mx + 2) // 2
        if f2[l] < r or f2[l + 1] < r:
            mx = cur_l - 1 - cur_l % 2
            ans += ((mx - 1) // 2) * (mx + 3) // 2
        if rad[l + r] <= cur_l:
            ans += cur_l
        print(ans)
    return
