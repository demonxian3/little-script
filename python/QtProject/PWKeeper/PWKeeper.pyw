#coding: utf-8
import sys
import os
import sqlite3
from PyQt4 import QtGui, QtCore

class PWKeeper(QtGui.QMainWindow):

    def __init__(self):
        super(PWKeeper, self).__init__()
        self.initToolbar()
        self.initDB()
        self.initGrid()
        self.setGeometry(300, 300, 650, 300)
        self.setWindowTitle(u'密码管理器v1 贤哥版')
        self.setWindowIcon(QtGui.QIcon('icon.png'))

    def initToolbar(self):
        newAction  = QtGui.QAction(QtGui.QIcon('new.png'),  'Add Item', self)
        delAction  = QtGui.QAction(QtGui.QIcon('del.png'),  'Del Item', self)
        editAction = QtGui.QAction(QtGui.QIcon('edit.png'), 'Edt Item', self)

        newAction.setShortcut('Ctrl+N')
        delAction.setShortcut('Ctrl+E')
        editAction.setShortcut('Delete')

        newAction.triggered.connect(self.newAction_def)
        delAction.triggered.connect(self.delAction_def)
        editAction.triggered.connect(self.editAction_def)

        self.tb_new  = self.addToolBar('New')
        self.tb_edit = self.addToolBar('Edit')
        self.tb_del  = self.addToolBar('Del')

        self.tb_new.addAction(newAction)
        self.tb_del.addAction(delAction)
        self.tb_edit.addAction(editAction)

    def initDB(self):
        if os.path.exists('pwd.db'):
            self.conn = sqlite3.connect('pwd.db')
            self.conn.isolation_level = None
        else:
            self.conn = sqlite3.connect('pwd.db')
            self.conn.isolation_level = None
            self.conn.execute('''CREATE TABLE pwd
                                (id int PRIMARY KEY NOT NULL,
                                site char(255),
                                name char(255),
                                pass char(255),
                                url char(255))''')

        cur = self.conn.cursor()
        cur.execute('Select * From pwd')
        self.UserData = cur.fetchall()
        cur.close()
        self.current_row = len(self.UserData)


    def initGrid(self):
        self.grid = QtGui.QTableWidget()
        self.grid.setColumnCount(4)
        #self.grid.setRowCount(3)
        self.setCentralWidget(self.grid)

        column_width = [75, 150, 270, 150]

        for i in range(4):
            self.grid.setColumnWidth(i, column_width[i])

        headerlabels = ['Website', 'Username', 'Password', 'URL']
        self.grid.setHorizontalHeaderLabels(headerlabels)
        self.grid.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.grid.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

    def showDialog(self, ws='', un='', pw='', url=''):

        ''' 创建对话框 '''
        edit_dialog = QtGui.QDialog(self)
        group = QtGui.QGroupBox('Edit Info', edit_dialog)       #创建组件盒子

        '''  创建Label  '''
        label_site = QtGui.QLabel('Website:',  group)
        label_name = QtGui.QLabel('Username:', group)
        label_pass = QtGui.QLabel('Password:', group)
        label_url  = QtGui.QLabel('URL:',      group)

        '''  创建输入框  '''
        line_site = QtGui.QLineEdit(group)
        line_name = QtGui.QLineEdit(group)
        line_pass = QtGui.QLineEdit(group)
        line_url  = QtGui.QLineEdit(group)

        line_site.setText(ws)
        line_name.setText(un)
        line_pass.setText(pw)
        line_url.setText(url)

        ''' 创建按钮 '''
        btn_OK = QtGui.QPushButton('OK', edit_dialog)
        btn_CC = QtGui.QPushButton('CANCEL', edit_dialog)
        btn_OK.clicked.connect(edit_dialog.accept)
        btn_CC.clicked.connect(edit_dialog.reject)
        btn_OK.setDefault(True)

        ''' 创建竖直组，将输入框部件加入其中 '''
        group_layout = QtGui.QVBoxLayout()
        group_item = [
            label_site, line_site,
            label_name, line_name,
            label_pass, line_pass,
            label_url , line_url
        ]
        for item in group_item:
            group_layout.addWidget(item)
        group.setLayout(group_layout)
        group.setFixedSize(group.sizeHint())

        ''' 创建水平组，将按钮控件加入其中 '''
        btn_layout = QtGui.QHBoxLayout()
        btn_layout.addWidget(btn_OK)
        btn_layout.addWidget(btn_CC)

        ''' 创建竖直组，将前面的竖直组，水平组包含其中 '''
        dialog_layout = QtGui.QVBoxLayout()
        dialog_layout.addWidget(group)
        dialog_layout.addLayout(btn_layout)

        ''' 设置对话框总格局 '''
        edit_dialog.setLayout(dialog_layout)
        edit_dialog.setFixedSize(edit_dialog.sizeHint())

        if edit_dialog.exec_():
            website  = line_site.text()
            username = line_name.text()
            password = line_pass.text()
            url = line_url.text()
            return True, website, username, password, url
        return False, None, None, None, None

    def newAction_def(self):
        data = self.showDialog()
        if data[0]:
            self.current_row += 1
            self.conn.execute("INSERT INTO pwd VALUES(%d, '%s', '%s', '%s', '%s')"
                              % (self.current_row, data[1], data[2], data[3], data[4]))
            self.grid.insertRow(self.current_row - 1)
            for i in range(4):
                new_item = QtGui.QTableWidgetItem(data[i + 1])
                self.grid.setItem(self.current_row - 1, i, new_item)

    def delAction_def(self):
        selected_row = self.grid.selectedItems()
        if selected_row:
            del_row = self.grid.row(selected_row[0])
            self.grid.removeRow(del_row)
            print del_row
            self.conn.execute("DELETE FROM pwd WHERE id = %d" % (del_row + 1))
            for index in range(del_row + 2, self.current_row + 1):
                self.conn.execute("UPDATE pwd SET id = %d WHERE id = %d" % ((index - 1), index))
            self.current_row -= 1
        else:
            self.showHint()

    def editAction_def(self):
        selected_row = self.grid.selectedItems()
        if selected_row:
            edit_row = self.grid.row(selected_row[0])
            old_data = []
            for i in range(4):
                old_data.append(self.grid.item(edit_row, i).text())
            new_data = self.showDialog(*old_data)
            if new_data[0]:
                self.conn.execute('''UPDATE pwd SET
                                     site = '%s', name = '%s',
                                     pass = '%s', url = '%s'
                                     WHERE id = '%d' '''
                                  % (new_data[1], new_data[2], new_data[3], new_data[4], edit_row + 1))
                for i in range(4):
                    new_item = QtGui.QTableWidgetItem(new_data[i + 1])
                    self.grid.setItem(edit_row, i, new_item)
        else:
            self.showHint()



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    pwk = PWKeeper()
    pwk.show()
    app.exec_()
    pwk.conn.close()
    sys.exit(0)