# 离线查询：通过改变回答询问的顺序，使问题更容易处理
# 相应的，在线算法就是按照输入的顺序处理，来一个处理一个
from math import inf
from typing import List
from sortedcontainers import SortedList


# lc1847 最近的房间
def closestRoom(rooms: List[List[int]], queries: List[List[int]]) -> List[int]:
    # 离线查询
    n = len(rooms)
    rooms.sort(key=lambda v: -v[1])
    m = len(queries)
    ans = [-1] * m
    sl = SortedList((-inf, inf))
    j = 0
    for i, (p, s) in sorted(enumerate(queries), key=lambda v: -v[1][1]):

        while j < n and rooms[j][1] >= s:
            sl.add(rooms[j][0])
            j += 1
        if len(sl) > 2:
            idx = sl.bisect_left(p)
            val = sl[idx] - p
            cur = sl[idx]
            val2 = p - sl[idx - 1]
            if val2 <= val:
                cur = sl[idx - 1]
            ans[i] = cur
    return ans
