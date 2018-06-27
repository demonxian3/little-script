# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui,QtCore



class myQtClass(QtGui.QWidget):

    def __init__(self):
        super(myQtClass, self).__init__()
        self.initUI()

    def initUI(self):

        ''' 绝对定位 '''
        label1 = QtGui.QLabel('Demon', self)
        label2 = QtGui.QLabel('Demonxian', self)
        label3 = QtGui.QLabel('Demonxian3', self)
        label1.move(15,10)
        label2.move(35,40)
        label3.move(55,70)

        ''' 盒子布局 '''
        okButton = QtGui.QPushButton("OK")
        ccButton = QtGui.QPushButton("Cancel")
        hbox = QtGui.QHBoxLayout()      #水平盒子
        hbox.addStretch(1)              #伸展系数
        hbox.addWidget(okButton)        #存放部件
        hbox.addWidget(ccButton)

        vbox = QtGui.QVBoxLayout()      #竖直盒子
        vbox.addStretch(1)              #挤压系数
        vbox.addLayout(hbox)            #存放盒子
        self.setLayout(vbox)            #设置布局

        self.setGeometry(500,300,500,300)
        self.setWindowTitle('written by D3M0n')
        self.show()

def main():
    app = QtGui.QApplication(sys.argv)
    w = myQtClass()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


