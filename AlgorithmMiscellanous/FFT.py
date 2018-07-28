import cmath
import random
import profile


class ListWrapper(object):
    def __init__(self, array):
        self.array = array
        self.mapping = lambda x: x

    def set_mapping(self, mapping):
        self.mapping = mapping

    def __getitem__(self, item):
        return self.array[self.mapping(item)]

    def __setitem__(self, key, value):
        self.array[self.mapping(key)] = value

    def __str__(self):
        result = ''
        for i in range(0, len(self.array)):
            result += '%s ' % self[i]
        return result


def eix(x):
    return cmath.exp(complex(0, x))


def bize(n):
    exp = 0
    while n > (1 << exp):
        exp += 1
    return 1 << exp


def bit_reverse(n, bound):
    left = bound >> 1
    right = 1
    while left > right:
        if ((n & left) > 0) != ((n & right) > 0):
            n ^= left
            n ^= right
        left >>= 1
        right <<= 1
    return n


def fft(array):
    # n = bize(len(array))
    n = len(array)
    if n == 1:
        return array
    new_array = array # [None] * n
    # MyList.copy(array, new_array)

    root = eix(2 * cmath.pi / n)
    current = 1
    evens = fft(new_array[::2])
    odds = fft(new_array[1::2])

    for i in range(0, n >> 1):
        item_e = evens[i]
        item_o = current * odds[i]
        new_array[i] = item_e + item_o
        new_array[i + (n >> 1)] = item_e - item_o
        current *= root
    return new_array


def inv_fft(array):
    # n = bize(len(array))
    n = len(array)
    if n == 1:
        return array
    new_array = array # [None] * n
    # MyList.copy(array, new_array)

    root = eix(-2 * cmath.pi / n)
    current = 1
    evens = inv_fft(new_array[::2])
    odds = inv_fft(new_array[1::2])

    for i in range(0, n >> 1):
        item_e = evens[i]
        item_o = current * odds[i]
        new_array[i] = item_e + item_o
        new_array[i + (n >> 1)] = item_e - item_o
        current *= root
    return new_array


def iter_fft(array):
    n = len(array)
    array_w = ListWrapper(array)
    array_w.set_mapping(lambda x: bit_reverse(x, n))

    storey = 1
    while n >> storey != 0:
        power = 1 << storey
        root = eix(2 * cmath.pi / power)
        for i in xrange(0, n, power):
            omega = 1
            half_power = power >> 1
            for j in range(0, half_power):
                index_base = i + j
                t = omega * array_w[index_base + half_power]
                u = array_w[index_base]
                array_w[index_base] = u + t
                array_w[index_base + half_power] = u - t
                omega *= root
        storey += 1
    return array_w


# NOT IMPLEMENTED
def iter_discrete_fft(array):
    n = len(array)
    assert n == 8
    # mod is 17
    array_w = ListWrapper(array)
    array_w.set_mapping(lambda x: bit_reverse(x, n))

    root = 1
    primitive_root = 2

    storey = 1
    while n >> storey != 0:
        power = 1 << storey
        root = eix(2 * cmath.pi / power)
        for i in xrange(0, n, power):
            omega = 1
            half_power = power >> 1
            for j in range(0, half_power):
                index_base = i + j
                t = omega * array_w[index_base + half_power]
                u = array_w[index_base]
                array_w[index_base] = u + t
                array_w[index_base + half_power] = u - t
                omega *= root
        storey += 1
    return array_w


roots = {8: 2, 4: 4, 2: 16, 1: 256}


def discrete_fft(array):
    orig = "%s" % array
    n = len(array)
    if n == 1:
        return array
    new_array = array

    root = roots[n]
    current = 1
    evens = discrete_fft(new_array[::2])
    odds = discrete_fft(new_array[1::2])

    for i in range(0, n):
        item_e = evens[i % (n >> 1)]
        item_o = current * odds[i % (n >> 1)]
        new_array[i] = item_e + item_o
        current *= root
    print "%s fft to be %s, root %d." % (orig, new_array, root)
    return new_array


def test():
    for i in range(12, 25):
        length = 2 << i
        arr = [complex(random.random(), 0) for __i__ in range(0, length)]
        profile.fire()
        iter_fft(arr)
        time = profile.check()


if __name__ == '__main__':
    a1 = discrete_fft([4, 1, 2, 3, 0, 0, 0, 0])
    print a1
    exit(0)
    a2 = fft([7, 6, 5, 4, 0, 0, 0, 0])
    a = [a1[i] * a2[i] for i in range(0, 8)]
    print a
    ia = inv_fft(a)
    ia = [ia[i] / 8 for i in range(0, 8)]
    print ia
