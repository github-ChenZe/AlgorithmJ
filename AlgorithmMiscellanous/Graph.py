from LinkedList import LinkedList


class Vertice(object):
    def __init__(self, index):
        self.index = index
        self.adjacent = LinkedList

    def connect(self, vertice):
        self.adjacent.push(vertice)
        vertice.adjacent.push(self)

    def degree(self):
        return self.adjacent.count

