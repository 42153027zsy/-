from typing import List
from collections import namedtuple
import time


class Point(namedtuple("Point", "x y")):
    def __repr__(self) -> str:
        return f'Point{tuple(self)!r}'


class Rectangle(namedtuple("Rectangle", "lower upper")):
    def __repr__(self) -> str:
        return f'Rectangle{tuple(self)!r}'

    def is_contains(self, p: Point) -> bool:
        return self.lower.x <= p.x <= self.upper.x and self.lower.y <= p.y <= self.upper.y


class Node(namedtuple("Node", "location left right")):
    """
    location: Point
    left: Node
    right: Node
    """

    def __repr__(self):
        return f'{tuple(self)!r}'


class KDTree:
    """k-d tree"""

    def __init__(self):
        self._root = None
        self._n = 0

    def insert(self, p: List[Point], depth):   #eastablish KD tree 创建kd树，返回根结点
        if (len(p) > 0):    #if length of p is a positive number 若list长度大于0
            m, n = np.shape(p)    #Take the sample row, the column, and index the one dimensional and two dimensional values of each point (求出样本行，列，索引出每个点的一维与二维的值)
            midIndex = int(m / 2) #Find the index of the middle number, where one dimension is the starting point (找到中间数的索引位置，这里一一维为起点)
            axis = depth % n    #Determining which axis to divide the data on is equivalent to changing the next dimension in the next section (判断以哪个轴划分数据，相当于在下一部分更改下一维度)
            sortedp = self.sort(p, axis) #Sort and reset the out-of-order points in the selected dimension to ordered points (进行排序，将该选取维度下的乱序点重置为有序点)
            node = Node(sortedp[midIndex]) #Sets the node data field to the median (将节点数据域设置为中位数)
            leftp = sortedp[: midIndex] #Create a 2-change copy to the left of the median (将中位数的左边创建2改副本)
            rightp= sortedp[midIndex+1 :]#Create a copy to the right of the median (中位数的右边创建副本)
            print(leftp)
            print(rightp)
            node.left = self.insert(leftp, depth+1) #Pass in the left sample of the median to create the tree recursively (将中位数左边样本传入来递归创建树)
            node.rchild = self.insert(rightp, depth+1)#Pass in the right sample of the median to create the tree recursively(将中位数右边样本传入来递归创建树)
            return node
        else:
            return None


    def range(self, rectangle: Rectangle) :
        lowerx=rectangle.lower.x
        upperx=rectangle.upper.x
        lowery=rectangle.lower.y
        uppery=rectangle.upper.y     #Find the upper, lower, left and right ranges of the region respectively （分别找到该区域的上下左右区域范围）
        result=[]
        walk=self._root
        if lowerx<=walk.x<=upperx and lowery<=walk.y<=uppery:   #The two dimensions are retrieved successively from the KD tree, and the points matching the conditions of the region are searched and placed in the result（从KD tree中依次对两个维度进行检索，查找符合区域条件的点并放在result中）
            result.append(walk)
        elif lowerx>= walk.x:
            walk=walk.left
        else:
            walk=walk.right
        return result

def range_test():
    points = [Point(7, 2), Point(5, 4), Point(9, 6), Point(4, 7), Point(8, 1), Point(2, 3)]
    kd = KDTree()
    kd.insert(points)
    result = kd.range(Rectangle(Point(0, 0), Point(6, 6)))
    assert sorted(result) == sorted([Point(2, 3), Point(5, 4)])


def performance_test():
    points = [Point(x, y) for x in range(1000) for y in range(1000)]

    lower = Point(500, 500)
    upper = Point(504, 504)
    rectangle = Rectangle(lower, upper)
    #  naive method
    start = int(round(time.time() * 1000))
    result1 = [p for p in points if rectangle.is_contains(p)]
    end = int(round(time.time() * 1000))
    print(f'Naive method: {end - start}ms')

    kd = KDTree()
    kd.insert(points)
    # k-d tree
    start = int(round(time.time() * 1000))
    result2 = kd.range(rectangle)
    end = int(round(time.time() * 1000))
    print(f'K-D tree: {end - start}ms')

    assert sorted(result1) == sorted(result2)


if __name__ == '__main__':
    range_test()
    performance_test()