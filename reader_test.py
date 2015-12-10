from reader import ReaderThread
from enum import Types


reader = ReaderThread("ReaderThread", None, None, None)


def receiveMessage(msg):
    return reader.incoming_parser(msg)

def testEmptyMessage():
    res = receiveMessage("")
    assert res.type == Types.responseTypes.EMPTY

def testWelcomeMessage():
    res = receiveMessage("HEL halil")
    assert res.type == Types.responseTypes.NEW_LOGIN

def testRejectedMessage():
    res = receiveMessage("REJ")
    assert res.type == Types.responseTypes.REJECTED

def testPrivateFailedMessage():
    res = receiveMessage("MNO")
    assert res.type == Types.responseTypes.PRIVATE_MES_FAILED
