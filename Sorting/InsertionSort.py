from Frame.Algorithm import *


class InsertionSort(Algorithm):
    def __init__(self, arr):
        super(InsertionSort, self).__init__()
        self.array = arr

    def to_xml(self, **kwargs):
        # create XML
        root = etree.Element('table')
        # another child with text
        row = etree.Element('row')
        for e in self.array:
            cell = etree.Element('cell', color="RED")
            cell.text = '%s' % e
            row.append(cell)
        root.append(row)

        print etree.tostring(root, pretty_print=True)
        return etree.tostring(root, pretty_print=True)

    def action(self):
        super(InsertionSort, self).action()
        self.pending(description="Algorithm begins.")
        self.insertion_sort(self.array)
        self.pending(description="Algorithm done.")

    def generate_algorithm_diagram(self, **kwargs):
        return super(InsertionSort, self).generate_algorithm_diagram(**kwargs)

        colors = [BLACK] * len(self.array)
        result = []
        if "tested" in kwargs:
            colors[kwargs["tested"][0]] = "Yellow"
            colors[kwargs["tested"][1]] = "Yellow"
        if "swapped" in kwargs:
            colors[kwargs["swapped"][0]] = "Red"
            colors[kwargs["swapped"][1]] = "Red"
        if "pointer" in kwargs:
            pass
        if len(result) == 0:
            result.append(self.diagram.render())
        return result, kwargs["description"]

    def swap(self, arr, i, j):
        temp = arr[i]
        arr[i] = arr[j]
        arr[j] = temp
        self.pending(swapped=(i, j), description="Swapped %d (index %d) with %d (index %d)." % (arr[i], i, arr[j], j))

    def accommodate(self, arr, i):
        for j in xrange(i, 0, -1):
            if arr[j] < arr[j - 1]:
                #self.pending(tested=(j, j - 1),
                #             description="%d (index %d) is less than %d (index %d)." % (arr[j], j, arr[j-1], j-1))
                self.swap(arr, j - 1, j)

    def insertion_sort(self, arr):
        for i in range(0, len(arr)):
            #self.pending(pointer=i, description="Handling %d (index %d)." % (arr[i], i))
            self.accommodate(arr, i)


def pr(st):
    st.show()


if __name__ == '__main__':
    toImage = XMLtoImage.XMLtoImage()
    a = [4, 5, 1, 3, 2]
    inS = InsertionSort(a)
    inS.generate_algorithm_diagram(description="")#[0][0].show()
