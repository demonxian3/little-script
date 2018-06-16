# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui,QtCore



class myQtClass(QtGui.QWidget):

    def __init__(self):
        super(myQtClass, self).__init__()
        self.initUI()

    def initUI(self):
        self.initWidget()
        self.initMenu()
        self.initLeftBar()
        self.initRightBar()
        self.initLayout()
        self.show()

    def initWidget(self):
        self.setGeometry(300,300,500,300)
        centerLocation = QtGui.QDesktopWidget().availableGeometry().center()
        targetFrame = self.frameGeometry()
        targetFrame.moveCenter(centerLocation)
        self.move(targetFrame.topLeft())

    def initMenu(self):
        # ac1 = QtGui.QAction("New",self)
        # ac2 = QtGui.QAction("Save",self)
        # ac3 = QtGui.QAction("Exit",self)
        # ac4 = QtGui.QAction("Open",self)
        #
        # ac1.setStatusTip('open file')
        # ac2.setStatusTip('open file')
        # ac3.setStatusTip('open file')
        # ac4.setStatusTip('open file')

        pass
        #menu = self.menuBar()
        #mf = menu.addMenu('File')
        #me = menu.addMenu('Edit')
        #mv = menu.addMenu('View')
        #mh = menu.addMenu('Help')

        #mf.addAction(ac1)
        #mf.addAction(ac2)
        #mf.addAction(ac3)
        #mf.addAction(ac4)

        #me.addAction(ac1)
        #me.addAction(ac2)
        #me.addAction(ac3)
        #me.addAction(ac4)

        #mv.addAction(ac1)
        #mv.addAction(ac2)
        #mv.addAction(ac3)
        #mv.addAction(ac4)

        # mh.addAction(ac1)
        # mh.addAction(ac2)
        # mh.addAction(ac3)
        # mh.addAction(ac4)

    def initLeftBar(self):
        btn1 = QtGui.QPushButton("Function1",self)
        btn2 = QtGui.QPushButton("Function2",self)
        btn3 = QtGui.QPushButton("Function3",self)
        btn4 = QtGui.QPushButton("Function4",self)

        self.v = QtGui.QVBoxLayout()
        self.v.addWidget(btn1)
        self.v.addWidget(btn2)
        self.v.addWidget(btn3)
        self.v.addWidget(btn4)
        self.v.addStretch(1)


    def initRightBar(self):
        txtEdit = QtGui.QTextEdit()
        rb = QtGui.QHBoxLayout()

        btn1 = QtGui.QPushButton("Cancael",self)
        btn2 = QtGui.QPushButton("OK",self)
        rb.addWidget(btn1)
        rb.addWidget(btn2)

        self.r = QtGui.QVBoxLayout()
        self.r.addWidget(txtEdit)
        self.r.addLayout(rb)


    def initLayout(self):
        main = QtGui.QHBoxLayout()
        main.addLayout(self.v)
        main.addLayout(self.r)
        self.setLayout(main)




def main():
    app = QtGui.QApplication(sys.argv)
    w = myQtClass()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

