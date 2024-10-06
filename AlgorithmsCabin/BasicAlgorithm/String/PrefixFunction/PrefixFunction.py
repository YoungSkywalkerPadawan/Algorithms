def prePalindrome(s):
    p = s + '#' + s[::-1]
    pi = [0] * len(p)
    j = 0
    for i in range(1, len(p)):
        while j != 0 and p[j] != p[i]:
            j = pi[j - 1]
        if p[j] == p[i]:
            j += 1
        pi[i] = j
    return s[:j]