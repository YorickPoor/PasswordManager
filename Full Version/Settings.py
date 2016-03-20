#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from PyQt4 import QtGui, uic
import configparser as cfg
from functions import center, ui_path


class Settings(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        global lang
        if lang == 'En_en':
            addr = 'res/ui/settings/en_settings.ui'
        elif lang == 'Ru_ru':
            addr = 'res/ui/settings/ru_settings.ui'
        uiClass, qtBaseClass = uic.loadUiType(addr)
        del qtBaseClass
        self.ui = uiClass()
        center(self)
        self.ui.setupUi(self)
        self.setModal(True)
        parser = cfg.ConfigParser()
        parser.read('res/config.ini')
        if parser['USER']['passwords_view'] == 'True':
            self.ui.pwd_v.setChecked(True)
        self.ui.ok.clicked.connect(self.ok)
        self.ui.no.clicked.connect(self.no)

    def ok(self):
        langs = 'En_en' if self.ui.lang.currentText() == 'English' else 'Ru_ru'
        parser = cfg.ConfigParser()
        path = 'res/config.ini'
        path = open(path, 'wt')
        parser['DEFAULT'] = {'Theme': 'Normal',
                             'passwords_view': 'False',
                             'language': 'En_en'}
        parser['USER'] = {'Theme': self.ui.theme.currentText(),
                          'passwords_view': str(self.ui.pwd_v.isChecked()),
                          'language': langs}
        parser.write(path)
        QtGui.QMessageBox.question(self,
                                   'Restarting',
                                   'Please restart program to saving changes!!!',
                                   QtGui.QMessageBox.Yes)

    def no(self):
        self.close()

lang = ui_path()