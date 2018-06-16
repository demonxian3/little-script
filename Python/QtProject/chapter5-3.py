#coding: utf-8

import sys
from PyQt4 import QtGui

class myQtClass(QtGui.QWidget):

    def __init__(self):
        super(myQtClass, self).__init__()
        self.initUI()

    def initUI(self):
        vb = QtGui.QVBoxLayout()

        btn = QtGui.QPushButton('Dialog', self)
        btn.setSizePolicy(QtGui.QSizePolicy.Fixed,
                          QtGui.QSizePolicy.Fixed)
        btn.move(20, 20)
        btn.clicked.connect(self.sDialog)

        vb.addWidget(btn)

        self.lb1 = QtGui.QLabel('Knowledge only matters', self)
        self.lb1.move(130, 20)

        vb.addWidget(self.lb1)
        self.setLayout(vb)

        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Found dialog')
        self.show()

    def sDialog(self):
        font, ok = QtGui.QFontDialog.getFont()
        if ok:
            self.lb1.setFont(font)

def main():
    app = QtGui.QApplication(sys.argv)
    w = myQtClass()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()