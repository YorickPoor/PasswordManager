#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import hashlib


class Hasher():
    def hasMd5(self, filename):
        """
        ===================
        calculating md5 hash of file
        ===================
        расчитывает md5 хеш
        ===================
        :param filename : absolute addr of file
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