#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from Crypto.Cipher import AES
import hashlib
import logging
import os


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
            self.encrypt = True
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
            self.decrypt = True
            return True
        except Exception as e:
            logging.error('Eror on decrypting base;')
            logging.error('File size {};'.format(os.stat(last_addr)[6]))
            logging.error('Eror {};'.format(e.args))

        @property
        def encrypt():
            return self.encrypt
        @property
        def decrypt():
            return self.decrypt