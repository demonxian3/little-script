# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui,QtCore

class myQtClass(QtGui.QMainWindow):

    def __init__(self):
        super(myQtClass, self).__init__()
        self.initUI()

    def initUI(self):

        btn1 = QtGui.QPushButton('Btn1', self)
        btn2 = QtGui.QPushButton('Btn2', self)

        btn1.move(30, 50)
        btn2.move(150, 50)

        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)

        self.statusBar()

        self.setGeometry(500, 300, 500, 300)
        self.setWindowTitle('Event sender')
        self.show()

    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + 'was pressed')

def main():
    app = QtGui.QApplication(sys.argv)
    w = myQtClass()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


