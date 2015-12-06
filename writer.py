import threading
import socket

class WriterThread (threading.Thread):
    def __init__(self, name, csoc, threadQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.csoc = csoc
        self.threadQueue = threadQueue

    def run(self):
        # code
        if self.threadQueue.qsize() > 0:
            queue_message = self.threadQueue.get()
            # code
            try:
                self.csoc.send(queue_message)
            except socket.error:
                self.csoc.close()
                # break
