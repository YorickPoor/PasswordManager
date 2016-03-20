#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from PyQt4 import QtGui, uic
import random
import pickle
from functions import center, enthropy, ui_path


class PasswordGenerator(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        global lang
        if lang == 'En_en':
            addr = 'res/ui/pwd_gen/en_pwd_gen.ui'
        elif lang == 'Ru_ru':
            addr = 'res/ui/pwd_gen/ru_pwd_gen.ui'
        uiClass, qtBaseClass = uic.loadUiType(addr)
        del qtBaseClass
        self.ui = uiClass()
        center(self)
        self.ui.setupUi(self)
        self.generator = MethGen()
        self.ui.prBar.setMaximum(300)
        self.ui.prBar.setMinimum(0)
        self.clipboard = QtGui.QApplication.clipboard()
        self.ui.generate.clicked.connect(self.generate)
        self.ui.copy.clicked.connect(self.copy)

    def generate(self):
        txt = self.ui.cbb.currentText()
        if txt == 'Hard password' or txt == 'Очень сложный':
            pwd = self.generator.strength_hard(self.generator.voider(8))
            self.ui.pwd.setText(pwd)
            pr = enthropy(pwd)
            self.ui.prBar.setValue(int(pr))
        elif txt == 'Middle strength password' or txt == 'Средний пароль':
            pwd = self.generator.strength_hard(self.generator.voider(6))
            self.ui.pwd.setText(pwd)
            pr = enthropy(pwd)
            self.ui.prBar.setValue(int(pr))
        elif txt == 'Low strength password' or txt == 'Простой пароль':
            pwd = self.generator.strength_hard(self.generator.voider(3))
            self.ui.pwd.setText(pwd)
            pr = enthropy(pwd)
            self.ui.prBar.setValue(int(pr))

    def copy(self):
        self.clipboard.clear()
        self.clipboard.setText(self.ui.pwd.text())


class MethGen():
    def generator(self):
        """
        this function generate random numbers for diceware password generator
        """
        one = random.randint(1, 6)
        two = random.randint(1, 6)
        three = random.randint(1, 6)
        four = random.randint(1, 6)
        five = random.randint(1, 6)
        x = str(one) + str(two) + str(three) + str(four) + str(five)
        del one, two, three, four, five
        return x

    def loader(self):
        """
        this function load the dict of diceware words and keys
        """
        opf = 'res/src/data/dict.dll'
        f = open(opf, 'rb')
        d = pickle.load(f)
        del opf, f
        return d

    def voider(self, do):
        """
        this function generate password on method diceware
        :param do: count of generate words
        """
        p = [self.generator() for x in range(do)]
        di = self.loader()
        en = ''
        for x in p:
            en += di[x] + ' '
        del p, di
        return en

    def strenght_middle(self, s):
        """
        this function do password more strenght
        :param s: string of password
        """
        p = str(s)
        del s
        p = p.replace('a', '@')
        p = p.replace('o', '()')
        p = p.replace('you', "u")
        p = p.replace(' ', '"')
        p = p[0:len(p) - 1]
        return p

    def strength_hard(self, s):
        """
        this function do password very big strength
        :param s: string of password
        """
        p = self.strenght_middle(s)
        p = p.replace('t', 'Y')
        p = p.replace('i', 'T')
        p = p.replace('for', '4')
        p = p.replace('s', '$')
        p = p.replace('j', 'R')
        p = p.replace('s', 'Z')
        return p

lang = ui_path()