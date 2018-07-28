from error import error
import random


class FlexArray(object):
    def __init__(self, capacity, copy_from=None, prototype=None):
        self.count = 0
        self.current_iter_index = 0
        self.capacity = capacity
        self.sealed = False
        self.array = [None] * capacity
        if copy_from is None:
            return
        if capacity < len(copy_from):
            error("New array is too small.")
        for i in range(0, len(copy_from)):
            self[i] = copy_from[i]

    def insert_into_empty(self, value, position):
        if self[position] is not None:
            error("Position not empty.")
        self[position] = value

    def insert(self, value, position):
        if self.count == self.capacity:
            error("FlexArray full.")
        if self.sealed:
            error("FlexArray sealed.")
        for i in xrange(self.count, position, -1):
            self[i] = self[i - 1]
        self[position] = value

    def tri_split_array(self):
        length = self.count
        if (length & 1) == 0:
            error("Tri-splitting an even-count array.")
        return type(self)(self.capacity, self.array[0: (length >> 1)], self), self.array[length >> 1], \
            type(self)(self.capacity, self.array[(length >> 1) + 1:], self)

    def bi_split_array(self):
        length = self.count
        if (length & 1) == 1:
            error("Bi-splitting an odd-count array.")
        return type(self)(self.capacity, self.array[0: (length >> 1)], self), \
            type(self)(self.capacity, self.array[(length >> 1):], self)

    def alter(self, func):
        for i in range(0, self.count):
            new_value = func(self.array[i], i)
            if new_value is not None:
                self[i] = new_value

    def foreach(self, func):
        for i in range(0, self.count):
            func(self[i], i)

    def seal(self):
        self.sealed = True

    def pop_end(self):
        value = self[self.count - 1]
        self[self.count - 1] = None
        return value

    def pop_first(self):
        return self.pop_at(0)

    def push_end(self, value):
        self.insert_ok()
        self[self.count] = value

    def push_first(self, value):
        self.insert(value, 0)

    def concat_end(self, right_array):
        self.insert_ok()
        if self.count + right_array.count > self.capacity:
            error("Array full while concat_end. Self count: %d, right count: %d." % (self.count, right_array.count))
        for i in range(0, right_array.count):
            self.push_end(right_array[i])

    def pop_at(self, index):
        value = self[index]
        for i in range(index, self.count - 1):
            self[i] = self[i + 1]
        self[self.count - 1] = None
        return value

    def insert_ok(self):
        if self.sealed:
            error("Pushing into sealed array.")
        if self.count == self.capacity:
            error("Pushing into fulled array.")

    def __getitem__(self, item):
        return self.array[item]

    def __setitem__(self, key, value):
        if self.array[key] is None and value is not None:
            self.count += 1
        if self.array[key] is not None and value is None:
            self.count -= 1
        self.array[key] = value

    def __str__(self):
        return self.array.__str__()

    def __len__(self):
        return self.count

    def __iter__(self):
        self.current_iter_index = 0
        return self

    def next(self):
        if self.current_iter_index < self.count:
            val = self[self.current_iter_index]
            self.current_iter_index += 1
            return val

        else:
            raise StopIteration


class SortedArray(FlexArray):
    def __init__(self, capacity, copy_from=None, prototype=None):
        super(SortedArray, self).__init__(capacity, copy_from)

    def auto_insert(self, value):
        length = self.count
        target_position = -1
        for i in range(0, length):
            if self.array[i] == value:
                error("Key existed while inplace.")
            if self.array[i] > value:
                target_position = i
                break
        if target_position == -1:
            target_position = length
        self.insert(value, target_position)
        return target_position

    def look_for_first_greater_than(self, value):
        for i in range(0, self.count):
            if self[i] >= value:
                return i
        return self.count

    def __str__(self):
        return self.array.__str__()


if __name__ == '__main__':
    sa = SortedArray(16)
    a = [__i__ for __i__ in range(0, 15)]
    random.shuffle(a)
    print a
    for i in a:
        sa.auto_insert(i)
    print sa
    sa1, _, sa2 = sa.tri_split_array()
    assert isinstance(sa1, SortedArray)
    print sa1
    sa1.foreach(lambda x, y: x+y)
    print sa1
    sa1.alter(lambda x, y: x + y)
    print sa1
    print sa1.look_for_first_greater_than(25)
    print sa1.pop_end()
    print sa1
    print sa1.count
    print sa1.pop_first()
    print sa1
    print sa1.count
    print sa1.pop_at(1)
    print sa1
    print sa1.count
    sa1.concat_end(sa2)
    print sa1
    print sa1.count


