#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from PyQt4 import QtGui, uic, QtCore
from SqlWorker import SqlWorker
from pickle import dumps, loads
from DataSecurity import Chifrator
from functions import center, ui_path
from Generator import MethGen
from functions import enthropy
from ErorWindow import ErorWindow


class AddData(QtGui.QDialog):
    def __init__(self, parent, base_path, pwd, uids):
        QtGui.QDialog.__init__(self, parent)
        global lang
        if lang == 'En_en':
            addr = 'res/ui/add_data/en.ui'
        elif lang == 'Ru_ru':
            addr = 'res/ui/add_data/ru.ui'
        uiClass, qtBaseClass = uic.loadUiType(addr)
        del qtBaseClass
        self.setModal(True)
        self.uids = uids
        self.ui = uiClass()
        self.ui.setupUi(self)
        self.b_p = base_path
        self.sql = SqlWorker()
        self.chi = Chifrator()
        self.pwd = pwd
        center(self)
        self.groups()
        self.ui.pwd.textChanged.connect(self.edtPwd)
        self.ui.generate.clicked.connect(self.generate)
        self.ui.view_pwd.setIcon(QtGui.QIcon('res/icons/pwd_no.png'))
        self.ui.view_pwd.setCheckable(True)
        self.ui.view_pwd.clicked.connect(self.view)
        self.ui.add.clicked.connect(self.add)
        self.ui.add_group.clicked.connect(self.addGroup)
        self.ui.prBar.setMinimum(0)
        self.ui.prBar.setMaximum(300)

    def generate(self):
        gen = MethGen()
        pwd = gen.strength_hard(gen.voider(6))
        del gen
        self.ui.pwd.setText(pwd)
        self.ui.repwd.setText(pwd)
        i = enthropy(pwd)
        self.ui.prBar.setValue(i)
        self.edtPwd()

    def edtPwd(self):
        val = self.ui.pwd.text()
        val = enthropy(val)
        val = int(val)
        self.ui.prBar.setValue(val)

    def groups(self):
        self.ui.cbb1.clear()
        global count
        self.uids = count
        for x in self.uids.keys():
            self.ui.cbb1.addItem(x)

    def view(self):
        if self.ui.view_pwd.isChecked():
            pwd = self.ui.pwd.text()
            repwd = self.ui.repwd.text()
            self.ui.view_pwd.setIcon(QtGui.QIcon('res/icons/pwd_yes.png'))
            self.ui.pwd.setEchoMode(QtGui.QLineEdit.Normal)
            self.ui.repwd.setEchoMode(QtGui.QLineEdit.Normal)
            self.ui.pwd.setText(pwd)
            self.ui.repwd.setText(repwd)
        elif not self.ui.view_pwd.isChecked():
            pwd = self.ui.pwd.text()
            repwd = self.ui.repwd.text()
            self.ui.view_pwd.setIcon(QtGui.QIcon('res/icons/pwd_no.png'))
            self.ui.pwd.setEchoMode(QtGui.QLineEdit.Password)
            self.ui.repwd.setEchoMode(QtGui.QLineEdit.Password)
            self.ui.pwd.setText(pwd)
            self.ui.repwd.setText(repwd)

    def add(self):
        inet = self.ui.inet_addr.text()
        login = self.ui.login.text()
        group = self.ui.cbb1.currentText()
        pwd = self.ui.pwd.text()
        repwd = self.ui.repwd.text()
        if pwd == repwd:
            login = dumps(self.chi.encrypt_text(self.pwd, login))  #
            uid = self.uids.get(group, 1)+1
            pwd = dumps(self.chi.encrypt_text(self.pwd, pwd))  #
            str_execute = 'INSERT INTO {}(uid, inet, login, pwd) VALUES('+str(uid)+', "{}",'
            str_execute = str_execute.format(group, inet)
            str_execute += '?, ?)'
            self.sql.executeSqlCmdToBlob(self.b_p, str_execute, (login, pwd))
            global count
            count[group] += 1
            self.close()
        else:
            erm = ErorWindow(self, self.tr('Eror'), 1)
            erm.exec_()
            return

    def addGroup(self):
        dialog = AddGroup(self, self.b_p)
        dialog.exec_()
        self.groups()


