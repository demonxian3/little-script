#coding: utf-8
import sys
from PyQt4 import QtGui,QtCore

class MyWindowClass(QtGui.QWidget):
    def __init__(self):
        super(MyWindowClass, self).__init__()       #初始化父类对象
        self.initUI()

    def initUI(self):
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))    #提示文体

        self.setToolTip("This is my <b>first</b> Widget")   #提示框
        self.setGeometry(500,300,500,300)                   #定义初始大小，位置
        self.center()                                       #移动至中心位置
        self.setWindowTitle('writen by Demon')              #标题
        self.setWindowIcon(QtGui.QIcon('icon.png'))         #图标

        btn = QtGui.QPushButton('Hello', self)              #按钮
        btn.setToolTip("This is my <i>first</i> Button")    #提示
        btn.resize(btn.sizeHint())                          #大小
        btn.move(50,50)                                     #位置
        #btn.setText("My New Name")                         #名称

        qbtn = QtGui.QPushButton("Exit",self)
        qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)   #事件响应
        qbtn.resize(btn.sizeHint())
        qbtn.move(150,50)
        self.show()

    def center(self):
        qr = self.frameGeometry()       #获取矩形框架对象
        cp = QtGui.QDesktopWidget().availableGeometry().center()  #计算桌面分辨率中心点
        qr.moveCenter(cp)               #将矩形框架移动到屏幕正中央，大小不变
        self.move(qr.topLeft())     #将程序窗口移动到矩形框架左上点，此时正好是正中央位置

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self,    #标题，内容，按钮组，默认按钮
            'Message', "Are you sure to quit?",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No |QtGui.QMessageBox.Ignore | QtGui.QMessageBox.Save | QtGui.QMessageBox.Cancel,
            QtGui.QMessageBox.Yes)

        if reply == QtGui.QMessageBox.Yes:          #事件信号处理
            event.accept()
        else:
            event.ignore()


def main():
    app = QtGui.QApplication(sys.argv)
    w = MyWindowClass()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
