#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from PyQt4 import QtGui, uic, QtCore
from pickle import loads
from SqlWorker import SqlWorker
import random
from functions import center, path_installer, ui_path
from DataHasher import Hasher
from ErorWindow import ErorWindow
from DataSecurity import Chifrator, CryptBase
import os
import tempfile


class BaseCreate(QtGui.QDialog):
    """This a BaseCreate window of Password Manager"""

    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        global lang
        if lang == 'En_en':
            addr = 'res/ui/dbs_crt/en_dbs_crt.ui'
        elif lang == 'Ru_ru':
            addr = 'res/ui/dbs_crt/ru_dbs_crt.ui'
        uiClass, qtBaseClass = uic.loadUiType(addr)
        del qtBaseClass
        self.ui = uiClass()
        self.ui.setupUi(self)
        self.setModal(True)
        center(self)
        self.opf = None
        self.sql = SqlWorker()
        self.k_file = None
        self.addr = None
        self.k_hash = None
        self.pwd = None
        self.hsc = Hasher()
        self.setModal(True)
        self.connect(self.ui.crt_base, QtCore.SIGNAL('clicked()'), self.opn_dbs)
        self.connect(self.ui.cls_btn, QtCore.SIGNAL('clicked()'), self.no)
        self.hash = ''
        self.connect(self.ui.ch_k_f, QtCore.SIGNAL('clicked()'), self.k_f)
        self.ui.view_pwd.setCheckable(True)
        self.connect(self.ui.view_pwd, QtCore.SIGNAL('clicked()'), self.view)
        self.connect(self.ui.ok_btn, QtCore.SIGNAL('clicked()'), self.ok)
        self.ui.view_pwd.setIcon(QtGui.QIcon('res/icons/pwd_no.png'))

    def opn_dbs(self):
        self.opf = QtGui.QFileDialog.getSaveFileName(self,
                                                     'Create database',
                                                     path_installer(),
                                                     'Password manager db (*.pwmdb)')
        if not '.pwmdb' in self.opf:
            self.opf += '.pwmdb'
        self.ui.addr.setText(self.opf)

    def no(self):
        self.opf = None
        self.k_file = None
        self.close()

    def k_f(self):
        self.k_file = QtGui.QFileDialog.getOpenFileName()
        self.ui.key_file.setText(self.k_file)

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

    def ok(self):
        pwd = self.ui.pwd.text()
        rep = self.ui.repwd.text()
        k_file = self.ui.key_file.text()
        opf = self.ui.addr.text()
        if pwd == rep:
            self.pwd = pwd
            if (k_file != '') and \
                    (k_file is not None) and \
                    (os.path.exists(k_file)):
                self.k_file = k_file
                self.k_hash = self.hsc.hasMd5(self.k_file)
            else:
                self.k_file = None
            if opf != '' and opf is not None:
                self.opf = opf
            else:
                ers = ErorWindow(self, 'Eror', 2)
                ers.exec_()

            self.close()
        else:
            ers = ErorWindow(self, 'Eror', 1)
            ers.exec_()
            return


class BaseOpen(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        global lang
        if lang == 'En_en':
            addr = 'res/ui/open_base/en_dbs_opn.ui'
        elif lang == 'Ru_ru':
            addr = 'res/ui/open_base/ru_dbs_opn.ui'
        uiClass, qtBaseClass = uic.loadUiType(addr)
        del qtBaseClass
        self.ui = uiClass()
        self.ui.setupUi(self)
        center(self)
        self.setModal(True)
        self.ui.view_pwd.setIcon(QtGui.QIcon('res/icons/pwd_no.png'))
        self.opf = None
        self.k_file = None
        self.dostup = False
        self.pwd = None
        self.sql = SqlWorker()
        self.chifrator = Chifrator()
        self.base_crypt = CryptBase()
        self.hsc = Hasher()
        self.setModal(True)
        self.connect(self.ui.ch_base, QtCore.SIGNAL('clicked()'), self.opn_dbs)
        self.connect(self.ui.cls_btn, QtCore.SIGNAL('clicked()'), self.no)
        self.hash = ''
        self.connect(self.ui.ch_k_f, QtCore.SIGNAL('clicked()'), self.k_f)
        self.ui.view_pwd.setCheckable(True)
        self.connect(self.ui.view_pwd, QtCore.SIGNAL('clicked()'), self.view)
        self.connect(self.ui.ok_btn, QtCore.SIGNAL('clicked()'), self.ok)

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

    def no(self):
        self.opf = None
        self.k_file = None
        self.close()

    def opn_dbs(self):
        self.opf = QtGui.QFileDialog.getOpenFileName(self,
                                                     'Open database',
                                                     path_installer(),
                                                     'Password manager db (*.pwmdb)')
        self.ui.addr.setText(self.opf)

    def k_f(self):
        self.k_file = QtGui.QFileDialog.getOpenFileName()
        self.ui.key_file.setText(self.k_file)

    def ok(self):
        global rec
        rec += 1
        if rec == 3:
            return
        pwd = self.ui.pwd.text()
        rep = self.ui.repwd.text()
        k_file = self.ui.key_file.text()
        opf = self.ui.addr.text()
        if pwd == rep:
            self.pwd = pwd
            if (k_file != '') and \
                    (k_file is not None) and \
                    (os.path.exists(k_file)):
                self.k_file = k_file
                hsc = self.hsc.hasMd5(self.k_file)
                self.pwd = splash(pwd, hsc)
            else:
                self.k_file = ''
                hsc = 'qwertyuioasdfghjklxcvbnmkjht'
                self.pwd = splash(pwd, hsc)
            if opf != '' and opf is not None:
                self.opf = opf
                tmp_addr = tempfile.mktemp()
                opf = open(self.opf, 'rb')
                tmp = open(tmp_addr, 'wb')
                tmp.write(opf.read())
                tmp.close()
                opf.close()
                d = self.base_crypt.decrypt_file(self.pwd, tmp_addr, self.opf)
            else:
                ers = ErorWindow(self, 'Eror', 2)
                ers.exec_()
                return
            decrypt = self.base_crypt.decrypt
            if decrypt and d:
                data = self.sql.selectDataFromTable(self.opf,
                                                ('dt',
                                                 'dostup',
                                                 'id = 1'))
                crd = self.sql.selectDataFromTable(self.opf,
                                               ('crd',
                                                'dostup',
                                                'id = 1'))
                try:
                    data = loads(data[0][0])
                    crd = loads(crd[0][0])
                    rpl = self.chifrator.decrypt_text(self.pwd, crd)
                except:
                    self.ok()
                    rpl = ''
                if rpl == data:
                    self.dostup = True
                    self.close()
                else:
                    ers = ErorWindow(self, 'Eror', 3)
                    ers.exec_()
                    self.dostup = False
                    return
        else:
            ers = ErorWindow(self, 'Eror', 1)
            ers.exec_()
            self.dostup = False
            return

rec = 0

def splash(s1, s2) -> str:
    ls1 = [str(x) for x in s1]
    ls2 = [str(x) for x in s2]
    if len(ls1) < 16 and len(ls2) < 16:
        while len(ls1) < 16:
            ls1.append('*')
        while len(ls2) < 16:
            ls2.append('*')
    random.seed(s1)
    random.shuffle(ls1)
    random.seed(s2)
    random.shuffle(ls2)
    s = ''
    for x in ls1:
        s += str(x)
    for x in ls2:
        s += str(x)
    del s1, s2, ls1, ls2
    return s[:16]


lang = ui_path()