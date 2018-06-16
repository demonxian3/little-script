# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui,QtCore

class myQtClass(QtGui.QWidget):

    def __init__(self):
        super(myQtClass, self).__init__()
        self.initUI()

    def initUI(self):
        lcd = QtGui.QLCDNumber(self)
        sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(sld)

        self.setLayout(vbox)
        sld.valueChanged.connect(lcd.display)

        self.setGeometry(300,300,250,150)
        self.setWindowTitle('Signal & slot')
        self.show()

def main():
    app = QtGui.QApplication(sys.argv)
    w = myQtClass()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


