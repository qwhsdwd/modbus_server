import threading
# import thread
import time
class Test(object):
    def __init__(self):
    #threading.Thread.__init__(self)
        self._sName = "machao"

    def process(self):
        th1 = threading.Thread(target = Test.buildList , (self ,))
        th1.start()
        th1.join()

    def buildList(self):
        while True:
            print "start"
            time.sleep(3)

test = Test()
test.process()