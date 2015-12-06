import sys
import signal
import socket
import Queue
from reader import ReaderThread
from writer import WriterThread
from interface import ClientDialog


if len(sys.argv) < 3:
    print "You have to specify hostname and port"
    sys.exit(2)
else:
    host = sys.argv[1]
    port = int(sys.argv[2])

print "Connecting to %s:%s" % (host, port)

signal.signal(signal.SIGINT, signal.SIG_DFL)

# connect to the server
s = socket.socket()
s.connect((host, port))
sendQueue = Queue.Queue(maxsize=0)
screenQueue = Queue.Queue(maxsize=0)
app = ClientDialog(sendQueue, screenQueue)
# start threads
reader = ReaderThread("ReaderThread", s, sendQueue, screenQueue)
reader.start()

writer = WriterThread("WriterThread", s, sendQueue)
writer.start()
app.run()
reader.join()
writer.join()
s.close()
