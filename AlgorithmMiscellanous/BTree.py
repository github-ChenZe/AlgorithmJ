from FlexArray import *
import profile
from Graphing.Pixel import *


BTree_Node_Least_Children = 2
BTree_Node_Least_Key = BTree_Node_Least_Children - 1
BTree_Node_Max_Children = 2 * BTree_Node_Least_Children
BTree_Node_Max_Key = BTree_Node_Max_Children - 1

assert (BTree_Node_Least_Children & 1) == 0


class BTreeNodeArray(FlexArray):
    def __init__(self, capacity, copy_from=None, prototype=None):
        self.node = None
        super(BTreeNodeArray, self).__init__(capacity, copy_from, prototype)

    def adopted(self, node):
        self.node = node

    def __setitem__(self, key, value):
        super(BTreeNodeArray, self).__setitem__(key, value)
        if value is None:
            return
        assert isinstance(self[key], BTreeNode)
        self[key].index = key
        self[key].room = self


class BTreeNode(object):
    def __init__(self):
        """"""
        self.room = None
        self.index = None
        self.keys = SortedArray(BTree_Node_Max_Key)
        self.children = BTreeNodeArray(BTree_Node_Max_Children)
        self.children.adopted(self)

    def switch(self, new_keys, new_children):
        self.keys = new_keys
        assert isinstance(self.children, BTreeNodeArray)
        self.children = new_children
        self.children.adopted(self)

    def parent(self):
        if self.room is None:
            return None
        parent = self.room.node
        if parent is None:
            error("Unintialized node.")
        return parent

    def hang(self, key, left_child, right_child):
        """Initial inserting into an empty node."""
        if not self.is_empty():
            error("Cannot hang to non-empty node.")
        if left_child is None or right_child is None:
            error("Not enough children to insert.")
        self.keys.insert_into_empty(key, 0)
        self.children.insert_into_empty(left_child, 0)
        self.children.insert_into_empty(right_child, 1)

    def insert(self, key, left_child, right_child):
        """Insert key and also corresponding children."""
        if self.is_empty():
            self.hang(key, left_child, right_child)
            return
        if left_child is None and right_child is None:
            error("Children not enough.")
        if left_child is not None and right_child is not None:
            error("Too many children to insert.")
        if self.is_full():
            error("Inserting into an full node.")
        position = self.keys.auto_insert(key)
        if left_child is not None:
            self.children.insert(left_child, position)
        if right_child is not None:
            self.children.insert(right_child, position + 1)

    def brother(self, offset):
        if self.parent() is None:
            error("Getting the brother of root.")
        assert isinstance(self.parent(), BTreeNode)
        if not(0 <= self.index + offset < BTree_Node_Max_Children):
            error("Brother out of range.")
        return self.parent().children[self.index + offset]

    def left_brother(self):
        return self.brother(-1)

    def right_brother(self):
        return self.brother(1)

    def internally_look_for(self, key):
        if self.keys_count() == 0:
            return -1, None
        right_index = self.keys.look_for_first_greater_than(key)
        if self.keys[right_index] == key:
            return right_index, key
        return right_index, None

    def look_for(self, key):
        """recursively looking for keys"""
        index, value = self.internally_look_for(key)
        if value is not None:
            return value
        if index == -1:
            return None
        return self.children[index].look_for(key)

    def tri_split(self):
        """Although leaf nodes do not have children, tri-split is valid for them."""
        left_keys, mid_key, right_keys = self.keys.tri_split_array()
        new_left = self
        new_right = type(self)()
        left_children, right_children = self.children.bi_split_array()

        new_left.switch(left_keys, left_children)
        new_right.switch(right_keys, right_children)

        return new_left, mid_key, new_right

    def full_root_split(self):
        if self.parent() is not None:
            error("Root splitting on an inner node.")
        if not self.is_full():
            error("Root splitting on an non-full node.")

        new_root = BTreeNode()
        new_left, mid_key, new_right = self.tri_split()
        new_root.hang(mid_key, new_left, new_right)
        return new_root

    def full_inner_split(self):
        if self.parent() is None:
            error("Inner splitting on an root node.")
        if not self.is_full():
            error("Inner splitting on an non-full node.")

        assert isinstance(self.parent(), BTreeNode)
        new_left, mid_key, new_right = self.tri_split()
        self.parent().insert(mid_key, None, new_right)
        return mid_key

    def inner_insert_key(self, key):
        if self.is_empty():
            error("Inner inserting on an empty node.")
        if self.is_full():
            error("Inner inserting on an full node.")
        target_index = self.keys.look_for_first_greater_than(key)
        if target_index < self.keys_count() and self.keys[target_index] == key:
            error("Key existed.")
        target_node = self.children[target_index]
        assert isinstance(target_node, BTreeNode)
        if target_node.is_full():
            mid_key = target_node.full_inner_split()
            if mid_key < key:
                target_node = target_node.right_brother()
        target_node.inner_insert_key(key)

    def pop_end(self):
        return self.keys.pop_end(), self.children.pop_end()

    def pop_first(self):
        return self.keys.pop_first(), self.children.pop_first()

    def push_end(self, key, child):
        self.keys.push_end(key)
        self.children.push_end(child)

    def push_first(self, key, child):
        self.keys.push_first(key)
        self.keys.push_end(child)

    def clockwise_rotate(self, key_index):
        left_child = self.children[key_index]
        right_child = self.children[key_index + 1]
        key, child = left_child.pop_end()
        right_child.push_first(self.keys[key_index], child)
        self.keys[key_index] = key

    def counter_clockwise_rotate(self, key_index):
        left_child = self.children[key_index]
        right_child = self.children[key_index + 1]
        key, child = right_child.pop_first()
        left_child.push_end(self.keys[key_index], child)
        self.keys[key_index] = key

    def merge_with_right(self, right_key, right_node):
        self.keys.push_end(right_key)
        self.keys.concat_end(right_node.keys)
        self.children.concat_end(right_node.children)

    def merge_to_left(self, key_index):
        key, child = self.pop_right(key_index)
        self.children[key_index].merge_with_right(key, child)

    def pop_right(self, key_index):
        return self.keys.pop_at(key_index), self.children.pop_at(key_index + 1)

    def pop_left(self, key_index):
        return self.keys.pop_at(key_index), self.children.pop_at(key_index)

    def is_empty(self):
        return self.keys_count() == 0

    def is_full(self):
        return self.keys_count() == BTree_Node_Max_Key

    def keys_count(self):
        return self.keys.count

    def children_count(self):
        return self.children.count

    def brief(self, level):
        print '  ' * level + "Level: %d, Node: keys: %d, Children: %d, Parent: %s." % (level, self.keys_count(), self.children_count(), self.parent())

    def print_self(self, level=0):
        self.brief(level)
        for i in range(0, self.keys_count()):
            self.children[i].print_self(level + 1)
            print '  ' * level + '%d' % self.keys[i]
        self.children[self.keys_count()].print_self(level + 1)

    def __str__(self):
        return self.keys.__str__()

    def to_tree(self, vertices, edges, labels, parent=None):
        my_index = len(vertices)
        vertices.append(my_index)
        if parent is not None:
            edges.append("%d<->%d" % (parent, my_index))
        labels.append("%d->Placed[\"%s\", Center]" % (my_index, self.keys))
        for i in range(0, self.children.count):
            self.children[i].to_tree(vertices, edges, labels, my_index)

    def to_pixel_tree(self):
        self_hotel = self.to_hotel()
        tree = TreeDiagram(root=self.to_hotel())
        for i in range(0, self.children_count()):
            tree.append(self.children[i].to_pixel_tree())
        return tree

    def to_hotel(self):
        keys = ["%d" % key for key in self.keys]
        m = MultiFrameTextDiagram(texts=keys)
        return m


