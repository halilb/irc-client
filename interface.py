import sys
from enum import Types
from PyQt4.QtCore import * # NOQA
from PyQt4.QtGui import * # NOQA
from time import gmtime, strftime


class ClientDialog(QDialog):
    def __init__(self, threadQueue, screenQueue):
        self.threadQueue = threadQueue
        self.screenQueue = screenQueue
        # create a Qt application --- every PyQt app needs one
        self.qt_app = QApplication(sys.argv)
        # Call the parent constructor on the current object
        QDialog.__init__(self, None)
        # Set up the window
        self.setWindowTitle('IRC Client')
        self.setMinimumSize(500, 200)
        self.resize(640, 480)
        # Add a vertical layout
        self.vbox = QVBoxLayout()
        self.vbox.setGeometry(QRect(10, 10, 621, 461))
        # Add a horizontal layout
        self.hbox = QHBoxLayout()
        # The sender textbox
        self.sender = QLineEdit("", self)
        # The channel region
        self.channel = QTextBrowser()
        self.channel.setMinimumSize(QSize(480, 0))
        # The send button
        self.send_button = QPushButton('&Send')
        # The users' section
        self.userList = QTextBrowser()
        # Connect the Go button to its callback
        self.send_button.clicked.connect(self.outgoing_parser)
        # Add the controls to the vertical layout
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.sender)
        self.vbox.addWidget(self.send_button)
        self.hbox.addWidget(self.channel)
        self.hbox.addWidget(self.userList)
        # start timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateChannelWindow)
        # update every 10 ms
        self.timer.start(10)
        # Use the vertical layout for the current window
        self.setLayout(self.vbox)

    def cprint(self, data):
        # code
        self.channel.append(data)

    def updateChannelWindow(self):
        if self.screenQueue.qsize() > 0:
            incoming_message = self.screenQueue.get()
            message = self.incoming_parser(incoming_message)
            if message:
                message = self.formatMessage(message, False)
                self.channel.append(message)

    def incoming_parser(self, mes):
        msgType = mes.type
        responseTypes = Types.responseTypes

        print msgType
        if msgType == responseTypes.PUBLIC_MESSAGE:
            return "<" + mes.nickname + ">:" + mes.text
        if msgType == responseTypes.PRIVATE_MESSAGE:
            return "*" + mes.nickname + "*:" + mes.text
        elif msgType == responseTypes.NEW_LOGIN:
            return "Registered as <" + mes.nickname + ">"
        elif msgType == responseTypes.REJECTED:
            return "Username rejected as <" + mes.nickname + ">"
        elif msgType == responseTypes.PRIVATE_MES_FAILED:
            return "Private message failed"
        elif msgType == responseTypes.SYSTEM:
            return mes.text
        elif msgType == responseTypes.ERROR:
            return "Server error"
        elif msgType == responseTypes.NOT_SIGNED_IN:
            return "You have to sign in first"
        elif msgType == responseTypes.PRIVATE_MES_FAILED:
            return "Target not found: <" + mes.nickname + ">"
        elif msgType == responseTypes.LIST:
            self.userList.clear()
            for item in mes.nickname.split(":"):
                self.userList.append(item)
            return

    def outgoing_parser(self):
        msg = str(self.sender.text())
        if len(msg) > 0:
            displayedMessage = self.formatMessage(msg, True)
            self.sender.clear()
            self.channel.append(displayedMessage)
            self.threadQueue.put(msg)

    def formatMessage(self, message, isLocal):
        result = strftime("%H:%M:%S", gmtime())
        result +=  " -Local-" if isLocal else " -Server-"
        return result + ": " + message

    def run(self):
        ''' Run the app and show the main form. '''
        self.show()
        self.qt_app.exec_()
