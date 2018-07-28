from Stack import Stack
from error import error
outputs = Stack()


def read_dict(file_name, f_key=lambda x: x, f_value=lambda x: x):
    result_dict = dict()
    file = open(file_name, 'r')
    for line in file:
        elements = line.split()
        if len(elements) != 2:
            error("Arg count error.")
        result_dict[f_key(elements[0])] = f_value(elements[1])
    return result_dict


def new(filename):
    file = open(filename, 'w')
    outputs.push(file)


def write(message):
    output_file = outputs.top()
    assert isinstance(output_file, file)
    output_file.write(message)
    output_file.flush()


def close():
    outputs.pop().close()
