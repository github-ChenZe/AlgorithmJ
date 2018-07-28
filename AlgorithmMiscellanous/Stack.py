from error import error
import MyList


class Stack(MyList.MyList):
    def __init__(self):
        self.capacity = 16
        self.array = [None] * self.capacity
        self.length = 0
        self.cur = 0

    def __iter__(self):
        self.cur = 0
        return self

    def next(self):
        if self.cur == self.length:
            raise StopIteration
        else:
            current_element = self.array[self.cur]
            self.cur += 1
            return current_element

    def push(self, value):
        index = self.length
        self.length += 1
        if self.length > self.capacity:
            self.capacity *= 2
            new_array = [None] * self.capacity
            self.array = self.copy(self.array, new_array)
        self.array[index] = value

    def pop(self):
        self.length -= 1
        if self.length < 0:
            error("Error pop: empty stack.")
        return self.array[self.length]

    def top(self):
        if self.length <= 0:
            error("Error top: empty stack.")
        return self.array[self.length - 1]


if __name__ == '__main__':
    ls = Stack()
    ls.push('a')
    ls.push('ha')
    ls.push('haha')
    for c in ls:
        print c
    print ls
