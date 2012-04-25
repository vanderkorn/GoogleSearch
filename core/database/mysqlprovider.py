#-------------------------------------------------------------------------------
# Created on 14.12.2011
# 
# @author: Van Der Korn
# @file: mysqlprovider.py
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-


from  dataprovider import DataProvider
import MySQLdb
import MySQLdb.cursors

class MysqlProvider(DataProvider):    
    '''Провайдер БД MySQL'''

    def __init__(self,host,dbname,user,password):
        '''констуктор'''
        self.host=host
        self.dbname=dbname
        self.user=user
        self.password=password
        MysqlProvider.connect(self)

    def connect(self):
        '''соеденимся с БД и получим курсор'''
        self.connection=MySQLdb.connect(host=self.host, user=self.user, passwd=self.password,db=self.dbname,cursorclass=MySQLdb.cursors.DictCursor)
        self.cursor = self.connection.cursor()
        
    def close(self):
        '''закроем соединение'''
        self.cursor.close()
        self.connection.close()

    def __del__(self):
        '''деструктор'''
        MysqlProvider.close(self)
        
    def set_charset(self,charset):
        '''Установить кодировку'''
        self.cursor.execute("SET CHARSET %s" %charset)
        
    @property    
    def rowcount(self):
        '''Количество строк в последнем запросе'''
        return MysqlProvider._getrowcount(self)
    
    def _getrowcount(self):
        '''Количество строк в последнем запросе'''
        return self.cursor.rowcount
      
