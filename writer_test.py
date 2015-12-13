import Queue
from writer import WriterThread


screenQueue = Queue.Queue(maxsize=0)
writer = WriterThread("WriterThread", None, None, screenQueue)

def sendMessage(msg):
    return writer.outgoing_parser(msg)

def testBroadcastMessage():
    assert sendMessage("hello guys") == "SAY hello guys"

def testNickChange():
    assert sendMessage("/nick halil") == "USR halil"

def testUserList():
    assert sendMessage("/list") == "LSQ"

def testQuit():
    assert sendMessage("/quit") == "QUI"

def testPrivateMessage():
    assert sendMessage("/msg halil selam halil") == "MSG halil:selam halil"

def testTick():
    assert sendMessage("/tic") == "TIC"
