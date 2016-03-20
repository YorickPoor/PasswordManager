#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from PyQt4 import QtGui, uic, QtCore
from pickle import dumps, loads
from Crypto.Cipher import AES
import configparser as cfg
import datetime as dt
import platform
import tempfile
import sqlite3
import hashlib
import logging
import random
import pickle
import math
import sys
import os

#


class MainWindow(QtGui.QMainWindow):
    """This a Main Window of Password Manager"""

    def __init__(self):
        addr = 'logs/{}{}'.format(dt.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), '.log')
        logging.basicConfig(filename=addr, level=logging.DEBUG)
        logging.debug('Run MainWindow.__init__();')
        QtGui.QMainWindow.__init__(self)
        global lang
        if lang == 'En_en':
            path = 'res/ui/Main/en_main.ui'
        elif lang == 'Ru_ru':
            path = 'res/ui/Main/ru_main.ui'
        uicl, qtbaseclass = uic.loadUiType(path)
        del qtbaseclass
        self.ui = uicl()
        logging.debug('Setup UI;')
        self.ui.setupUi(self)
        # create items
        self.tableWidgets = []
        self.gr_widgets = [QtGui.QTreeWidgetItem(self.ui.GroupView) for x in range(2)]
        self.gr_widgets[0].setText(0, 'Internet')
        self.gr_widgets[1].setText(0, 'Email')
        self.ingr_widgets = {'Internet': {}, 'Email': {}}
        # run some functions
        center(self)
        self.toolBarInst()
        # create some variables
        self.base_addr = None
        self.sql = SqlWorker()
        self.chifrator = Chifrator()
        self.base_chifrator = CryptBase()
        global count
        self.count = count
        self.t_itm = QtGui.QTreeWidgetItem
        self.base_pwd = None
        self.file_dlg = QtGui.QFileDialog
        self.clipboard = QtGui.QApplication.clipboard()
        self.groupData = None
        #
        self.actionAdd_data = QtGui.QAction('Add data', self)
        self.actionAdd_data.setVisible(True)
        self.actionEdit_gr = QtGui.QAction('Edit data', self)
        self.actionCopyPwd_gr = QtGui.QAction('Copy password to clipboard', self)
        self.actionCopyLogin_gr = QtGui.QAction('Copy login to clipboard', self)
        self.actionAddNewGroup_gr = QtGui.QAction('Add new group', self)
        self.actionDuplicate_gr = QtGui.QAction('Duplicate this data', self)
        self.actionDelete_gr = QtGui.QAction('Delete this data', self)
        self.actionDelete_group = QtGui.QAction('Delete this group', self)
        self.installContextMenuToGroups()
        #
        self.actionAdd_data_data = QtGui.QAction('Add data', self)
        self.actionEdit_data = QtGui.QAction('Edit data', self)
        self.actionCopyPwd_data = QtGui.QAction('Copy password to clipboard', self)
        self.actionCopyLogin_data = QtGui.QAction('Copy login to clipboard', self)
        self.actionDuplicate_data = QtGui.QAction('Duplicate this data', self)
        self.actionDelete_data = QtGui.QAction('Delete this data', self)
        self.installContextMenuToData()
        self.iconInstaller()
        #
        self.ui.actionBlock_this_window.setEnabled(False)
        self.ui.actionChange_master_pwd.setEnabled(False)
        # create connections
        self.ui.actionCreate_database.triggered.connect(self.CreateBase)
        self.ui.actionOpen_database.triggered.connect(self.OpenBase)
        self.ui.actionClose_database.triggered.connect(self.closeBase)
        self.ui.actionSave_database_as.triggered.connect(self.saveBaseAs)
        self.ui.actionAdd_data_to_base.triggered.connect(self.addDataToBase)
        self.ui.actionView_Edit_data_on_base.triggered.connect(self.editData_Group)
        self.ui.actionDelete_data.triggered.connect(self.delData_gr)
        self.ui.GroupView.itemClicked.connect(self.TableView)
        self.ui.GroupView.itemDoubleClicked.connect(self.TableView)
        self.ui.GroupView.itemEntered.connect(self.TableView)
        self.ui.GroupView.itemPressed.connect(self.TableView)
        self.ui.GroupView.itemSelectionChanged.connect(self.TableView)
        self.ui.actionExit.triggered.connect(self.close)
        self.actionAddNewGroup_gr.triggered.connect(self.addGroup_gr)
        self.actionAdd_data.triggered.connect(self.addDataToBase)
        self.actionEdit_gr.triggered.connect(self.editData_Group)
        self.actionDelete_gr.triggered.connect(self.delData_gr)
        self.actionDelete_group.triggered.connect(self.delGroup)
        self.actionCopyLogin_gr.triggered.connect(self.copyLogin_Group)
        self.actionCopyPwd_gr.triggered.connect(self.copyPassword_Group)
        self.ui.actionCopy_login_to_clipboard.triggered.connect(self.copyLogin_Group)
        self.ui.actionCopy_password_to_clipboard.triggered.connect(self.copyPassword_Group)
        self.actionEdit_gr.triggered.connect(self.editData_Group)
        self.actionAdd_data_data.triggered.connect(self.addDataToBase)
        self.actionEdit_data.triggered.connect(self.editData_Data)
        self.actionDuplicate_data.triggered.connect(self.duplicate_data_Data)
        self.actionDelete_data.triggered.connect(self.del_data_data)
        self.actionCopyLogin_data.triggered.connect(self.copyLogin_Data)
        self.actionCopyPwd_data.triggered.connect(self.copyPassword_Data)
        self.actionDuplicate_gr.triggered.connect(self.duplicate_gr)
        self.ui.actionPassword_genrator.triggered.connect(self.runPwdGenerator)
        self.ui.actionSearch_in_database.triggered.connect(self.runFindInBase)
        self.ui.actionSave_database.triggered.connect(self.saveDatabse)
        self.ui.actionBlock_this_window.triggered.connect(self.blockWindow)
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.actionSettings.triggered.connect(self.runSettings)

    def installContextMenuToGroups(self):
        self.ui.GroupView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.ui.GroupView.addAction(self.actionAdd_data)
        self.ui.GroupView.addAction(self.actionEdit_gr)
        self.ui.GroupView.addAction(self.actionAddNewGroup_gr)
        self.ui.GroupView.addAction(self.actionCopyLogin_gr)
        self.ui.GroupView.addAction(self.actionCopyPwd_gr)
        self.ui.GroupView.addAction(self.actionDuplicate_gr)
        self.ui.GroupView.addAction(self.actionDelete_gr)
        self.ui.GroupView.addAction(self.actionDelete_group)

    def installContextMenuToData(self):
        self.ui.DataView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.ui.DataView.addAction(self.actionAdd_data_data)
        self.ui.DataView.addAction(self.actionEdit_data)
        self.ui.DataView.addAction(self.actionCopyLogin_data)
        self.ui.DataView.addAction(self.actionCopyPwd_data)
        self.ui.DataView.addAction(self.actionDuplicate_data)
        self.ui.DataView.addAction(self.actionDelete_data)

    def toolBarInst(self):
        logging.debug('Running toolBarInst();')
        self.ui.toolBar.addAction(self.ui.actionCreate_database)
        self.ui.toolBar.addAction(self.ui.actionOpen_database)
        self.ui.toolBar.addAction(self.ui.actionSave_database)
        self.ui.toolBar.addAction(self.ui.actionSave_database_as)
        self.ui.toolBar.addAction(self.ui.actionClose_database)
        self.ui.toolBar_2.addAction(self.ui.actionAdd_data_to_base)
        self.ui.toolBar_2.addAction(self.ui.actionView_Edit_data_on_base)
        self.ui.toolBar_2.addAction(self.ui.actionDelete_data)
        self.ui.toolBar_2.addAction(self.ui.actionCopy_login_to_clipboard)
        self.ui.toolBar_2.addAction(self.ui.actionCopy_password_to_clipboard)
        self.ui.toolBar_2.addAction(self.ui.actionSearch_in_database)

    def iconInstaller(self):
        """ This function install icon to all menu entries"""
        logging.debug('Running iconInstaller();')
        icn = QtGui.QIcon
        # menu File
        main = 'res/icons/main.png'
        crt_dbs = 'res/icons/create.png'
        opn_dbs = 'res/icons/open.png'
        sv_dbs = 'res/icons/save.png'
        sv_dbs_as = 'res/icons/save_as.png'
        cls_dbs = 'res/icons/close.png'
        ch_prt = 'res/icons/change.png'
        w_block = 'res/icons/block.png'
        exit = 'res/icons/exit.png'
        self.setWindowIcon(icn(main))
        self.ui.actionCreate_database.setIcon(icn(crt_dbs))
        self.ui.actionOpen_database.setIcon(icn(opn_dbs))
        self.ui.actionSave_database.setIcon(icn(sv_dbs))
        self.ui.actionSave_database_as.setIcon(icn(sv_dbs_as))
        self.ui.actionClose_database.setIcon(icn(cls_dbs))
        self.ui.menuWindow_blocking.setIcon(icn(w_block))
        self.ui.actionExit.setIcon(icn(exit))
        # menu Data
        add_dt = 'res/icons/plus.png'
        edt_dt = 'res/icons/edit.png'
        del_dt = 'res/icons/del.png'
        cp_lg = 'res/icons/copy_login.png'
        cp_pwd = 'res/icons/copy_password.png'
        srh_in = 'res/icons/find.png'
        double = 'res/icons/double.png'
        self.ui.actionAdd_data_to_base.setIcon(icn(add_dt))
        self.ui.actionView_Edit_data_on_base.setIcon(icn(edt_dt))
        self.ui.actionDelete_data.setIcon(icn(del_dt))
        self.ui.actionCopy_login_to_clipboard.setIcon(icn(cp_lg))
        self.ui.actionCopy_password_to_clipboard.setIcon(icn(cp_pwd))
        self.ui.actionSearch_in_database.setIcon(icn(srh_in))
        self.actionAdd_data.setIcon(icn(add_dt))
        self.actionEdit_gr.setIcon(icn(edt_dt))
        self.actionCopyPwd_gr.setIcon(icn(cp_pwd))
        self.actionCopyLogin_gr.setIcon(icn(cp_lg))
        self.actionAddNewGroup_gr.setIcon(icn(add_dt))
        self.actionDuplicate_gr.setIcon(icn(double))
        self.actionDelete_gr.setIcon(icn(del_dt))
        self.actionDelete_group.setIcon(icn(cls_dbs))
        self.actionAdd_data_data.setIcon(icn(add_dt))
        self.actionEdit_data.setIcon(icn(edt_dt))
        self.actionCopyPwd_data.setIcon(icn(cp_pwd))
        self.actionCopyLogin_data.setIcon(icn(cp_lg))
        self.actionDuplicate_data.setIcon(icn(double))
        self.actionDelete_data.setIcon(icn(del_dt))
        # menu Advanced functions
        pwd_gen = 'res/icons/generator.png'
        settings = 'res/icons/settings.png'
        self.ui.actionPassword_genrator.setIcon(icn(pwd_gen))
        self.ui.actionSettings.setIcon(icn(settings))
        # menu Help..
        about = 'res/icons/about.png'
        self.ui.actionAbout.setIcon(icn(about))
        # icons on GroupView
        internet = 'res/icons/internet.png'
        email = 'res/icons/email.png'
        for x in self.gr_widgets:
            txt = x.text(0).lower()
            if txt == 'internet':
                x.setIcon(0, icn(internet))
            elif txt == 'email':
                x.setIcon(0, icn(email))

    def icnUnderGroup(self):
        logging.debug('Running icnUnderGroup();')
        icn = QtGui.QIcon
        vk = 'res/icons/vk.png'
        fcb = 'res/icons/facebook.png'
        ok = 'res/icons/odnoklassniki.png'
        gm = 'res/icons/gmail.png'
        twt = 'res/icons/twitter.png'
        mail_ru = 'res/icons/mail_ru.png'
        pin = 'res/icons/pinterest.png'
        internet = 'res/icons/internet.png'
        email = 'res/icons/email.png'
        default = 'res/icons/default.png'
        for x in self.ingr_widgets.keys():
            for y in self.ingr_widgets[x].values():
                txt = y.text(0).lower()
                txt = txt[txt.find('-')+1:]
                if txt == 'vk.com' or txt == 'vkontakte.com':
                    y.setIcon(0, icn(vk))
                elif txt == 'facebook.com':
                    y.setIcon(0, icn(fcb))
                elif txt == 'ok.ru' or txt == 'odnoklassniki.ru':
                    y.setIcon(0, icn(ok))
                elif txt == 'gmail.com':
                    y.setIcon(0, icn(gm))
                elif txt == 'twitter.com':
                    y.setIcon(0, icn(twt))
                elif txt == 'mail.ru':
                    y.setIcon(0, icn(mail_ru))
                elif txt == 'pin.com' or txt == 'pinterest.com':
                    y.setIcon(0, icn(pin))
                elif x == 'Email':
                    y.setIcon(0, icn(email))
                elif x == 'Internet':
                    y.setIcon(0, icn(internet))
                else:
                    y.setIcon(0, icn(default))

    def icnUnderData(self):
        logging.debug('Running icnUnderGroup();')
        icn = QtGui.QIcon
        vk = 'res/icons/vk.png'
        fcb = 'res/icons/facebook.png'
        ok = 'res/icons/odnoklassniki.png'
        gm = 'res/icons/gmail.png'
        twt = 'res/icons/twitter.png'
        mail_ru = 'res/icons/mail_ru.png'
        pin = 'res/icons/pinterest.png'
        default = 'res/icons/default.png'
        for y in self.tableWidgets:
            txt = y.text(1).lower()
            if txt == 'vk.com' or txt == 'vkontakte.com':
                y.setIcon(0, icn(vk))
            elif txt == 'facebook.com':
                y.setIcon(0, icn(fcb))
            elif txt == 'ok.ru' or txt == 'odnoklassniki.ru':
                y.setIcon(0, icn(ok))
            elif txt == 'gmail.com':
                y.setIcon(0, icn(gm))
            elif txt == 'twitter.com':
                y.setIcon(0, icn(twt))
            elif txt == 'mail.ru':
                y.setIcon(0, icn(mail_ru))
            elif txt == 'pin.com' or txt == 'pinterest.com':
                y.setIcon(0, icn(pin))
            else:
                y.setIcon(0, icn(default))

    def rndCh(self, i):
        logging.debug('Running rndCH();')
        str = 'abcdefghiklmnopqrstwxyzABCDEFGHIKLMNOPQRSTWXYZ'
        s = ''
        for x in range(i):
            s += random.choice(str)
        return s

    def CreateBase(self):
        logging.debug('Running CreateBase();')
        dial = BaseCreate(self)
        dial.setModal(True)
        dial.exec_()
        addr = dial.opf
        pwd = dial.pwd
        hsc = dial.k_hash  # 32
        if hsc is None:
            hsc = 'qwertyuioasdfghjklxcvbnmkjht'
        data = self.rndCh(16)  # text for (de/en)crypt
        if (addr is not None) and (pwd is not None):
            if os.path.exists(addr):
                os.remove(addr)
            self.ui.actionBlock_this_window.setEnabled(True)
            self.ui.actionChange_master_pwd.setEnabled(True)
            mast_pwd = pwd
            pwd = splash(pwd, hsc)
            crd = dumps(self.chifrator.encrypt_text(pwd, data))
            data = dumps(data)
            self.base_pwd = pwd
            self.base_addr = addr
            self.sql.createBase(self.base_addr)
            self.sql.createTableInBase(self.base_addr,
                                       ('gr',
                                        'table_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                                        grop TEXT NOT NULL'))
            self.sql.createTableInBase(self.base_addr,
                                       ('pwd_to_block',
                                        'pwd BLOB'))
            mast_pwd = dumps(self.chifrator.encrypt_text(mast_pwd, mast_pwd))
            self.sql.addBlobDataToTable(self.base_addr,
                                        ('pwd_to_block',
                                         'pwd', mast_pwd))
            self.sql.createTableInBase(self.base_addr,
                                       ('dostup',
                                        'id INTEGER NOT NULL PRIMARY KEY,\
                                        dt BLOB,\
                                        crd BLOB'))
            str_execute = 'INSERT INTO dostup(id, dt, crd) VALUES(1, ?, ?)'
            self.sql.executeCmdForDataTable(self.base_addr,
                                            (str_execute, data, crd))
            self.sql.createTableInBase(self.base_addr,
                                       ('Internet',
                                        'uid INTEGER PRIMARY KEY AUTOINCREMENT,\
                                        login BLOB,\
                                        pwd BLOB ,\
                                        inet BLOB'))
            self.sql.createTableInBase(self.base_addr,
                                       ('Email',
                                        'uid INTEGER PRIMARY KEY AUTOINCREMENT,\
                                        login BLOB ,\
                                        pwd BLOB ,\
                                        inet BLOB'))
            for x in self.count.keys():
                self.sql.addDataToTable(self.base_addr,
                                        ('gr',
                                         'grop',
                                         '"{}"'.format(x)))
            self.GroupView()

    def OpenBase(self):
        logging.debug('Runnng OpenBase();')
        dial = BaseOpen(self)
        dial.setModal(True)
        dial.exec_()
        addr = dial.opf
        dostup = dial.dostup
        global count
        if addr is not None and dostup:
            self.closeBase()
            self.base_addr = addr
            self.base_pwd = dial.pwd
            groups = self.sql.selectDataFromTable(self.base_addr, ('grop', 'gr'))
            groups = [groups[x][0] for x in range(len(groups))]
            for x in groups:
                data = self.sql.selectDataFromTable(self.base_addr,
                                                    ('*',
                                                     '{}'.format(x)))
                self.ui.actionBlock_this_window.setEnabled(True)
                self.ui.actionChange_master_pwd.setEnabled(True)
                group_count = 0
                for y in range(len(data)):
                    group_count += 1
                count[x] = group_count
                self.ingr_widgets[x] = {}
            miss = []
            for x in count.keys():
                if x not in groups:
                    miss.append(x)
            for x in miss:
                del count[x]
            self.count = count
            self.GroupView()

    def GroupView(self):
        logging.debug('Running View on group;')
        self.ui.GroupView.clear()
        self.ingr_widgets = {'Internet': {}, 'Email': {}}
        groups = self.sql.selectDataFromTable(self.base_addr, ('grop', 'gr'))
        groups = [groups[x][0] for x in range(len(groups))]
        self.gr_widgets = [self.t_itm(self.ui.GroupView) for x in range(len(groups))]
        [self.gr_widgets[x].setText(0, groups[x]) for x in range(len(groups))]
        self.iconInstaller()
        data = {}
        lenx = {}
        for x in groups:
            d = self.sql.selectDataFromTable(self.base_addr, ('*', x))
            lenx[x] = len(d)
            data[x] = {}
            for y in d:
                data[x][y[0]] = y
        self.count = lenx
        obj = {}
        for x in self.gr_widgets:
            obj[x.text(0)] = self.gr_widgets.index(x)
        for x in data.keys():
            self.ingr_widgets[x] = {}
        for x in data.keys():
            group = x
            for y in data[x].keys():
                uid = y
                addr = str(data[x][y][3])
                parent = self.gr_widgets[obj[group]]
                self.ingr_widgets[group][uid] = self.t_itm(parent)
                self.ingr_widgets[group][uid].setText(4, str(uid))
                self.ingr_widgets[group][uid].setText(0, addr)
        self.icnUnderGroup()

    def TableView(self):
        if self.base_addr is not None and self.base_addr != '':
            self.ui.DataView.clear()
            global lang
            logging.debug('Running View on group;')
            groups = self.sql.selectDataFromTable(self.base_addr, ('grop', 'gr'))
            if type(groups) == bool:
                return
            groups = [groups[x][0] for x in range(len(groups))]
            try:
                prnt_txt = self.ui.GroupView.currentItem().parent().text(0)
                if prnt_txt in groups:
                    self.groupData = prnt_txt
            except:
                itm_txt = self.ui.GroupView.currentItem().text(0)
                if itm_txt in groups:
                    self.groupData = itm_txt
            group = self.groupData
            data = self.sql.selectDataFromTable(self.base_addr,
                                                ('*',
                                                 '{}'.format(group)))
            if type(data) == bool:
                return
            self.tableWidgets = [x for x in range(len(data))]
            global pwd_view
            for x in data:
                i = data.index(x)
                self.tableWidgets[i] = QtGui.QTreeWidgetItem(self.ui.DataView)
                self.tableWidgets[i].setText(4, str(data[i][0]))
                self.tableWidgets[i].setText(0, str(i))
                self.tableWidgets[i].setText(1, data[i][3])
                self.tableWidgets[i].setText(2,
                                             self.chifrator.decrypt_text(self.base_pwd,
                                                                         loads(data[i][1])))
                if not pwd_view:
                    self.tableWidgets[i].setText(3, '************')
                else:
                    self.tableWidgets[i].setText(3,
                                                 self.chifrator.decrypt_text(self.base_pwd,
                                                                             loads(data[i][2])))
            self.icnUnderData()

    def duplicate_data_Data(self):
        logging.debug('Running duplicate data;')
        if self.base_addr != '' and self.base_addr is not None:
            group = self.groupData
            uid = self.ui.DataView.currentItem().text(4)
            tmp = self.sql.selectDataFromTable(self.base_addr,
                                               ('*',
                                                '{}'.format(group),
                                                'uid = {}'.format(uid)))
            tmp = tmp[0]
            old_pwd = self.chifrator.decrypt_text(self.base_pwd, loads(tmp[2]))
            old_login = self.chifrator.decrypt_text(self.base_pwd, loads(tmp[1]))
            old_inet = tmp[3]
            old_pwd = dumps(self.chifrator.encrypt_text(self.base_pwd, old_pwd))
            old_login = dumps(self.chifrator.encrypt_text(self.base_pwd, old_login))
            str_execute = 'INSERT INTO {} (login, inet, pwd)'.format(group)
            str_execute += ' VALUES(?, "{}", ?)'.format(old_inet)
            self.sql.executeSqlCmdToBlobThree(self.base_addr,
                                              str_execute,
                                              (old_login, old_pwd))
            self.GroupView()
            try:
                self.TableView()
            except:
                pass
        else:
            reply = QtGui.QMessageBox.question(self,
                                               'Database do not create',
                                               'Сreate the database before adding data to it',
                                               QtGui.QMessageBox.Yes,
                                               QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                self.CreateBase()

    def duplicate_gr(self):
        logging.debug('Running duplicate data;')
        if self.base_addr != '' and self.base_addr is not None:
            try:
                group = self.ui.GroupView.currentItem().parent().text(0)
            except:
                return
            uid = self.ui.GroupView.currentItem().text(4)
            tmp = self.sql.selectDataFromTable(self.base_addr,
                                               ('*',
                                                '{}'.format(group),
                                                'uid = {}'.format(uid)))
            tmp = tmp[0]
            old_pwd = self.chifrator.decrypt_text(self.base_pwd, loads(tmp[2]))
            old_login = self.chifrator.decrypt_text(self.base_pwd, loads(tmp[1]))
            old_inet = tmp[3]
            old_pwd = dumps(self.chifrator.encrypt_text(self.base_pwd, old_pwd))
            old_login = dumps(self.chifrator.encrypt_text(self.base_pwd, old_login))
            str_execute = 'INSERT INTO {} (login, inet, pwd)'.format(group)
            str_execute += ' VALUES(?, "{}", ?)'.format(old_inet)
            self.sql.executeSqlCmdToBlobThree(self.base_addr,
                                              str_execute,
                                              (old_login, old_pwd))
            self.GroupView()
            try:
                self.TableView()
            except:
                pass
        else:
            reply = QtGui.QMessageBox.question(self,
                                               'Database do not create',
                                               'Сreate the database before adding data to it',
                                               QtGui.QMessageBox.Yes,
                                               QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                self.CreateBase()

    def saveBaseAs(self):
        logging.debug('Running Save base as..;')
        if self.base_addr is not None and self.base_addr != '':
            if platform.system() == 'Linux':
                base_addr = self.file_dlg.getSaveFileName(self,
                                                          'Save Database as',
                                                          '/home/',
                                                          'Password manager db(*.pwmdb);;')
            elif platform.system() == 'Windows':
                base_addr = self.file_dlg.getSaveFileName(self,
                                                          'Save Database as',
                                                          'C://',
                                                          'Password manager db(*.pwmdb);;')
            if base_addr is not None and base_addr != '':
                opn_base = open(self.base_addr, 'rb')
                opn_to = open(base_addr, 'wb')
                opn_to.write(opn_base.read())
                opn_to.close()
                opn_base.close()
                QtGui.QMessageBox.information(self,
                                              'Done',
                                              'Database saved saved',
                                              QtGui.QMessageBox.Yes)
        else:
            self.CreateBase()

    def runPwdGenerator(self):
        dialog = PasswordGenerator(self)
        dialog.exec_()

    def runFindInBase(self):
        if self.base_addr != '' and self.base_addr is not None:
            dialog = FindInBase(self, self.base_pwd, self.base_addr)
            dialog.exec_()

    def blockWindow(self):
        if self.base_addr != '' and self.base_addr is not None:
            self.ui.DataView.setVisible(False)
            self.ui.GroupView.setVisible(False)
            dialog = BlockWindow(self, self.base_pwd, self.base_addr)
            dialog.exec_()
            if dialog.bool:
                self.unblockWindow()

    def unblockWindow(self):
        if self.base_addr != '' and self.base_addr is not None:
            self.ui.DataView.setVisible(True)
            self.ui.GroupView.setVisible(True)

    def addDataToBase(self):
        logging.debug('Running add data to table;')
        if self.base_addr != '' and self.base_addr is not None:
            dialog = AddData(self, self.base_addr, self.base_pwd, self.count)
            dialog.exec_()
            global count
            self.count = count
            for x in count.keys():
                self.ingr_widgets[x] = {}
            self.GroupView()
        else:
            reply = QtGui.QMessageBox.question(self,
                                               'Database do not create',
                                               'Сreate the database before adding data to it',
                                               QtGui.QMessageBox.Yes,
                                               QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                self.CreateBase()
                del reply

    def editData_Data(self):
        logging.debug('Running edit data;')
        if self.base_addr != '' and self.base_addr is not None:
            data = {'uid': None, 'group': None}
            group = self.groupData
            uid = self.ui.DataView.currentItem().text(4)
            data['uid'] = uid
            data['group'] = group
            dialog = UpdateData(self, self.base_addr, self.base_pwd, data)
            dialog.exec_()
            self.ui.GroupView.setCurrentItem(self.gr_widgets[0])
            self.GroupView()
            try:
                self.TableView()
            except:
                pass
        else:
            reply = QtGui.QMessageBox.question(self,
                                               'Database do not create',
                                               'Сreate the database before adding data to it',
                                               QtGui.QMessageBox.Yes,
                                               QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                self.CreateBase()

    def editData_Group(self):
        logging.debug('Running edit data;')
        if self.base_addr != '' and self.base_addr is not None:
            data = {'uid': None, 'group': None}
            try:
                group = self.ui.GroupView.currentItem().parent().text(0)
            except:
                return
            uid = self.ui.GroupView.currentItem().text(4)
            data['uid'] = uid
            data['group'] = group
            dialog = UpdateData(self, self.base_addr, self.base_pwd, data)
            dialog.exec_()
            self.GroupView()
        else:
            reply = QtGui.QMessageBox.question(self,
                                               'Database do not create',
                                               'Сreate the database before adding data to it',
                                               QtGui.QMessageBox.Yes,
                                               QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                self.CreateBase()

    def delData_gr(self):
        logging.debug('Running del data;')
        if self.base_addr != '' and self.base_addr is not None:
            try:
                group = self.ui.GroupView.currentItem().parent().text(0)
            except:
                return
            uid = self.ui.GroupView.currentItem().text(4)
            self.sql.delDataInTable(self.base_addr,
                                    ('{}'.format(group),
                                     'uid = {}'.format(uid)))
            self.GroupView()
        else:
            reply = QtGui.QMessageBox.question(self,
                                               'Database do not create',
                                               'Сreate the database before adding data to it',
                                               QtGui.QMessageBox.Yes,
                                               QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                self.CreateBase()
                self.addDataToBase()

    def del_data_data(self):
        logging.debug('Running del data;')
        if self.base_addr != '' and self.base_addr is not None:
            group = self.groupData
            uid = self.ui.DataView.currentItem().text(4)
            self.sql.delDataInTable(self.base_addr,
                                    ('{}'.format(group),
                                     'uid = {}'.format(uid)))
            self.GroupView()

    def runSettings(self):
        dialog = Settings(self)
        dialog.exec_()

    def delGroup(self):
        if self.base_addr != '' and self.base_addr is not None:
            try:
                group = self.ui.GroupView.currentItem().text(0)
            except:
                return
            global count
            if group in count.keys():
                reply = QtGui.QMessageBox.question(self,
                                                   'Warning!!!',
                                                   'You will lose all data in this group.\n\
                                                   Are you sure to do it?',
                                                   QtGui.QMessageBox.Yes,
                                                   QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    self.sql.deleteTableInBase(self.base_addr, group)
                    self.sql.delDataInTable(self.base_addr,
                                            ('gr',
                                             'grop = "{}"'.format(group)))
                    del count[group]
                    self.GroupView()
            else:
                return

    def about(self):
        dialog = About(self)
        dialog.exec_()

    def saveDatabse(self):
        if self.base_addr == '' or self.base_addr is None:
            self.CreateBase()
        else:
            pass

    def copyLogin_Group(self):
        logging.debug('Running copy login;')
        try:
            group = self.ui.GroupView.currentItem().parent().text(0)
        except:
            return
        uid = self.ui.GroupView.currentItem().text(4)
        txt = self.sql.selectDataFromTable(self.base_addr,
                                           ('login',
                                           '{}'.format(group),
                                           'uid = {}'.format(uid)))
        login = self.chifrator.decrypt_text(self.base_pwd,
                                            loads(txt[0][0]))
        self.clipboard.clear()
        self.clipboard.setText(login)

    def copyLogin_Data(self):
        logging.debug('Running copy login;')
        group = self.groupData
        uid = self.ui.DataView.currentItem().text(4)
        login = self.sql.selectDataFromTable(self.base_addr,
                                             ('login',
                                              '{}'.format(group),
                                              'uid = {}'.format(uid)))
        login = loads(login[0][0])
        login = self.chifrator.decrypt_text(self.base_pwd, login)
        self.clipboard.clear()
        self.clipboard.setText(login)

    def copyPassword_Data(self):
        logging.debug('Running copy pwd;')
        group = self.groupData
        uid = self.ui.DataView.currentItem().text(4)
        pwd = self.sql.selectDataFromTable(self.base_addr,
                                             ('pwd',
                                              '{}'.format(group),
                                              'uid = {}'.format(uid)))
        pwd = loads(pwd[0][0])
        pwd = self.chifrator.decrypt_text(self.base_pwd, pwd)
        self.clipboard.clear()
        self.clipboard.setText(pwd)

    def copyPassword_Group(self):
        logging.debug('Running copy login;')
        try:
            group = self.ui.GroupView.currentItem().parent().text(0)
        except:
            return
        uid = self.ui.GroupView.currentItem().text(4)
        txt = self.sql.selectDataFromTable(self.base_addr,
                                           ('pwd',
                                           '{}'.format(group),
                                           'uid = {}'.format(uid)))
        pwd = self.chifrator.decrypt_text(self.base_pwd,
                                            loads(txt[0][0]))
        self.clipboard.clear()
        self.clipboard.setText(pwd)

    def addGroup_gr(self):
        if self.base_addr is not None and self.base_addr != '':
            dialog = AddGroup(self, self.base_addr)
            dialog.exec_()
            self.GroupView()
        else:
            reply = QtGui.QMessageBox.question(self,
                                               'Database do not create',
                                               'Сreate the database before adding group to it',
                                               QtGui.QMessageBox.Yes,
                                               QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                self.CreateBase()
                self.addGroup_gr()

    def closeBase(self):
        logging.debug('Running close base;')
        if self.base_addr is not None and self.base_addr != '':
            tmp_addr = tempfile.mktemp()
            opf = open(self.base_addr, 'rb')
            tmp = open(tmp_addr, 'wb')
            tmp.write(opf.read())
            tmp.close()
            opf.close()
            self.base_chifrator.encrypt_file(self.base_pwd, tmp_addr, self.base_addr)
            self.ui.GroupView.clear()
            self.ui.DataView.clear()
            self.gr_widgets = [QtGui.QTreeWidgetItem(self.ui.GroupView) for x in range(2)]
            self.gr_widgets[0].setText(0, 'Internet')
            self.gr_widgets[1].setText(0, 'Email')
            self.iconInstaller()

    def closeEvent(self, event):
        logging.debug('CloseEvent ;')
        logs_list = list(os.walk('logs'))[0][2]
        for x in logs_list:
            x = 'logs/' + x
            if x[-3:] != 'log':
                continue
            opf = open(x, 'rt')
            if 'Eror' not in opf.read():
                opf.close()
                os.remove(x)
        if self.base_addr is not None and self.base_addr != '':
            tmp_addr = tempfile.mktemp()
            opf = open(self.base_addr, 'rb')
            tmp = open(tmp_addr, 'wb')
            tmp.write(opf.read())
            tmp.close()
            opf.close()
            self.base_chifrator.encrypt_file(self.base_pwd, tmp_addr, self.base_addr)
        self.clipboard.clear()
        event.accept()

#


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
        if not ".pwmdb" in self.opf:
            self.opf += ".pwmdb"
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

#


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
            global decrypt
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
                    rpl = ''
                    self.ok()
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

#


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

#


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

#


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

#


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

#


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

#


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

#


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

#


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

#


class SqlWorker():
    def __init__(self):
        logging.debug('Create SqlWorker() object;')

    def abspath(self, path):
        return os.path.abspath(path)

    def createBase(self, path):
        """
        path = path to database
        """
        try:
            path = self.abspath(path)
            base = sqlite3.connect(path)
            base.close()
            del base, path
            return True
        except Exception as e:
            logging.error('Eror in SQLWorker;')
            logging.error('Eror on create base;')
            logging.error('Eror type : {};'.format(e.__class__))
            logging.error('Eror description : {};'.format(e.__str__()))
            del path
            return False

    def createTableInBase(self, path, args):
        """
        args = [
        'table_name',
        "1_row row_type some conditions,
         2_row row_type some conditions,
         n_row row_type some conditions,
         ..."]
        """
        path = self.abspath(path)
        base = sqlite3.connect(path)
        cursor = base.cursor()
        str_execute = 'CREATE TABLE {} ({})'.format(*args)
        try:
            cursor.execute(str_execute)
            base.commit()
            base.close()
            del base, cursor, str_execute, path, args
            return True
        except Exception as e:
            logging.error('Eror in SQLWorker;')
            logging.error('Eror on create table in base;')
            logging.error('Eror type : {};'.format(e.__class__))
            logging.error('Eror description : {};'.format(e.__str__()))
            base.close()
            del str_execute, path, args
            return False

    def addDataToTable(self, path, args):
        """
        args = ['table_name',
        "row_name1,
         row_name2,
         row_namen...",
        "row_value1,
         row_value2,
         row_valuen..."]

         or
         args = ['table_name',
        "row_value1,
         row_value2,
         row_valuen..."]
        """
        path = self.abspath(path)
        base = sqlite3.connect(path)
        cursor = base.cursor()
        if len(args) == 3:
            str_execute = 'INSERT INTO {} ({}) VALUES({})'.format(*args)
        elif len(args) == 2:
            str_execute = 'INSERT INTO {} VALUES({})'.format(*args)
        try:
            cursor.execute(str_execute)
            base.commit()
            base.close()
            del base, cursor, str_execute, path, args
            return True
        except Exception as e:
            logging.error('Eror in SQLWorker;')
            logging.error('Eror on add data to base;')
            logging.error('Eror type : {};'.format(e.__class__))
            logging.error('Eror description : {};'.format(e.__str__()))
            base.close()
            del str_execute, path, args
            return False

    def addBlobDataToTable(self, path, args):
        """
        args = ['table_name',
                'colum_1,',
                blob_data]
        args = ['table_name',
                'colum_1,',
                blob_data,
                'condition']
        """
        path = self.abspath(path)
        base = sqlite3.connect(path)
        cursor = base.cursor()
        try:
            if len(args) == 3:
                str_execute = 'INSERT INTO {}({}) VALUES'.format(args[0], args[1])
                str_execute += '(?)'
            elif len(args) == 4:
                str_execute = 'INSERT INTO {}({}) VALUES'.format(args[0], args[1])
                str_execute += '(?)'
                str_execute += ' WHERE {}'.format(args[3])
            data = self.convertDataToBlob(args[2])
            cursor.execute(str_execute, (data,))
            base.commit()
            base.close()
            del base, cursor, str_execute, path, args, data
            return True
        except Exception as e:
            logging.error('Eror in SQLWorker;')
            logging.error('Eror on add blob data to base;')
            logging.error('Eror type : {};'.format(e.__class__))
            logging.error('Eror description : {};'.format(e.__str__()))
            base.close()
            del str_execute, path, args
            return False

    def convertDataToBlob(self, data):
        return sqlite3.Binary(data)

    def selectDataFromTable(self, path, args):
        """
        args = ['row-1 , row-2, row-n',
                'table_name',
                'condition']
        or
        args = ['row-1 , row-2, row-n',
                'table_name']
        """
        path = self.abspath(path)
        base = sqlite3.connect(path)
        cursor = base.cursor()
        if len(args) == 2:
            str_execute = 'SELECT {} FROM {}'.format(*args)
        elif len(args) == 3:
            str_execute = 'SELECT {} FROM {} WHERE {}'.format(*args)
        try:
            cursor.execute(str_execute)
            data = cursor.fetchall()
            base.commit()
            base.close()
            del base, cursor, str_execute, path, args
            return data
        except Exception as e:
            logging.error('Eror in SQLWorker;')
            logging.error('Eror on select data from base;')
            logging.error('Eror type : {};'.format(e.__class__))
            logging.error('Eror description : {};'.format(e.__str__()))
            base.close()
            del str_execute, path, args
            return False

    def updateDataInTable(self, path, args):
        """
        args = ['table_name',
                'row_name',
                'new_data on row',
                'condition']
        or
        args = ['table_name',
                'row_name',
                'new_data on row',
                'row_name',
                'old_data_on_row']
        """
        path = self.abspath(path)
        base = sqlite3.connect(path)
        cursor = base.cursor()
        if len(args) == 4:
            str_execute = 'UPDATE {} SET {} = {} WHERE {}'.format(*args)
        elif len(args) == 5:
            str_execute = 'UPDATE {} SET {} = {} WHERE {} = {}'.format(*args)
        try:
            cursor.execute(str_execute)
            base.commit()
            base.close()
            del base, cursor, str_execute, path, args
            return True
        except Exception as e:
            logging.error('Eror in SQLWorker;')
            logging.error('Eror on update data in table;')
            logging.error('Eror type : {};'.format(e.__class__))
            logging.error('Eror description : {};'.format(e.__str__()))
            base.close()
            del str_execute, path, args
            return False

    def delDataInTable(self, path, args):
        """
        args = ['table_name',
                'conditions']
        or
        args = ['table_name',
                'row_name',
                'row_data']
        """
        path = self.abspath(path)
        base = sqlite3.connect(path)
        cursor = base.cursor()
        if len(args) == 2:
            str_execute = 'DELETE FROM {} WHERE {}'.format(*args)
        elif len(args) == 3:
            str_execute = 'DELETE FROM {} WHERE {} = {}'.format(*args)
        try:
            cursor.execute(str_execute)
            base.commit()
            base.close()
            del base, cursor, str_execute, path, args
            return True
        except Exception as e:
            logging.error('Eror in SQLWorker;')
            logging.error('Eror on delete data to base;')
            logging.error('Eror type : {};'.format(e.__class__))
            logging.error('Eror description : {};'.format(e.__str__()))
            base.close()
            del str_execute, path, args
            return False

    def addNewColumnInTable(self, path, args):
        """
        args = ['table_name',
                'New_column_name',
                'type of new column']
        """
        path = self.abspath(path)
        base = sqlite3.connect(path)
        cursor = base.cursor()
        str_execute = 'ALERT TABLE {} ADD COLUMN {} {}'.format(*args)
        try:
            cursor.execute(str_execute)
            base.commit()
            base.close()
            del base, cursor, str_execute, path, args
            return True
        except Exception as e:
            logging.error('Eror in SQLWorker;')
            logging.error('Eror on add new column to base;')
            logging.error('Eror type : {};'.format(e.__class__))
            logging.error('Eror description : {};'.format(e.__str__()))
            base.close()
            del str_execute, path, args
            return False

    def renameTableInBase(self, path, old_name, new_name):
        path = self.abspath(path)
        base = sqlite3.connect(path)
        cursor = base.cursor()
        str_execute = 'ALERT TABLE {} RENAME TO {}'.format(old_name, new_name)
        try:
            cursor.execute(str_execute)
            base.commit()
            base.close()
            del base, cursor, str_execute, path, old_name, new_name
            return True
        except Exception as e:
            logging.error('Eror in SQLWorker;')
            logging.error('Eror on rename table in base;')
            logging.error('Eror type : {};'.format(e.__class__))
            logging.error('Eror description : {};'.format(e.__str__()))
            base.close()
            del str_execute, path, old_name, new_name
            return False

    def executeSqlCmd(self, path, cmd, ret_data):
        """
        path(str) - path to base
        cmd(str) - once SQL command
        ret_data(bool) - cmd is return some data or no (True os False)
        """
        path = self.abspath(path)
        base = sqlite3.connect(path)
        cursor = base.cursor()
        if ret_data:
            try:
                cursor.execute(cmd)
                data = cursor.fetchall()
                base.commit()
                base.close()
                del base, cursor, ret_data
                return data, True
            except Exception as e:
                logging.error('Eror in SQLWorker;')
                logging.error('Eror on execute sql cmd;')
                logging.error('Eror: {};'.format(e.args))
                base.close()
                del ret_data
                return None, False
        else:
            try:
                cursor.execute(cmd)
                base.commit()
                base.close()
                del base, cursor, ret_data
                return True
            except Exception as e:
                logging.error('Eror in SQLWorker;')
                logging.error('Eror on execute sql cmd;')
                logging.error('Eror type : {};'.format(e.__class__))
                logging.error('Eror description : {};'.format(e.__str__()))
                base.close()
                del ret_data
                return False

    def executeSqlCmdToBlob(self, path, cmd, blob_data):
        """
        path(str) - path to base
        cmd(str) - once SQL command
        ret_data(bool) - cmd is return some data or no (True os False)
        """
        path = self.abspath(path)
        base = sqlite3.connect(path)
        cursor = base.cursor()
        try:
            cursor.execute(cmd, (self.convertDataToBlob(blob_data[0]), self.convertDataToBlob(blob_data[1])))
            base.commit()
            base.close()
            del base, cursor, path, blob_data
            return True
        except Exception as e:
            logging.error('Eror in SQLWorker;')
            logging.error('Eror on execute sql cmd;')
            logging.error('Eror type : {};'.format(e.__class__))
            logging.error('Eror description : {};'.format(e.__str__()))
            base.close()
            del path, blob_data
            return False

    def executeSqlCmdToBlobThree(self, path, cmd, blob_data):
        """
        path(str) - path to base
        cmd(str) - once SQL command
        ret_data(bool) - cmd is return some data or no (True os False)
        """
        path = self.abspath(path)
        base = sqlite3.connect(path)
        cursor = base.cursor()
        try:
            cursor.execute(cmd, (self.convertDataToBlob(blob_data[0]),
                                 self.convertDataToBlob(blob_data[1])))
            base.commit()
            base.close()
            del base, cursor, path, blob_data
            return True
        except Exception as e:
            logging.error('Eror in SQLWorker;')
            logging.error('Eror on execute sql cmd;')
            logging.error('Eror type : {};'.format(e.__class__))
            logging.error('Eror description : {};'.format(e.__str__()))
            base.close()
            del path, blob_data
            return False

    def executeSqlCmdToBlobOne(self, path, cmd, blob_data):
        """
        path(str) - path to base
        cmd(str) - once SQL command
        """
        path = self.abspath(path)
        base = sqlite3.connect(path)
        cursor = base.cursor()
        try:
            cursor.execute(cmd, (self.convertDataToBlob(blob_data), ))
            base.commit()
            base.close()
            del base, cursor, path, blob_data
            return True
        except Exception as e:
            logging.error('Eror in SQLWorker;')
            logging.error('Eror on execute sql cmd;')
            logging.error('Eror type : {};'.format(e.__class__))
            logging.error('Eror description : {};'.format(e.__str__()))
            base.close()
            del path, blob_data
            return False

    def executeCmdForDataTable(self, path, args):
        path = self.abspath(path)
        base = sqlite3.connect(path)
        cursor = base.cursor()
        try:
            cursor.execute(args[0], (args[1], args[2]))
            base.commit()
            base.close()
            del base, cursor, path, args
            return True
        except Exception as e:
                logging.error('Eror in SQLWorker;')
                logging.error('Eror on execute sql cmd for data table;')
                logging.error('Eror type : {};'.format(e.__class__))
                logging.error('Eror description : {};'.format(e.__str__()))
                base.close()
                del path, args
                return False

    def deleteTableInBase(self, path, table_name):
        path = self.abspath(path)
        base = sqlite3.connect(path)
        cursor = base.cursor()
        str_execute = 'DROP TABLE {}'.format(table_name)
        try:
            cursor.execute(str_execute)
            base.commit()
            base.close()
            del base, path, cursor, table_name
            return True
        except Exception as e:
                logging.error('Eror in SQLWorker;')
                logging.error('Eror on delete table in base;')
                logging.error('Eror type : {};'.format(e.__class__))
                logging.error('Eror description : {};'.format(e.__str__()))
                base.close()
                del cursor, table_name
                return False

#


class Hasher():
    def hasMd5(self, filename):
        """
        ===================
        calculating md5 hash
        ===================
        расчитывает md5 хеш
        ===================
        """

        m = hashlib.md5()
        f = open(filename, 'rb')
        c = f.read()
        m.update(c)
        f.close()
        del f, c
        return m.hexdigest()

    def hasMd5Str(self, content):
        """
        ======================================
        calculating md5 hash of string content
        ======================================
        расчитывает md5 хеш строки content
        ======================================
        """

        content = content.encode('utf-8')
        m = hashlib.md5()
        m.update(content)
        del content
        return m.hexdigest()

#


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

#


class Chifrator():
    def __init__(self):
        logging.debug('Create Chifrator() object;')

    def _keyget(self, s) -> str:
        return hashlib.md5(s.encode('utf-8')).hexdigest()[:16]

    def split_n(self, lst, n) -> list or str:
        return [lst[z:z + n] for z in range(0, len(lst), n)]

    def decrypt_text(self, pwd, txt) -> str:
        pwd = self._keyget(pwd)
        txt = txt.replace('[', '')
        txt = txt.replace(']', '')
        txt = txt.split(',')
        txt = [int(x) for x in txt]
        txt = self.split_n(txt, 16)
        txt = tuple(txt)
        prm1 = [bytes() for x in txt]
        decryptor = AES.new(pwd, AES.MODE_CBC, pwd)
        for x in txt:
            i = txt.index(x)
            for y in txt[i]:
                prm1[i] += bytes([y])
        ret_data = bytes()
        for x in prm1:
            ret_data += decryptor.decrypt(x)
        ret_data = str(ret_data, 'utf-8')
        while ret_data[-1] == '\t':
            ret_data = ret_data[:-1]
        del txt, pwd, prm1, decryptor
        return ret_data

    def encrypt_text(self, pwd, txt) -> str:
        pwd = self._keyget(pwd)
        txt = [bytes(x, 'utf-8') for x in txt]
        cryptor = AES.new(pwd, AES.MODE_CBC, pwd)
        p1 = bytes()
        for x in txt:
            p1 += x
        txt = self.split_n(p1, 16)
        ex = []
        for x in txt:
            if len(x) < 16:
                x += bytes('\t', 'utf-8') * (16 - len(x))
            ex.append(cryptor.encrypt(x))
        prm1 = bytes()
        ret_data = []
        for x in ex:
            prm1 += x
        for x in prm1:
            ret_data.append(x)
        del pwd, txt, cryptor, ex, prm1
        return str(ret_data)

#


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
        """
        p = self.strenght_middle(s)
        p = p.replace('t', 'Y')
        p = p.replace('i', 'T')
        p = p.replace('for', '4')
        p = p.replace('s', '$')
        p = p.replace('j', 'R')
        p = p.replace('s', 'Z')
        return p

#


class CryptBase():
    def __init__(self):
        logging.debug('Create CryptBase() object;')

    def _keyget(self, s) -> str:
        return hashlib.md5(s.encode('utf-8')).hexdigest()[:16]

    def split_n(self, lst, n) -> list or str:
        return [lst[z:z + n] for z in range(0, len(lst), n)]

    def encrypt_file(self, pwd, last_addr, new_addr) -> bool:
        try:
            last_addr = os.path.abspath(last_addr)
            new_addr = os.path.abspath(new_addr)
            pwd = self._keyget(pwd)
            filesize = os.stat(last_addr)[6]
            counter = filesize / 16 if (filesize % 16 == 0) else (round(filesize / 16)) + 1
            file = open(last_addr, 'rb')
            data = file.read(16)
            new_file = open(new_addr, 'wb')
            iv = os.urandom(16)
            new_file.write(iv)
            new_file.close()
            encryptor = AES.new(pwd, AES.MODE_CBC, iv)
            i = 0
            while i < counter:
                data = data if len(data) >= 16 else data + b'\t' * (16 - len(data))
                rtd = encryptor.encrypt(data)
                new_file = open(new_addr, 'ab')
                new_file.write(rtd)
                new_file.close()
                i += 1
                data = file.read(16)
            file.close()
            del last_addr, pwd, new_addr, data, file, i, encryptor, counter
            global encrypt
            encrypt = True
            return True
        except Exception as e:
            logging.error('Eror on encrypting base;')
            logging.error('File size: {};'.format(os.stat(last_addr)[6]))
            logging.error('Eror {};'.format(e.args))

    def decrypt_file(self, pwd, last_addr, new_addr) -> bool:
        try:
            last_addr = os.path.abspath(last_addr)
            new_addr = os.path.abspath(new_addr)
            pwd = self._keyget(pwd)
            filesize = os.stat(last_addr)[6]
            counter = filesize / 16 if (filesize % 16 == 0) else (round(filesize / 16)) + 1
            counter -= 1
            file = open(last_addr, 'rb')
            iv = file.read(16)
            data = file.read(16)
            new_file = open(new_addr, 'wb')
            new_file.close()
            decryptor = AES.new(pwd, AES.MODE_CBC, iv)
            i = 0
            while i < counter:
                rtd = decryptor.decrypt(data)
                if i + 1 == counter:
                    while bytes([rtd[-1]]) == b'^':
                        rtd = rtd[:len(rtd) - 1]
                new_file = open(new_addr, 'ab')
                new_file.write(rtd)
                new_file.close()
                i += 1
                data = file.read(16)
            file.close()
            del last_addr, pwd, new_addr, data, file, i, decryptor, counter
            global decrypt
            decrypt = True
            return True
        except Exception as e:
            logging.error('Eror on decrypting base;')
            logging.error('File size {};'.format(os.stat(last_addr)[6]))
            logging.error('Eror {};'.format(e.args))

#


def enthropy(pwd) -> int:
    l = len(pwd)
    x = pow(75, l)
    out = math.log2(x)
    del l, x
    return out

#


def center(self):
        """This function displays programm winndow on center of user screen"""
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        width = (screen.width() - size.width()) / 2
        height = (screen.height() - size.height()) / 2
        self.move(width, height)

#


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

#


def ui_path() -> str:
        """This function return a address on ui file"""
        parser = cfg.ConfigParser()
        path = 'res/config.ini'
        parser.read(path)
        lang = parser['USER']['language']
        del parser, path
        return lang

#


def runner():
    try:
        os.mkdir('logs')
    except:
        pass
    if not os.path.exists('res'):
        logging.error('delete files;')
        sys.exit(0)

#


def theme_str() -> str:
    parser = cfg.ConfigParser()
    path = 'res/config.ini'
    parser.read(path)
    theme_s = parser['USER']['Theme']
    del parser, path
    return theme_s

#


def themeInstaller():
    global theme
    if theme != 'Normal':
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(theme))

#


def pwd_view_config() -> bool:
    parser = cfg.ConfigParser()
    path = 'res/config.ini'
    parser.read(path)
    pwd_v = parser['USER']['passwords_view']
    del parser, path
    if pwd_v == 'True':
        return True
    else:
        return False

#


def path_installer() -> str:
    pl = platform.system()
    if pl == 'Windows':
        return 'C://'
    elif pl == 'Linux':
        return '/home/'



count = {'Internet': 0, 'Email': 0}
lang = ui_path()
theme = theme_str()
pwd_view = pwd_view_config()
rec = 0

def main() -> None:
    """This a main function on file"""
    runner()
    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    themeInstaller()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
