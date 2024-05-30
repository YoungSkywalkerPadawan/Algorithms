from AlgorithmsCabin.DataStructure.SegmentTree.SegmentTree3 import SegmentTree


class BlackBox:

    def __init__(self, n: int, m: int):
        self.dict = {}  # 记录每个线段树的n
        self.pos, self.neg, self.groups = [], [], []
        tot = (n + m) * 2
        self.pos, self.neg = [(-1, -1) for _ in range(tot)], [(-1, -1) for _ in range(tot)]
        for i in range(tot):
            # 如果不是左上角或者右下角的小孔，那么从 y=x 方向射出找循环
            if i != 0 and i != m + n and self.pos[i][0] == -1:
                self.createGroup(n, m, i, 1)
            # 如果不是左下角或者右上角的小孔，那么从 y=-x 方向射出找循环
            if i != m and i != m * 2 + n and self.neg[i][0] == -1:
                self.createGroup(n, m, i, -1)

    def createGroup(self, n: int, m: int, index: int, direction: int):
        groupId = len(self.groups)
        rank = 0
        res = [index]
        # 不断模拟光线的路径，直到走到一个已经遇见过的状态，这样就找到了一个循环
        while not (direction == 1 and self.pos[index][0] != -1) and not (
                direction == -1 and self.neg[index][0] != -1):
            if direction == 1:
                self.pos[index] = (groupId, rank)
                index = (n + m) * 2 - index
                res.append(index)
            else:
                self.neg[index] = (groupId, rank)
                index = m * 2 - index if index <= m * 2 else (m * 2 + n) * 2 - index
                res.append(index)
            # 如果小孔不在角上，就改变方向
            if index != 0 and index != m and index != m + n and index != m * 2 + n:
                direction = -direction
            rank += 1
        self.dict[groupId] = len(res)
        st = SegmentTree(len(res), res)
        st.build(1, 1, len(res))
        self.groups.append(st)

    def open(self, index: int, direction: int) -> int:
        # 将对应索引的值更新为1，表示打开
        groupId, rank = self.pos[index]
        if groupId != -1:
            self.groups[groupId].update(1, 1, self.dict[groupId], rank + 1, 1)
        groupId, rank = self.neg[index]
        if groupId != -1:
            self.groups[groupId].update(1, 1, self.dict[groupId], rank + 1, 1)
        # 查询，先查询索引右边，再查询左部
        groupId, rank = self.pos[index] if direction == 1 else self.neg[index]
        j = self.groups[groupId].BinaryQuery(1, 1, self.dict[groupId], rank + 2, 1)
        if j >= 0:
            return j
        return self.groups[groupId].BinaryQuery2(1, 1, self.dict[groupId], rank + 1, 1)

    def close(self, index: int) -> None:
        # 将对应索引的值更新为0，表示关闭
        groupId, rank = self.pos[index]
        if groupId != -1:
            self.groups[groupId].update(1, 1, self.dict[groupId], rank + 1, 0)
        groupId, rank = self.neg[index]
        if groupId != -1:
            self.groups[groupId].update(1, 1, self.dict[groupId], rank + 1, 0)
