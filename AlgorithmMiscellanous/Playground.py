def it():
    c = 1
    while c < 10:
        c += 1
        yield c

if __name__ == "__main__":
    i = it()
    p = []
    p.append(i)
    print p
    print p[-1]
