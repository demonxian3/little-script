#coding: utf-8

import sys
from PyQt4 import QtGui

class myQtClass(QtGui.QWidget):

    def __init__(self):
        super(myQtClass, self).__init__()
        self.initUI()

    def initUI(self):

        self.btn = QtGui.QPushButton('Dialog', self)
        self.btn.move(20,20)
        self.btn.clicked.connect(self.showDiaglog)

        self.le = QtGui.QLineEdit(self)
        self.le.move(130, 22)

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input diaglog')
        self.show()

    def showDiaglog(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')

        if ok:
            self.le.setText(str(text))

def main():
    app = QtGui.QApplication(sys.argv)
    w = myQtClass()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()