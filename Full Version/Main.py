#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from PyQt4 import QtGui, uic, QtCore
from pickle import dumps, loads
import datetime as dt
import platform
import tempfile
import logging
import random
import sys
import os
from functions import *
from SqlWorker import SqlWorker
from DataSecurity import CryptBase, Chifrator
from BaseWorker import BaseCreate, BaseOpen, splash
from DataWorker import AddData, UpdateData, AddGroup, FindInBase
from Generator import PasswordGenerator
from About import About
from BlockWindow import BlockWindow
from Settings import Settings


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


global lang, theme, pwd_view, count
count = {'Internet': 0, 'Email': 0}
lang = ui_path()
theme = theme_str()
pwd_view = pwd_view_config()


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