from math import inf
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


#  树上最大独立集：需要从图中选择尽量多的点，使得这些点不相邻
def rob_on_tree(root: Optional[TreeNode]) -> int:
    def dfs(node: Optional[TreeNode]) -> (int, int):
        if not node:
            return 0, 0

        l_rob, l_not_rob = dfs(node.left)
        r_rob, r_not_rob = dfs(node.right)

        rob = node.val + l_not_rob + r_not_rob
        not_rob = max(l_rob, l_not_rob) + max(r_rob, r_not_rob)
        return rob, not_rob

    return max(dfs(root))


# 树上最小支配集: 每个点有两种状态,即属于支配集合或者不属于支配集合
# 其中不属于支配集合时此点还需要被覆盖,被覆盖也有两种状态,即被子节点覆盖或者被父节点覆盖
def minCameraCover(root: Optional[TreeNode]) -> int:
    def dfs(node):
        if node is None:
            return inf, 0, 0  # 空节点不能安装摄像头，也无需被监控到
        l_choose, l_by_fa, l_by_children = dfs(node.left)
        r_choose, r_by_fa, r_by_children = dfs(node.right)
        cur_choose = min(l_choose, l_by_fa) + min(r_choose, r_by_fa) + 1
        cur_by_fa = min(l_choose, l_by_children) + min(r_choose, r_by_children)
        cur_by_children = min(l_choose + r_by_children, l_by_children + r_choose, l_choose + r_choose)
        return cur_choose, cur_by_fa, cur_by_children

    choose, _, by_children = dfs(root)  # 根节点没有父节点
    return min(choose, by_children)
