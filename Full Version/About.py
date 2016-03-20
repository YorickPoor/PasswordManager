#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from PyQt4 import QtGui, uic
from functions import center, ui_path


class About(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        global lang
        if lang == 'En_en':
            addr = 'res/ui/about/about_en.ui'
        elif lang == 'Ru_ru':
            addr = 'res/ui/about/about_ru.ui'
        uiClass, qtBaseClass = uic.loadUiType(addr)
        del qtBaseClass
        self.ui = uiClass()
        center(self)
        self.ui.setupUi(self)
        self.setModal(True)


lang = ui_path()