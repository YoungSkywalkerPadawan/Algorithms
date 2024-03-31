# 曼哈顿距离
# 在二维空间内，两个点之间的曼哈顿距离（Manhattan distance）为它们横坐标之差的绝对值与纵坐标之差的绝对值之和。
# A(x1, y1), B(x2, y2) 的曼哈顿距离d(A, B) = |x1 - x2| + |y1 - y2|

# 切比雪夫距离
# 切比雪夫距离（Chebyshev distance）是向量空间中的一种度量，二个点之间的距离定义为其各坐标数值差的最大值。
# 在二维空间内，两个点之间的切比雪夫距离为它们横坐标之差的绝对值与纵坐标之差的绝对值的最大值。
# A(x1, y1), B(x2, y2) 的距离d(A, B) = max(|x1 - x2| ,|y1 - y2|)

# 曼哈顿距离与切比雪夫距离的关系
# 曼哈顿坐标系是通过切比雪夫坐标系旋转 45度 后，再缩小到原来的一半得到的。
# 将一个点 (x,y) 的坐标变为 (x + y, x - y) 后，原坐标系中的曼哈顿距离等于新坐标系中的切比雪夫距离。
# 将一个点 (x,y) 的坐标变为 ((x + y)/2,(x - y)/2) 后，原坐标系中的切比雪夫距离等于新坐标系中的曼哈顿距离。

# 证明
# 设 A(x_1,y_1),B(x_2,y_2)
# A，B的曼哈顿距离d(A, B) = |x1 - x2| + |y1 - y2| = max{x1-x2+y1-y2,x1-x2+y2-y1,x2-x1+y1-y2,x2-x1+y2-71}
# d(A, B)  = max(|(x1+y1)-(x2+y2)|,|(x1-y1)-(x2-y2)|) 即 （x1+y1, x1-y1）,(x2+y2,x2-y2)的切比雪夫距离

# 同理，A，B两点的切比雪夫距离d(A, B) = max(|x1 - x2| ,|y1 - y2|) = |(x1+y1)/2-(x2+y2)/2| + |(x1-y1)/2-(x2-y2)/2|
# 即（(x1+y1)/2，(x1-y1)/2）到 （(x2+y2)/2，(x2-y2)/2）的曼哈顿距离
from typing import List
from sortedcontainers import SortedList
from math import inf


# lc391T4
def minimumDistance(points: List[List[int]]) -> int:
    xs = SortedList()
    ys = SortedList()
    for x, y in points:
        xs.add(x + y)
        ys.add(x - y)
    ans = inf
    for x, y in points:
        xs.remove(x + y)
        ys.remove(x - y)
        ans = min(ans, max(xs[-1] - xs[0], ys[-1] - ys[0]))
        xs.add(x + y)
        ys.add(x - y)
    return ans
