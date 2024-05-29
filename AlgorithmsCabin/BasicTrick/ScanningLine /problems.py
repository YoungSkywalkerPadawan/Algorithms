from typing import List


# lc850 矩形面积II
def rectangleArea(rectangles: List[List[int]]) -> int:
    st = set()
    for x, _, y, _ in rectangles:
        st.add(x)
        st.add(y)

    nums = sorted(list(st))
    ans = 0
    for i in range(len(nums) - 1):
        x1, x2 = nums[i], nums[i + 1]

        w = x2 - x1
        arr = [(r[1], r[3]) for r in rectangles if r[0] < x2 and r[2] > x1]
        arr.sort(key=lambda p: [p[0], -p[1]])
        height = l = h = 0
        for y1, y2 in arr:
            if y1 >= h:
                height += h - l
                l, h = y1, y2
            else:
                h = max(h, y2)
        height += h - l
        ans += height * w % (10 ** 9 + 7)
    return ans % (10 ** 9 + 7)
