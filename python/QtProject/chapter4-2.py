# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui,QtCore

class myQtClass(QtGui.QWidget):

    def __init__(self):
        super(myQtClass, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 250, 150)
        self.show()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()

def main():
    app = QtGui.QApplication(sys.argv)
    w = myQtClass()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


