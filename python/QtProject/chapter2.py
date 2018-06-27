#coding: utf-8

import sys
from PyQt4 import QtGui,QtCore

class myQtClass(QtGui.QMainWindow):

    def __init__(self):
        super(myQtClass, self).__init__()
        self.initUI()

    def initUI(self):
        '''    Action   '''
        MA_exit = QtGui.QAction(QtGui.QIcon('icon.png'), '&Exit', self)
        MA_exit.setShortcut('Ctrl+Q')
        MA_exit.setStatusTip('Exit application')
        MA_exit.triggered.connect(QtGui.qApp.quit)

        TA_exit = QtGui.QAction(QtGui.QIcon('exit.png'),'Left',self)
        TA_exit.setShortcut('Ctrl+E')
        TA_exit.setStatusTip('Tool for exit')
        TA_exit.triggered.connect(QtGui.qApp.quit)

        '''   StatusBar   '''
        self.statusBar().showMessage('Ready')

        '''   MenuBar   '''
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')     #注意有&符号可以配合Alt键快速定位
        fileMenu.addAction(MA_exit)
        fileMenu.addAction(TA_exit)
        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction(MA_exit)
        editMenu.addAction(TA_exit)

        '''   ToolBar   '''
        exitbar = self.addToolBar('Exit')
        exitbar.addAction(TA_exit)
        exitbar.addAction(MA_exit)
        toolbar = self.addToolBar('King')
        toolbar.addAction(TA_exit)
        toolbar.addAction(MA_exit)

        '''  Text Edit  '''
        textEdit = QtGui.QTextEdit()
        self.setCentralWidget(textEdit)

        '''  Window Widget  '''
        self.setGeometry(500,300,500,300)
        self.setWindowTitle('Statusbar')
        self.show()


def main():
    app = QtGui.QApplication(sys.argv)
    w = myQtClass()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()