#coding: utf-8

import sys
from PyQt4 import QtGui

class myQtClass(QtGui.QMainWindow):

    def __init__(self):
        super(myQtClass, self).__init__()
        self.initUI()

    def initUI(self):

        ''' Global Information '''
        self.textEdit = QtGui.QTextEdit("Welcome, My name is Demon!!!")
        self.textEdit.setFont(QtGui.QFont('Andalus',20))
        violet = QtGui.QColor(170,170,255)
        red    = QtGui.QColor(255,0,0)
        self.textEdit.setStyleSheet('QWidget{background-color: %s;color: %s}' %(violet.name(),red.name()))

        self.setCentralWidget(self.textEdit)
        self.setWindowIcon(QtGui.QIcon('notepad.png'))
        self.statusBar()

        ''' Action - File '''
        openFile = QtGui.QAction(QtGui.QIcon('open.png'),u'打开',self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.Fun_openFile)

        exitAction= QtGui.QAction(u'退出',self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        saveFile = QtGui.QAction(u'保存',self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('save file')
        saveFile.triggered.connect(self.Fun_saveFile)

        saveAsFile = QtGui.QAction(u'另存为',self)
        saveAsFile.setShortcut('Ctrl+Shift+S')
        saveAsFile.setStatusTip('save as ...')
        saveAsFile.triggered.connect(self.Fun_saveAsFile)

        ''' Action - Format'''
        fontChange = QtGui.QAction(u'字体',self)
        fontChange.setShortcut('Ctrl+L')
        fontChange.setStatusTip('Change font format')
        fontChange.triggered.connect(self.Fun_changeFont)

        backChange = QtGui.QAction(u'背景', self)
        backChange.setShortcut('Ctrl+B')
        backChange.setStatusTip('Change background color')
        backChange.triggered.connect(self.Fun_changeBack)

        colorChange = QtGui.QAction(u'颜色',self)
        colorChange.setShortcut('Ctrl+F')
        colorChange.setStatusTip('Change font color')
        colorChange.triggered.connect(self.Fun_changeColor)


        ''' Menu - File '''
        menubar = self.menuBar()
        fileMenu = menubar.addMenu(u'&文件(F)')
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)
        fileMenu.addAction(saveAsFile)
        fileMenu.addAction(exitAction)

        ''' Menu - Format '''
        formatMenu = menubar.addMenu(u'&格式(O)')
        formatMenu.addAction(fontChange)
        formatMenu.addAction(backChange)
        formatMenu.addAction(colorChange)

        ''' Menu - Format '''
        searchMenu = menubar.addMenu(u'&搜索(S)')

        ''' Global Information '''
        self.setGeometry(500, 300, 500, 300)
        self.setWindowTitle(u'贤哥版超简单记事本')
        self.setStatusTip('Editing...')
        self.show()

    def Fun_openFile(self):
        self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file','/home')
        fp = open(self.filename, 'r')
        with fp:
            data = fp.read()
            self.textEdit.setText(data)

    def Fun_saveFile(self):
        if 'filename' in dir(self):
            wp = open(self.filename, 'w')
            with wp:
                wp.write(self.textEdit.toPlainText())
        else:
            Fun_saveAsFile()

    def Fun_saveAsFile(self):
        self.filename = QtGui.QFileDialog.getSaveFileName(self, 'Save As file', '/home')
        wp = open(self.filename, 'w')
        with wp:
            wp.write(self.textEdit.toPlainText())

    def Fun_changeFont(self):
        font, ok = QtGui.QFontDialog.getFont()
        if ok:
            self.textEdit.setFont(font)

    def Fun_changeBack(self):
        back_col  = QtGui.QColorDialog.getColor()
        if back_col.isValid():
            self.textEdit.setStyleSheet('QWidget {background-color: %s}' % back_col.name())

    def Fun_changeColor(self):
        font_col = QtGui.QColorDialog.getColor()
        if font_col.isValid():
            self.textEdit.setStyleSheet('QWidget {color: %s}' %font_col.name())



def main():
    app = QtGui.QApplication(sys.argv)
    w = myQtClass()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()