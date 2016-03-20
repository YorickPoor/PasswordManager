#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sqlite3
import logging
import os


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
