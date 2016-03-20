#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from PyQt4 import QtGui, uic
from SqlWorker import SqlWorker
from DataSecurity import Chifrator
from pickle import loads
from functions import center, ui_path


class BlockWindow(QtGui.QDialog):
    def __init__(self, parent, base_pwd, base_addr):
        QtGui.QDialog.__init__(self, parent)
        global lang
        if lang == 'En_en':
            addr = 'res/ui/block/en_block.ui'
        elif lang == 'Ru_ru':
            addr = 'res/ui/block/ru_block.ui'
        uiClass, qtBaseClass = uic.loadUiType(addr)
        del qtBaseClass
        self.ui = uiClass()
        center(self)
        self.ui.setupUi(self)
        self.base_pwd = base_pwd
        self.sql = SqlWorker()
        self.chi = Chifrator()
        self.base_addr = base_addr
        self.bool = False
        self.ui.ok.clicked.connect(self.ok)

    def ok(self):
        pwd = self.ui.pwd.text()
        repwd = self.sql.selectDataFromTable(self.base_addr,
                                             ('*', 'pwd_to_block'))
        repwd = self.chi.decrypt_text(pwd, loads(repwd[0][0]))
        if pwd == repwd:
            self.bool = True
            self.close()
        else:
            self.bool = False
            return

lang = ui_path()