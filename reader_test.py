import Queue
from reader import ReaderThread
from enum import Types


threadQueue = Queue.Queue(maxsize=0)
reader = ReaderThread("ReaderThread", None, threadQueue, None)


def receiveMessage(msg):
    return reader.incoming_parser(msg)

def testEmptyMessage():
    res = receiveMessage("")
    assert res == None

def testWelcomeMessage():
    res = receiveMessage("HEL halil")
    assert res.type == Types.responseTypes.NEW_LOGIN

def testRejectedMessage():
    res = receiveMessage("REJ")
    assert res.type == Types.responseTypes.REJECTED

def testPrivateFailedMessage():
    res = receiveMessage("MNO")
    assert res.type == Types.responseTypes.PRIVATE_MES_FAILED

def testTick():
    assert receiveMessage("TIC") == None