class BTreeLeaf(BTreeNode):
    def __init__(self):
        super(BTreeLeaf, self).__init__()
        self.children.seal()

    def inner_insert_key(self, key):
        assert isinstance(self.keys, SortedArray)
        self.keys.auto_insert(key)

    def look_for(self, key):
        return self.internally_look_for(key)[1]

    def children_count(self):
        return 0

    def brief(self, level):
        print '  ' * level + "Level: %d, Leaf keys: %d, Parent: %s" % (level, self.keys_count(), self.parent())

    def print_self(self, level=0):
        self.brief(level)
        for i in range(0, self.keys_count()):
            print '  ' * level + '%d' % self.keys[i]

    def to_pixel_tree(self):
        return TreeDiagram(root=self.to_hotel())


class BTree(object):
    def __init__(self):
        self.root = BTreeLeaf()

    def look_for(self, key):
        self.root.look_for(key)

    def insert(self, key):
        assert isinstance(self.root, BTreeNode)
        if self.root.is_full():
            self.root = self.root.full_root_split()
        self.root.inner_insert_key(key)

    def print_self(self):
        self.root.print_self()

    def to_tree(self):
        vertices = []
        edges = []
        labels = []
        self.root.to_tree(vertices, edges, labels)
        return edges, labels

    def to_pixel_tree(self):
        return self.root.to_pixel_tree()


def test(n):
    bt = BTree()
    a = [__i__ for __i__ in range(0, n)]
    random.shuffle(a)
    c = 0

    profile.fire()
    for __i__ in a:
        bt.insert(__i__)
        #print '------------------------------------------------------------------------------------------'
        #print '%d: inserted %d' % (c, __i__)
        #bt.print_self()
        c += 1
    # bt.print_self()
    profile.check()
    return bt


def step_test(n):
    bt = BTree()
    a = [__i__ for __i__ in range(0, n)]
    random.shuffle(a)
    for __i__ in a:
        bt.insert(__i__)
        yield bt.to_pixel_tree().render()


def get_tree_PIL():
    bt = test(64)
    # bt.print_self()
    # vt, lb = bt.to_tree()
    # arg_v = "{%s}" % ','.join(vt)
    # arg_l = "{%s}" % ','.join(lb)
    # print "TreeGraph[%s, VertexLabels->%s, PlotTheme -> \"VintageDiagram\"]" % (arg_v, arg_l)
    tree = bt.to_pixel_tree()
    return tree.render()


def ultimate_test():
    bt = test(64)
    tree = bt.to_pixel_tree()
    return tree.canvas_rendering()


if __name__ == '__main__':
    bt = test(64)
    # bt.print_self()
    # vt, lb = bt.to_tree()
    # arg_v = "{%s}" % ','.join(vt)
    # arg_l = "{%s}" % ','.join(lb)
    # print "TreeGraph[%s, VertexLabels->%s, PlotTheme -> \"VintageDiagram\"]" % (arg_v, arg_l)
    tree = bt.to_pixel_tree()
    # tree.render()
    tree.canvas_rendering().show()
