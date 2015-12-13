class IncomingMessage:
    type = -1
    text = ""
    nickname = ""

    def __init__(self, origin):
        self.origin = origin
