# 凸多边形
# 指所有内角大小都在 [0,π] 范围内的 简单多边形
# 凸包
# 在平面上能包含所有给定点的最小凸多边形叫做凸包。
# Andrew 算法 O（nlogn）
# 首先把所有点以横坐标为第一关键字，纵坐标为第二关键字排序。排序后最小的元素和最大的元素一定在凸包上
# 因为是凸多边形，如果从一个点出发逆时针走，轨迹总是「左拐」的，一旦出现右拐，就说明这一段不在凸包上。可以用一个单调栈来维护上下凸壳。
# 从左向右看，上下凸壳所旋转的方向不同，为了让单调栈起作用，我们首先 升序枚举 求出下凸壳，然后 降序 求出上凸壳。
from collections import deque
from typing import List


# lc587 安装栅栏
def outerTrees(trees: List[List[int]]) -> List[List[int]]:
    def cross(p: List[int], q: List[int], r: List[int]) -> int:
        return (q[0] - p[0]) * (r[1] - q[1]) - (q[1] - p[1]) * (r[0] - q[0])

    n = len(trees)
    if n < 4:
        return trees

    trees.sort()
    dq = deque([0])  # 需要入栈两次，不标记
    used = [False] * n
    # 求凸包下半部分
    for i in range(1, n):
        while len(dq) > 1 and cross(trees[dq[-2]], trees[dq[-1]], trees[i]) < 0:
            used[dq.pop()] = False
        dq.append(i)
        used[i] = True

    # 求凸包上半部分
    m = len(dq)
    for i in range(n - 2, -1, -1):
        if not used[i]:
            while len(dq) > m and cross(trees[dq[-2]], trees[dq[-1]], trees[i]) < 0:
                used[dq.pop()] = False
            dq.append(i)
            used[i] = True
    dq.pop()
    return [trees[i] for i in dq]


# LCP15 游乐园的迷宫
def visitOrder(points: List[List[int]], direction: str) -> List[int]:
    def cross(p: List[int], q: List[int], r: List[int]) -> int:
        return (q[0] - p[0]) * (r[1] - q[1]) - (q[1] - p[1]) * (r[0] - q[0])

    n = len(points)
    m = 0
    for i in range(1, n):
        if points[i][0] < points[m][0]:
            m = i
    dq = deque([m])
    vis = [0] * n
    vis[m] = 1

    for i in range(n - 2):
        q_ = -1
        for j in range(n):
            if vis[j]:
                continue
            if q_ == -1:
                q_ = j
            else:
                if direction[i] == 'L':
                    if cross(points[dq[-1]], points[q_], points[j]) < 0:
                        q_ = j
                else:
                    if cross(points[dq[-1]], points[q_], points[j]) > 0:
                        q_ = j
        vis[q_] = 1
        dq.append(q_)
    for i in range(n):
        if not vis[i]:
            dq.append(i)
    return list(dq)
