import MyList


class LinkedListNode(object):
    def __init__(self, value, follower=None):
        self.value = value
        self.follower = follower


class LinkedList(MyList.MyList):
    def __init__(self):
        self.head = None
        self.cur = None

    def push(self, value):
        self.head = LinkedListNode(value, self.head)

    def __iter__(self):
        self.cur = self.head
        return self

    def next(self):
        if self.cur is None:
            raise StopIteration
        else:
            current_value = self.cur.value
            self.cur = self.cur.follower
            return current_value


if __name__ == '__main__':
    ls = LinkedList()
    ls.push('a')
    ls.push('ha')
    ls.push('haha')
    for c in ls:
        print c
    print ls
