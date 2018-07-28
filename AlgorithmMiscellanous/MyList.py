from error import error


class MyList(object):
    def __iter__(self):
        pass

    def next(self):
        pass

    def __str__(self):
        return '[%s]' % ', '.join(self)


def copy(old_array, new_array):
    if len(new_array) < len(old_array):
        error("New array is too small.")
    else:
        for i in range(0, len(old_array)):
            new_array[i] = old_array[i]
    return new_array
