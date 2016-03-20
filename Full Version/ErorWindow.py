#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from PyQt4 import QtGui, uic
from SqlWorker import SqlWorker
from functions import ui_path, center


class ErorWindow(QtGui.QDialog):
    def __init__(self, parent, title, err_number):
        QtGui.QDialog.__init__(self, parent)
        uiClass, qtBaseClass = uic.loadUiType('res/ui/err/err_dlg.ui')
        del qtBaseClass
        self.ui = uiClass()
        self.ui.setupUi(self)
        self.setModal(True)
        self.nm = err_number
        center(self)
        self.setWindowTitle(title)
        global lang
        self.ui.err_text.setText(self.ertxret(lang))

    def ertxret(self, lang):
        sql = SqlWorker()
        if self.nm == 1 and lang == 'En_en':
            data = sql.selectDataFromTable('res/src/data/errs.pwdb',
                                           ('*', 'erors_eng', 'number = 1'))
            return data[0][1]
        elif self.nm == 2 and lang == 'En_en':
            data = sql.selectDataFromTable('res/src/data/errs.pwdb',
                                           ('*', 'erors_eng', 'number = 2'))
            return data[0][1]
        elif self.nm == 3 and lang == 'En_en':
            data = sql.selectDataFromTable('res/src/data/errs.pwdb',
                                           ('*', 'erors_eng', 'number = 3'))
            return data[0][1]
        elif self.nm == 1 and lang == 'Ru_ru':
            data = sql.selectDataFromTable('res/src/data/errs.pwdb',
                                           ('*', 'erors_rus', 'number = 1'))
            return data[0][1]
        elif self.nm == 2 and lang == 'Ru_ru':
            data = sql.selectDataFromTable('res/src/data/errs.pwdb',
                                           ('*', 'erors_rus', 'number = 2'))
            return data[0][1]
        elif self.nm == 3 and lang == 'Ru_ru':
            data = sql.selectDataFromTable('res/src/data/errs.pwdb',
                                           ('*', 'erors_rus', 'number = 3'))
            return data[0][1]

lang = ui_path()