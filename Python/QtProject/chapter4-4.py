# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui,QtCore

class Communicate(QtCore.QObject):
    closeApp = QtCore.pyqtSignal()

class myQtClass(QtGui.QMainWindow):

    def __init__(self):
        super(myQtClass, self).__init__()
        self.initUI()

    def initUI(self):
        self.c = Communicate()
        self.c.closeApp.connect(self.close)
        self.show()

    def mousePressEvent(self, event):
        self.c.closeApp.emit()

def main():
    app = QtGui.QApplication(sys.argv)
    w = myQtClass()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


