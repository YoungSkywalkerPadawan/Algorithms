from collections import defaultdict
from string import ascii_lowercase
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


def cf954I():
    s = input()
    t = input()
    m = len(t)
    ans = [0] * (len(s) - m + 1)
    mp = defaultdict()
    mp['g'] = 0

    @bootstrap
    def dfs(c, sz):
        if c == 'g':
            pi = [0] * m
            j = 0
            for i in range(1, m):
                v = mp[t[i]]
                while j > 0 and mp[t[j]] != v:
                    j = pi[j - 1]
                if mp[t[j]] == v:
                    j += 1
                pi[i] = j

            j = 0
            for i in range(len(s)):
                v = mp[s[i]]
                while j > 0 and mp[t[j]] != v:
                    j = pi[j - 1]
                if mp[t[j]] == v:
                    j += 1
                if j == m:
                    st = i - m + 1
                    ans[st] = ans[st] if ans[st] > sz else sz
                    j = pi[j - 1]
            yield

        mp[c] = sz
        yield dfs(ascii_lowercase[ord(c) - ord('a') + 1], sz + 1)
        for i in range(sz):
            mp[c] = i
            yield dfs(ascii_lowercase[ord(c) - ord('a') + 1], sz)
        yield

    dfs('a', 0)

    for x in ans:
        print(6 - x)
    return
