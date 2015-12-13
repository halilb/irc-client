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
    assert res.nickname == "halil"

def testRejectedMessage():
    res = receiveMessage("REJ halil")
    assert res.type == Types.responseTypes.REJECTED
    assert res.nickname == "halil"

def testPrivateFailedMessage():
    res = receiveMessage("MNO")
    assert res.type == Types.responseTypes.PRIVATE_MES_FAILED

def testTick():
    assert receiveMessage("TIC") == None

def testPublicMessage():
    res = receiveMessage("SAY halil:selam herkese")
    assert res.type == Types.responseTypes.PUBLIC_MESSAGE
    assert res.nickname == "halil"

def testPrivateMessage():
    res = receiveMessage("MSG adam:selam halil")
    assert res.type == Types.responseTypes.PRIVATE_MESSAGE
    assert res.nickname == "adam"
