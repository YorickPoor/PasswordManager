import math
from PyQt4 import QtGui
import configparser as cfg
import logging
import os
import sys
import platform


def enthropy(pwd) -> int:
    l = len(pwd)
    x = pow(75, l)
    out = math.log2(x)
    del l, x
    return out


def center(self):
        """This function displays program window on center of user screen"""
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        width = (screen.width() - size.width()) / 2
        height = (screen.height() - size.height()) / 2
        self.move(width, height)


def ui_path() -> str:
        """This function return a address on ui file"""
        parser = cfg.ConfigParser()
        path = 'res/config.ini'
        parser.read(path)
        lang = parser['USER']['language']
        del parser, path
        return lang


def runner():
    try:
        os.mkdir('logs')
    except:
        pass
    if not os.path.exists('res'):
        logging.error('delete files;')
        sys.exit(0)


def theme_str() -> str:
    parser = cfg.ConfigParser()
    path = 'res/config.ini'
    parser.read(path)
    theme_s = parser['USER']['Theme']
    del parser, path
    return theme_s


def themeInstaller():
    global theme
    if theme != 'Normal':
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(theme))


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