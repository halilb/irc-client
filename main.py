import socket
import Queue
from reader import ReaderThread
from writer import WriterThread
from interface import ClientDialog

# connect to the server
s = socket.socket()
host = "178.233.19.205"
port = 12345
s.connect((host, port))
sendQueue = Queue.Queue(maxsize=0)
screenQueue = Queue.Queue(maxsize=0)
app = ClientDialog(sendQueue, screenQueue)
# start threads
rt = ReaderThread("ReaderThread", s, sendQueue, screenQueue)
rt.start()

wt = WriterThread("WriterThread", s, sendQueue)
wt.start()
app.run()
rt.join()
wt.join()
s.close()
