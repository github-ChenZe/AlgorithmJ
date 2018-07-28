from Steper import Steper
import time
from lxml import etree
import XMLtoImage


class Algorithm(Steper):
    def __init__(self):
        super(Algorithm, self).__init__()
        self.callback = None
        self.converter = None

    def register(self, func):
        self.callback = func

    def generate_algorithm_diagram(self, **kwargs):
        return self.converter.convert(self.to_xml(**kwargs))

    def action(self):
        self.converter = XMLtoImage.XMLtoImage()

    def to_xml(self, **kwargs):
        return

    def pending(self, **kwargs):
        self.callback(self.generate_algorithm_diagram(**kwargs))
        super(Algorithm, self).pending()


def pr(st):
    print st


if __name__ == "__main__":
    st = Algorithm()
    st.register(pr)
    st.launch()
    while True:
        st.resume()
        time.sleep(3)