class UpdateData(QtGui.QDialog):
    def __init__(self, parent, base_path, pwd, data):

        """
        data = {uid:number;
                group:group}
        """
        QtGui.QDialog.__init__(self, parent)
        global lang
        if lang == 'En_en':
            addr = 'res/ui/add_data/en_up.ui'
        elif lang == 'Ru_ru':
            addr = 'res/ui/add_data/ru_up.ui'
        uiClass, qtBaseClass = uic.loadUiType(addr)
        del qtBaseClass
        self.setModal(True)
        self.data = data
        self.ui = uiClass()
        self.ui.setupUi(self)
        self.b_p = base_path
        self.sql = SqlWorker()
        self.chi = Chifrator()
        self.pwd = pwd
        center(self)
        tmp = self.sql.selectDataFromTable(self.b_p,
                                           ('*',
                                            '{}'.format(self.data['group']),
                                            'uid = {}'.format(self.data['uid'])))
        tmp = tmp[0]
        self.old_pwd = self.chi.decrypt_text(self.pwd, loads(tmp[2]))
        self.old_login = self.chi.decrypt_text(self.pwd, loads(tmp[1]))
        self.old_inet = tmp[3]
        self.ui.inet_addr.setText(self.old_inet)
        self.ui.login.setText(self.old_login)
        self.ui.pwd.setText(self.old_pwd)
        self.ui.repwd.setText(self.old_pwd)
        self.ui.pwd.textChanged.connect(self.edtPwd)
        self.ui.generate.clicked.connect(self.generate)
        self.ui.view_pwd.setIcon(QtGui.QIcon('res/icons/pwd_no.png'))
        self.ui.view_pwd.setCheckable(True)
        self.ui.view_pwd.clicked.connect(self.view)
        self.ui.add.clicked.connect(self.add)
        self.ui.prBar.setMaximum(300)
        self.ui.prBar.setMinimum(0)

    def generate(self):
        gen = MethGen()
        pwd = gen.strength_hard(gen.voider(6))
        del gen
        self.ui.pwd.setText(pwd)
        self.ui.repwd.setText(pwd)
        i = enthropy(pwd)
        self.ui.prBar.setValue(i)

    def edtPwd(self):
        val = self.ui.pwd.text()
        val = enthropy(val)
        val = int(val)
        self.ui.prBar.setValue(val)

    def view(self):
        if self.ui.view_pwd.isChecked():
            pwd = self.ui.pwd.text()
            repwd = self.ui.repwd.text()
            self.ui.view_pwd.setIcon(QtGui.QIcon('res/icons/pwd_yes.png'))
            self.ui.pwd.setEchoMode(QtGui.QLineEdit.Normal)
            self.ui.repwd.setEchoMode(QtGui.QLineEdit.Normal)
            self.ui.pwd.setText(pwd)
            self.ui.repwd.setText(repwd)
        elif not self.ui.view_pwd.isChecked():
            pwd = self.ui.pwd.text()
            repwd = self.ui.repwd.text()
            self.ui.view_pwd.setIcon(QtGui.QIcon('res/icons/pwd_no.png'))
            self.ui.pwd.setEchoMode(QtGui.QLineEdit.Password)
            self.ui.repwd.setEchoMode(QtGui.QLineEdit.Password)
            self.ui.pwd.setText(pwd)
            self.ui.repwd.setText(repwd)

    def add(self):
        inet = self.ui.inet_addr.text()
        login = self.ui.login.text()
        group = self.data['group']
        pwd = self.ui.pwd.text()
        repwd = self.ui.repwd.text()
        uid = self.data['uid']
        if pwd == repwd:
            if inet != self.old_inet:
                self.sql.updateDataInTable(self.b_p,
                                           ('{}'.format(group),
                                            'inet',
                                            '"{}"'.format(inet),
                                            'uid = {}'.format(uid)))
            if login != self.old_login:
                login = dumps(self.chi.encrypt_text(self.pwd, login))
                self.sql.executeSqlCmdToBlobOne(self.b_p,
                                                'UPDATE {}'.format(group) +
                                                ' SET login = ? ' +
                                                'WHERE uid = {}'.format(uid),
                                                login)
            if pwd != self.old_pwd:
                pwd = dumps(self.chi.encrypt_text(self.pwd, pwd))
                self.sql.executeSqlCmdToBlobOne(self.b_p,
                                                'UPDATE {}'.format(group) +
                                                ' SET pwd = ? ' +
                                                'WHERE uid = {}'.format(uid),
                                                pwd)
            self.close()
        else:
            erm = ErorWindow(self, self.tr('Eror'), 1)
            erm.exec_()
            return


