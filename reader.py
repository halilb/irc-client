import threading


class ReaderThread (threading.Thread):
    def __init__(self, name, csoc, threadQueue, screenQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.csoc = csoc
        self.nickname = ""
        self.threadQueue = threadQueue
        self.screenQueue = screenQueue

    def incoming_parser(self, data):
        print("parser")

    def run(self):
        while True:
            data = self.csoc.recv(1024)
            print("data " + data)
