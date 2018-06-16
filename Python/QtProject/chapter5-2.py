#coding: utf-8

import sys
from PyQt4 import QtGui

class myQtClass(QtGui.QWidget):

    def __init__(self):
        super(myQtClass, self).__init__()
        self.initUI()

    def initUI(self):
        col = QtGui.QColor(0, 0, 0)
        self.btn = QtGui.QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.sDialog)

        self.frm = QtGui.QFrame(self)
        self.frm.setStyleSheet('QWidget{background-color: %s}' % col.name())
        self.frm.setGeometry(130, 22, 100, 100)
        self.setGeometry(300, 300, 250, 180)
        self.show()

    def sDialog(self):
        col  = QtGui.QColorDialog.getColor()
        if col.isValid():
            self.frm.setStyleSheet('QWidget {background-color: %s}' % col.name())

def main():
    app = QtGui.QApplication(sys.argv)
    w = myQtClass()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()