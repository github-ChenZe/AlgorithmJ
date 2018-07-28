import random
import profile


def max_sub(array):
    max_sum = 0
    for i in range(0, len(array)):
        for j in range(i, len(array)):
            max_sum = max(max_sum, sum(array[i: j]))
    return max_sum


def max_sub_opt(array):
    max_sum = 0
    max_current = 0
    for i in array:
        max_current += i
        if max_current < 0:
            max_current = 0
        elif i > 0:
            max_sum = max(max_sum, max_current)
    return max_sum


if __name__ == '__main__':
    while True:
        length = raw_input('>>> ')
        arr = [random.randint(-1000, 1000) for i in range(0, int(length))]
        profile.fire()
        print max_sub_opt(arr)
        profile.check()
        profile.fire()
        print max_sub(arr)
        profile.check()
