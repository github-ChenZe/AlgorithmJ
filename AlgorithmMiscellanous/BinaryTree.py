from LinkedList import LinkedList
from random import randint
import time


class BinaryTreeNode(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

    def right_add(self, node):
        self.right = node
        node.parent = self

    def left_add(self, node):
        self.left = node
        node.parent = self

    def add(self, value):
        if value > self.value:
            if self.right is None:
                self.right_add(BinaryTreeNode(value))
            else:
                self.right.add(value)
        if value < self.value:
            if self.left is None:
                self.left_add(BinaryTreeNode(value))
            else:
                self.left.add(value)

    def flatten(self, flattened):
        if self.right is not None:
            self.right.flatten(flattened)
        flattened.push(self.value)
        if self.left is not None:
            self.left.flatten(flattened)
        return flattened


class BinaryTree(object):
    def __init__(self):
        self.root = None

    def add(self, value):
        if self.root is None:
            self.root = BinaryTreeNode(value)
        else:
            self.root.add(value)

    def to_linked_list(self):
        if self.root is None:
            return None
        else:
            return self.root.flatten(LinkedList())


if __name__ == "__main__":
    while 1:
        bt = BinaryTree()
        length = eval(raw_input())
        sum = 0
        for i in range(0, 10):
            start = time.time()
            for i in range(0, length):
                bt.add(randint(0, 1000000))
            end = time.time()
            sum += end-start
        print sum/10
