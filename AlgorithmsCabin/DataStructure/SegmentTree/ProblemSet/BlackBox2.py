from sortedcontainers import SortedList


class BlackBox:

    def __init__(self, n: int, m: int):
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
        self.groups.append(SortedList())
        # 不断模拟光线的路径，直到走到一个已经遇见过的状态，这样就找到了一个循环
        while not (direction == 1 and self.pos[index][0] != -1) and not (
                direction == -1 and self.neg[index][0] != -1):
            if direction == 1:
                self.pos[index] = (groupId, rank)
                index = (n + m) * 2 - index
            else:
                self.neg[index] = (groupId, rank)
                index = m * 2 - index if index <= m * 2 else (m * 2 + n) * 2 - index
            # 如果小孔不在角上，就改变方向
            if index != 0 and index != m and index != m + n and index != m * 2 + n:
                direction = -direction
            rank += 1

    def open(self, index: int, direction: int) -> int:
        # 插入二元组
        groupId, rank = self.pos[index]
        if groupId != -1:
            store = self.groups[groupId]
            if (rank, index) not in store:
                self.groups[groupId].add((rank, index))
        groupId, rank = self.neg[index]
        if groupId != -1:
            store = self.groups[groupId]
            if (rank, index) not in store:
                self.groups[groupId].add((rank, index))
        # 查询
        groupId, rank = self.pos[index] if direction == 1 else self.neg[index]
        store = self.groups[groupId]
        j = store.bisect_right((rank, index))
        if j < len(store):
            return store[j][1]
        return store[0][1]

    def close(self, index: int) -> None:
        # 删除二元组
        groupId, rank = self.pos[index]
        if groupId != -1:
            self.groups[groupId].remove((rank, index))
        groupId, rank = self.neg[index]
        if groupId != -1:
            self.groups[groupId].remove((rank, index))