class AddGroup(QtGui.QDialog):
    """docstring for AddGroup"""

    def __init__(self, parent, base_path):
        QtGui.QDialog.__init__(self, parent)
        uiClass, qtBaseClass = uic.loadUiType('res/ui/add_data/add_group.ui')
        del qtBaseClass
        self.setModal(True)
        self.b_p = base_path
        self.ui = uiClass()
        center(self)
        self.ui.setupUi(self)
        self.name = None
        self.sql = SqlWorker()
        self.ui.add.clicked.connect(self.ok)
        self.ui.no.clicked.connect(self.no)

    def ok(self):
        self.name = self.ui.name.text()
        if (self.name != '') and (self.name is not None) and (self.name != ('group' or 'data')) and (' ' not in self.name):
            self.sql.addDataToTable(self.b_p, ('gr',
                                               'grop',
                                               '"{}"'.format(self.name)))
            self.sql.createTableInBase(self.b_p,
                                       ('{}'.format(self.name),
                                        'uid INTEGER PRIMARY KEY AUTOINCREMENT,\
                                        login BLOB,\
                                        pwd BLOB ,\
                                        inet BLOB'))
            global count
            count[self.name] = 0
            self.close()
        else:
            QtGui.QMessageBox.question(self,
                                       'Eror',
                                       'Please enter correct name !!!',
                                       QtGui.QMessageBox.Yes)
            return

    def no(self):
        self.close()


class FindInBase(QtGui.QDialog):
    def __init__(self, parent, base_pwd, base_addr):
        QtGui.QDialog.__init__(self, parent)
        global lang
        if lang == 'En_en':
            addr = 'res/ui/find/en_find.ui'
        elif lang == 'Ru_ru':
            addr = 'res/ui/find/ru_find.ui'
        self.base_pwd = base_pwd
        self.base_addr = base_addr
        self.sql = SqlWorker()
        uiClass, qtBaseClass = uic.loadUiType(addr)
        del qtBaseClass
        self.ui = uiClass()
        center(self)
        self.ui.setupUi(self)
        self.setModal(True)
        self.chi = Chifrator()
        self.clipboard = QtGui.QApplication.clipboard()
        self.ui.find.clicked.connect(self.find_in_data)
        self.ui.pwd_v.stateChanged.connect(self.find_in_data)
        self.actionCopyLogin = QtGui.QAction('Copy login to clipboard', self)
        self.actionCopyPwd = QtGui.QAction('Copy password to clipboard', self)
        self.ui.data.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.ui.data.addAction(self.actionCopyLogin)
        self.ui.data.addAction(self.actionCopyPwd)
        self.actionCopyLogin.triggered.connect(self.copyLogin)
        self.actionCopyPwd.triggered.connect(self.copyPassword)

    def find_in_data(self):
        self.ui.data.clear()
        find_txt = self.ui.string.text()
        groups = self.sql.selectDataFromTable(self.base_addr, ('grop', 'gr'))
        groups = [groups[x][0] for x in range(len(groups))]
        finded = []
        for x in groups:
            data = self.sql.selectDataFromTable(self.base_addr,
                                                ('uid, login, pwd, inet', '{}'.format(x)))
            data = [list(x) for x in data]
            for y in data:
                i = data.index(y)
                data[i].append(x)
                inet = data[i][3]
                pwd = self.chi.decrypt_text(self.base_pwd, loads(data[i][2]))
                login = self.chi.decrypt_text(self.base_pwd, loads(data[i][1]))
                if (find_txt in inet) or (find_txt in pwd) or (find_txt in login):
                    finded.append(y)
        widgets = [QtGui.QTreeWidgetItem(self.ui.data) for x in range(len(finded))]
        for x in finded:
            i = finded.index(x)
            widgets[i].setText(5, str(finded[i][0]))
            widgets[i].setText(0, str(i))
            widgets[i].setText(1, finded[i][3])
            widgets[i].setText(2, finded[i][4])
            login = self.chi.decrypt_text(self.base_pwd, loads(finded[i][1]))
            widgets[i].setText(3, login)
            if self.ui.pwd_v.isChecked():
                pwd = self.chi.decrypt_text(self.base_pwd, loads(finded[i][2]))
                widgets[i].setText(4, pwd)
            else:
                widgets[i].setText(4, '************')

    def copyLogin(self):
        login = self.ui.data.currentItem().text(3)
        print(login)
        self.clipboard.clear()
        self.clipboard.setText(login)

    def copyPassword(self):
        if self.ui.pwd_v.isChecked():
            pwd = self.ui.data.currentItem().text(4)
        else:
            group = self.ui.data.currentItem().text(2)
            uid = self.ui.data.currentItem().text(5)
            pwd = self.sql.selectDataFromTable(self.base_addr,
                                               ('pwd',
                                                '{}'.format(group),
                                                'uid = {}'.format(uid)))
            pwd = pwd[0][0]
            pwd = self.chi.decrypt_text(self.base_pwd, loads(pwd))
        self.clipboard.clear()
        self.clipboard.setText(pwd)

    def closeEvent(self, event):
        self.clipboard.clear()
        event.accept()

lang = ui_path()
count = {'Internet': 0, 'Email': 0}