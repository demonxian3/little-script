#coding: utf-8

import os
import sys
import sqlite3
from PyQt4 import QtGui, QtCore

class PwKeeper(QtGui.QMainWindow):

    def __init__(self):
        super(PwKeeper, self).__init__()
        self.initDB()
        self.initToolBar()
        self.initTableGrid()
        self.showPwdData()

        self.setGeometry(300, 300, 685, 300)
        self.center(self)
        self.setWindowTitle(u'密码管理器v3     -- written by dem0n')
        self.setWindowIcon(QtGui.QIcon('img/icon.png'))
        self.statusBar().showMessage('QQ:920248921')



    def initDB(self):
        if os.path.exists('pwd.db'):
            self.conn = sqlite3.connect('pwd.db')
        else :
            self.conn = sqlite3.connect('pwd.db')
            self.conn.execute(''' CREATE TABLE info (
             id     int ,
             site char(255),
             name char(255),
             pass char(255),
             url  char(255)); ''')
            self.conn.commit()

        cur = self.conn.cursor()
        cur.execute('select * from info')
        self.datas = cur.fetchall()
        self.rowLength = len(self.datas)
        cur.close()



    def initToolBar(self):
        acAdd = QtGui.QAction(QtGui.QIcon('img/new.png'),  'Add item',  self)
        acEdt = QtGui.QAction(QtGui.QIcon('img/edit.png'), 'Edit item', self)
        acDel = QtGui.QAction(QtGui.QIcon('img/del.png'),  'Del item',  self)
        acInf = QtGui.QAction(QtGui.QIcon('img/timg.jpg'), 'About author', self)
        acQck = QtGui.QAction(QtGui.QIcon('img/quick.jpg'), 'Exit program', self)

        acAdd.setShortcut('Ctrl+N')
        acEdt.setShortcut('Ctrl+E')
        acDel.setShortcut('Ctrl+D')
        acInf.setShortcut('Ctrl+I')
        acQck.setShortcut('Ctrl+Q')

        acAdd.triggered.connect(self.addItem_def)
        acEdt.triggered.connect(self.edtItem_def)
        acDel.triggered.connect(self.delItem_def)
        acInf.triggered.connect(self.aboutInfo_def)
        acQck.triggered.connect(QtGui.qApp.quit)
        #acQck.triggered.connect(QtCore.QCoreApplication.instance().quit)

        acAdd.setToolTip("<b>Add</b> a item")
        acEdt.setToolTip("<b>Edit</b> a item")
        acDel.setToolTip("<b>Delete</b> a item")
        acInf.setToolTip("<b>Show</b> info about author")
        acQck.setToolTip("<b>Exit</b> program")

        tbAdd = self.addToolBar('Add')
        tbEdt = self.addToolBar('Edit')
        tbDel = self.addToolBar('Del')
        tbInf = self.addToolBar('Inf')
        tbQck = self.addToolBar('Qck')

        tbAdd.addAction(acAdd)
        tbEdt.addAction(acEdt)
        tbDel.addAction(acDel)
        tbInf.addAction(acInf)
        tbQck.addAction(acQck)



    def initTableGrid(self):
        self.colLength = 4
        self.grid = QtGui.QTableWidget()
        self.grid.setColumnCount(self.colLength)
        self.setCentralWidget(self.grid)
        #self.grid.setRowCount(6)

        columnWidth = [200, 165, 160, 150]  #colLength
        for i in range(self.colLength):
            self.grid.setColumnWidth(i, columnWidth[i])

        columnName = ['Website', 'Username', 'Password', 'Remark']
        self.grid.setHorizontalHeaderLabels(columnName)

        self.grid.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)    #禁止双击编辑
        self.grid.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)   #行选中
        #self.grid.setSelectionBehavior(QtGui.QAbstractItemView.SelectColumn) #列选中



    def showPwdData(self):
        for row in range(self.rowLength):
            self.grid.insertRow(row)
            for col in range(self.colLength):
                #跳过ID字段 col+1
                newItem = QtGui.QTableWidgetItem(self.datas[row][col+1])
                self.grid.setItem(row, col, newItem)



    def showDiaglog(self, ws='', un='', pw='', url=''):
        edtDialog =  QtGui.QDialog(self)
        myGroupBox = QtGui.QGroupBox('Edit Info', edtDialog)

        lbSite = QtGui.QLabel('Website:',  myGroupBox)
        lbName = QtGui.QLabel('Username:', myGroupBox)
        lbPass = QtGui.QLabel('Password:', myGroupBox)
        lbURL  = QtGui.QLabel('Remark:',  myGroupBox)
        leSite = QtGui.QLineEdit(myGroupBox)
        leName = QtGui.QLineEdit(myGroupBox)
        lePass = QtGui.QLineEdit(myGroupBox)
        leURL  = QtGui.QLineEdit(myGroupBox)

        leName.setText(un)
        lePass.setText(pw)
        leSite.setText(ws)
        leURL.setText(url)

        btnOK = QtGui.QPushButton('OK', edtDialog)
        btnCC = QtGui.QPushButton('CANCEL', edtDialog)
        btnCC.clicked.connect(edtDialog.reject)
        btnOK.clicked.connect(edtDialog.accept)
        btnOK.setDefault(True)

        lbList = [lbName, lbPass, lbSite, lbURL]
        leList = [leName, lePass, leSite, leURL]

        leftLayout = QtGui.QVBoxLayout()
        rightLayout =  QtGui.QVBoxLayout()
        bodyLayout = QtGui.QHBoxLayout()

        for i in lbList:
            leftLayout.addWidget(i)

        for i in leList:
            rightLayout.addWidget(i)

        bodyLayout.addLayout(leftLayout)
        bodyLayout.addLayout(rightLayout)

        myGroupBox.setLayout(bodyLayout)
        #myGroupBox.setFixedSize(myGroupBox.sizeHint())

        btnLayout = QtGui.QHBoxLayout()
        btnLayout.addWidget(btnOK)
        btnLayout.addWidget(btnCC)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(myGroupBox)
        mainLayout.addLayout(btnLayout)

        edtDialog.setLayout(mainLayout)
        #edtDialog.setFixedSize(edtDialog.sizeHint())
        #edtDialog.setGeometry(300,300,300,175)
        edtDialog.resize(500,200)
        self.center(edtDialog)

        if edtDialog.exec_():
            wb = leSite.text()
            un = leName.text()
            pw = lePass.text()
            url = leURL.text()
            return True, wb, un, pw, url
        return False, None, None, None, None


    def center(self, target):
        centerLocation = QtGui.QDesktopWidget().availableGeometry().center()
        targetFrame = target.frameGeometry()
        targetFrame.moveCenter(centerLocation)
        target.move(targetFrame.topLeft())



    def addItem_def(self):
        self.statusBar().showMessage('Add New Item')

        inp = self.showDiaglog('','','','')
        if inp[0]:
            self.conn.execute('insert into info values(%d, "%s", "%s", "%s", "%s")'
                              % (self.rowLength+1, inp[1], inp[2], inp[3], inp[4]))
            print 'insert into info values(%d, "%s", "%s", "%s", "%s' % (self.rowLength+1, inp[1], inp[2], inp[3], inp[4])
            self.conn.commit()
            #show new line
            self.grid.insertRow(self.rowLength)
            for i in range(self.colLength):
                newItem = QtGui.QTableWidgetItem(inp[i+1])
                self.grid.setItem(self.rowLength, i, newItem)
            self.rowLength += 1



    def edtItem_def(self):
        selectedItem = self.grid.selectedItems()
        selectedRow = self.grid.row(selectedItem[0])
        if selectedItem:
            print selectedRow
            oldData = []
            for i in range(self.colLength):
                oldData.append(selectedItem[i].text())
            newData = self.showDiaglog(*oldData)
            newData = list(newData)
            if newData[0]:
                print newData[1:]+oldData
                self.conn.execute('update info set '
                                  'site = "%s",'
                                  'name = "%s",'
                                  'pass = "%s",'
                                  'url  = "%s" where '
                                  'site = "%s" and '
                                  'name = "%s" and '
                                  'pass = "%s" and '
                                  'url  = "%s"' %
                tuple(newData[1:]+oldData))
                self.conn.commit()

            for i in range(self.colLength):
                newItem = QtGui.QTableWidgetItem(newData[i+1])
                self.grid.setItem(selectedRow, i, newItem)
        else:
            print "No selected"







    def delItem_def(self):
        self.statusBar().showMessage('Delete Item')

        selectedRow = self.grid.selectedItems()
        if selectedRow:
            #face delete:
            id = self.grid.row(selectedRow[0])
            wb = selectedRow[0].text()
            un = selectedRow[1].text()
            pw = selectedRow[2].text()
            url = selectedRow[3].text()
            self.grid.removeRow(id)
            self.rowLength -= 1

            #database delete:
            deleteSQL =  'delete from info where '
            deleteSQL += 'site = "%s" and ' % wb
            deleteSQL += 'name = "%s" and ' % un
            deleteSQL += 'pass = "%s" and ' % pw
            deleteSQL += 'url  = "%s"; ' % url
            print deleteSQL
            self.conn.execute(deleteSQL);
            self.conn.commit()
        else:
            print "No selected"


    def aboutInfo_def(self):
        edtDialog =  QtGui.QDialog(self)
        edtDialog.setWindowTitle(u"关于作者")
        edtDialog.setGeometry(500,300,300,200)
        self.center(edtDialog)
        myGroupBox = QtGui.QGroupBox('Edit Info', edtDialog)

        lbAuthor = QtGui.QLabel('Author: Dem0n',  myGroupBox)
        lbQQ     = QtGui.QLabel('QQ:     920248921',  myGroupBox)
        lbDate   = QtGui.QLabel('Date:   2018-04-07', myGroupBox)
        lbBlog   = QtGui.QLabel('Blog:   http://cnblogs.com/demonxian3', myGroupBox)
        lbGithub = QtGui.QLabel('GitHub: http://github.com/demonxian3',  myGroupBox)

        labelLayout = QtGui.QVBoxLayout()
        mainLayout  = QtGui.QVBoxLayout()
        btnLayout   = QtGui.QVBoxLayout()

        labelLayout.addWidget(lbAuthor)
        labelLayout.addWidget(lbQQ)
        labelLayout.addWidget(lbDate)
        labelLayout.addWidget(lbBlog)
        labelLayout.addWidget(lbGithub)

        btnOK = QtGui.QPushButton('OK', edtDialog)
        btnOK.clicked.connect(edtDialog.accept)
        btnOK.setDefault(True)
        btnLayout.addWidget(btnOK)

        myGroupBox.setLayout(labelLayout)
        mainLayout.addWidget(myGroupBox)
        mainLayout.addLayout(btnLayout)

        edtDialog.setLayout(mainLayout)
        edtDialog.exec_()


    def closeEvent(self, event):
        answerYes = QtGui.QMessageBox.Yes
        answerNo = QtGui.QMessageBox.No
        boxTitle = u"想退出吗"
        boxContent = u"真的要退出？"
        answer = questionBox = QtGui.QMessageBox.question(self, boxTitle, boxContent, answerYes|answerNo)
        if answer == answerYes:
            event.accept()
        else:
            event.ignore()




if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    pwk = PwKeeper()
    pwk.show()
    app.exec_()
    pwk.conn.close()
    sys.exit(0)
