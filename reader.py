import threading
from enum import Types
from incoming_message import IncomingMessage


class ReaderThread (threading.Thread):
    def __init__(self, name, csoc, threadQueue, screenQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.csoc = csoc
        self.nickname = ""
        self.threadQueue = threadQueue
        self.screenQueue = screenQueue

    def incoming_parser(self, data):
        incoming_message = IncomingMessage(Types.originTypes.SERVER)

        if len(data) == 0:
            return

        print("INCOMING: " + data)

        cmd = data[0:3]
        rest = data[4:]

        if cmd == "TIC":
            self.threadQueue.put("/tic")
            return
        if cmd == "TOC":
            return

        if cmd == "SAY":
            tempArr = rest.split(":")
            incoming_message.type = Types.responseTypes.PUBLIC_MESSAGE
            incoming_message.nickname = tempArr[0]
            incoming_message.text = tempArr[1]
        if cmd == "MSG":
            tempArr = rest.split(":")
            incoming_message.type = Types.responseTypes.PRIVATE_MESSAGE
            incoming_message.nickname = tempArr[0]
            incoming_message.text = tempArr[1]
        elif cmd == "HEL":
            incoming_message.type = Types.responseTypes.NEW_LOGIN
            incoming_message.nickname = rest
        elif cmd == "SYS":
            incoming_message.type = Types.responseTypes.SYSTEM
            incoming_message.text = rest
        elif cmd == "REJ":
            incoming_message.type = Types.responseTypes.REJECTED
            incoming_message.nickname = rest
        elif cmd == "MNO":
            incoming_message.type = Types.responseTypes.PRIVATE_MES_FAILED
        elif cmd == "LSA":
            incoming_message.type = Types.responseTypes.LIST
            incoming_message.nickname = rest

        return incoming_message

    def run(self):
        while True:
            data = self.csoc.recv(1024)
            msg = self.incoming_parser(data)
            if msg:
                self.screenQueue.put(msg)
