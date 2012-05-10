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
    '''DataBase Provider MySQL'''

    def __init__(self,host,dbname,user,password):
        '''Constructor'''
        self.host=host
        self.dbname=dbname
        self.user=user
        self.password=password
        MysqlProvider.connect(self)

    def connect(self):
        '''Connect to DataBase and we receive the cursor'''
        self.connection=MySQLdb.connect(host=self.host, user=self.user, passwd=self.password,db=self.dbname,cursorclass=MySQLdb.cursors.DictCursor)
        self.cursor = self.connection.cursor()
        
    def close(self):
        '''Close connection'''
        self.cursor.close()
        self.connection.close()

    def __del__(self):
        '''Destructor'''
        MysqlProvider.close(self)
        
    def set_charset(self,charset):
        '''Set up encoding'''
        self.cursor.execute("SET CHARSET %s" %charset)
        
    @property    
    def rowcount(self):
        '''Count of lines in the last request'''
        return MysqlProvider._getrowcount(self)
    
    def _getrowcount(self):
        '''count of lines in the last request'''
        return self.cursor.rowcount
      
