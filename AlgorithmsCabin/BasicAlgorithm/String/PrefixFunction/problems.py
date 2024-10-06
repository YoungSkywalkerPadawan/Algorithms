from AlgorithmsCabin.BasicAlgorithm.String.PrefixFunction.PrefixFunction import prePalindrome


def cf1326D():
    s = input()
    n = len(s)
    if s == s[::-1]:
        print(s)
        return

    l, r = 0, n - 1
    while s[l] == s[r]:
        l += 1
        r -= 1
    new_s = s[l:r + 1]
    pre, suf = prePalindrome(new_s), prePalindrome(new_s[::-1])
    if len(pre) >= len(suf):
        print(s[:l] + pre + s[r + 1:])
    else:
        print(s[:l] + suf + s[r + 1:])

    return
