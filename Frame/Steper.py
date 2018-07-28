import threading
import time


class Steper(object):
    def __init__(self):
        self.e = threading.Event()

    def pending(self):
        self.e.wait()
        self.e.clear()

    def action(self):
        while True:
            print "Action invoked."
            self.pending()

    def launch(self):
        t = threading.Thread(target=self.action)
        t.start()

    def resume(self):
        self.e.set()


if __name__ == "__main__":
    st = Steper()
    st.launch()
    while True:
        st.resume()
        time.sleep(3)
