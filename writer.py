import threading
import socket


class WriterThread (threading.Thread):
    def __init__(self, name, csoc, threadQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.csoc = csoc
        self.threadQueue = threadQueue

    def outgoing_parser(self, msg):
        if msg[0] == "/":
            words = msg.split(" ")
            cmd = words[0][1:]
            print "cmd: " + cmd
            if cmd == "tic":
                return "TIC"
            if cmd == "nick":
                return "USR " + words[1]
            if cmd == "list":
                return "LSQ"
            if cmd == "quit":
                return "QUI"
            if cmd == "msg":
                return "MSG %s:%s" % (words[1], " ".join(words[2:]))

        return "SAY " + msg

    def run(self):
        while True:
            if self.threadQueue.qsize() > 0:
                queue_message = self.threadQueue.get()
                outgoing = self.outgoing_parser(queue_message)
                outgoing += "\n"
                print("OUTGOING: " + outgoing)
                # code
                try:
                    self.csoc.send(outgoing)
                except socket.error:
                    self.csoc.close()
                    break
