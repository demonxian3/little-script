# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui,QtCore



class myQtClass(QtGui.QWidget):

    def __init__(self):
        super(myQtClass, self).__init__()
        self.initUI()

    def initUI(self):
        grid = QtGui.QGridLayout()
        self.setLayout(grid)

        names = ['Cls', 'Bck', '', 'Close',
                 '7','8','9','/',
                 '4','5','6','*',
                 '1','2','3','-',
                 '0','.','=','+']

        positions = [(i,j) for i in range(5) for j in range(4)]

        for position, name in zip(positions, names):
            if name == '':
                continue
            btn = QtGui.QPushButton(name)
            grid.addWidget(btn, *position)

        self.setGeometry(500,300,500,300)
        self.setWindowTitle('Calc written by D3M0n')
        self.show()

def main():
    app = QtGui.QApplication(sys.argv)
    w = myQtClass()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


