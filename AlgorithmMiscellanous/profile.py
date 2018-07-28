import Stack
import time

start_time = Stack.Stack()


def fire():
    start_time.push(time.time())


def check():
    start = start_time.pop()
    end = time.time()
    print end - start
    return end - start


if __name__ == '__main__':
    fire()
    time.sleep(10)
    check()
