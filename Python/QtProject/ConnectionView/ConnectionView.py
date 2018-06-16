#coding: utf-8
#version: 2.0
#author: demon
#date: 2018-04-10

import os
import sys
import urllib
import urllib2
import httplib
from threading import Thread
from PyQt4 import QtGui, QtCore

class ConnectionView(QtGui.QMainWindow):

    def __init__(self):
        super(ConnectionView, self).__init__()
        self.initToolBar()
        self.initTableGrid()
        self.initTimer()

        self.setGeometry(300, 300, 870, 400)
        self.center(self)
        self.setWindowTitle(u'连接查看器v2     -- written by dem0n')
        self.setWindowIcon(QtGui.QIcon('img/icon.ico'))
        self.statusBar().showMessage('QQ:920248921')


    def initToolBar(self):
        acAdd = QtGui.QAction(QtGui.QIcon('img/start.png'),  'Start Scan',  self)
        acCls = QtGui.QAction(QtGui.QIcon('img/clear.png'), 'Clear Scan', self)
        acInf = QtGui.QAction(QtGui.QIcon('img/info.png'), 'About author', self)
        acQck = QtGui.QAction(QtGui.QIcon('img/quick.ico'), 'Exit program', self)

        acAdd.setShortcut('Ctrl+B')
        acInf.setShortcut('Ctrl+I')
        acCls.setShortcut('Ctrl+L')
        acQck.setShortcut('Ctrl+Q')

        acAdd.triggered.connect(self.getConnection)
        acCls.triggered.connect(self.clsConnection)
        acInf.triggered.connect(self.aboutInfo_def)
        acQck.triggered.connect(QtGui.qApp.quit)

        acAdd.setToolTip("<b>Begin</b> scan")
        acCls.setToolTip("<b>Clear</b> scan")
        acInf.setToolTip("<b>Show</b> info about author")
        acQck.setToolTip("<b>Exit</b> program")

        tbAdd = self.addToolBar('Add')
        tbCls = self.addToolBar('Cls')
        tbInf = self.addToolBar('Inf')
        tbQck = self.addToolBar('Qck')

        self.pbar = QtGui.QProgressBar(self)

        tbAdd.addAction(acAdd)
        tbCls.addAction(acCls)
        tbInf.addAction(acInf)
        tbQck.addAction(acQck)

        ttt = self.addToolBar('Progress')
        ttt.addWidget(self.pbar)

    def initTableGrid(self):
        self.colLength = 7
        self.rowLength = 0
        self.grid = QtGui.QTableWidget()
        self.grid.setColumnCount(self.colLength)
        self.setCentralWidget(self.grid)
        #self.grid.setRowCount(6)

        columnWidth = [130, 130, 120, 55, 90, 370, 200]  #colLength
        for i in range(self.colLength):
            self.grid.setColumnWidth(i, columnWidth[i])

        columnName = [u'源socket', u'目的socket', u'进程名', u'进程号', u'连接状态', u'物理位置', u'服务名称']
        self.grid.setHorizontalHeaderLabels(columnName)

        #self.grid.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)    #禁止双击编辑
        self.grid.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)   #行选中
        #self.grid.setSelectionBehavior(QtGui.QAbstractItemView.SelectColumn) #列选中







    def center(self, target):
        centerLocation = QtGui.QDesktopWidget().availableGeometry().center()
        targetFrame = target.frameGeometry()
        targetFrame.moveCenter(centerLocation)
        target.move(targetFrame.topLeft())

    def initTimer(self):
        self.timer = QtCore.QBasicTimer()


    def getRealAddr(self, ip):
        try:
            url="http://ip.chinaz.com"
            user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
            headers = {'User-Agent': user_agent}
            params = {'ip' : ip}
            data = urllib.urlencode(params)
            req = urllib2.Request(url, data, headers)
            rep = urllib2.urlopen(req)
            res = rep.read().split("\n")
            first = 0
            for i in res:
                if "Whwtdhalf w50-0" in i and "IP" not in i:
                    address =  i.split(">")[1].split("<")[0].decode("utf-8")
                    return address
        except Exception, e:
            print e
            return u"暂查不到地址"

    def resultInTable(self, conn):
        try:
            res = conn.strip("\n")
            myNet = res.split("    ")
            try:
                myNet.remove("")
            except:
                pass

            src    = myNet[1].strip(" ")
            dst    = myNet[2].strip(" ")
            pid    = myNet[4].strip(" ")
            status = myNet[3].strip(" ")

            cmdTasklist = 'tasklist /svc /fi "pid eq '+pid+'" /fo csv | findstr "'+pid+'"'
            # print cmdTasklist
            p = os.popen(cmdTasklist)
            res = p.readline()
            process = res.split(",")[0].strip('"').strip('"')
            service = res.split(",")[2].strip('"').strip('\n').strip('"').decode("gb2312")

            ipaddr = dst.split(":")[0]
            realAddr = self.getRealAddr(ipaddr)
            connList = [src, dst, process, pid, status, realAddr ,service]
            print connList

            self.grid.insertRow(self.rowLength)
            for i in range(self.colLength):
                newItem = QtGui.QTableWidgetItem(connList[i])
                self.grid.setItem(self.rowLength, i, newItem)

            self.rowLength += 1
            self.step += 2
            self.pbar.setValue(self.step)

        except:
            pass


    def getConnection(self):
        self.clsConnection()
        self.pbar.setValue(0)
        self.step = 0
        noUDP     =   'find "TCP"'
        noLocal   =   'find /v "127.0.0.1"'
        noListen  =   'find /v "0.0.0.0"'
        noIPV6    =   'find /v "*:*" | find /v "[::]"'
        cmdNestat =   'netstat -ano|' +noUDP+ '|' +noLocal+ '|' +noIPV6+ '|' +noListen

        print cmdNestat
        p = os.popen(cmdNestat)
        connections = p.read().split("\n")

        for conn in connections:
            self.resultInTable(conn)
        self.pbar.setValue(100)


    def clsConnection(self):
        rowList = range(self.rowLength)
        rowList.reverse()
        for i in rowList:
            self.grid.removeRow(i)
        self.rowLength = 0

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


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    connView = ConnectionView()
    connView.show()
    app.exec_()
    sys.exit(0)
