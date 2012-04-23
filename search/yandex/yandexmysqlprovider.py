# -*- coding=utf-8 -*-
'''
Created on 13.12.2011

@author: vanderkorn
'''


import MySQLdb
import MySQLdb.cursors

class YandexMysqlProvider:    
    '''Провайдер БД MySQL'''
    def __init__(self,host,dbname,user,password):
        '''констуктор'''
        self.host=host
        self.dbname=dbname
        self.user=user
        self.password=password
        YandexMysqlProvider.connect(self)

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
        YandexMysqlProvider.close(self)
        
    def set_charset(self,charset):
        '''Установить кодировку'''
        self.cursor.execute("SET CHARSET %s" %charset)
        
    @property    
    def rowcount(self):
        '''Количество строк в последнем запросе'''
        return YandexMysqlProvider._getrowcount(self)
    
    def _getrowcount(self):
        '''Количество строк в последнем запросе'''
        return self.cursor.rowcount
    
    def getkeywordsfromsite(self,site_id):
        '''Полуить список ключевых слов для сайта'''
        sql = "SELECT key_words.id AS id,key_words.key_word AS key_word,sites.domain AS domain,sites.region AS region_id FROM key_words,sites WHERE key_words.site_id=sites.id AND sites.id=%s ORDER By domain" % site_id
        self.cursor.execute(sql)
        return self.cursor.fetchall()  
    
    def insertpositionforce(self,key_word_id,position,day,month,year):
        '''Вставить позицию yandex'''
        self.cursor.execute("SELECT * FROM positions WHERE key_word_id = '" + str(key_word_id) + "' AND position = '" + str(position) + "' AND day = '" + day + "' AND month = '" + month + "' AND year = '" + year + "'")
        if YandexMysqlProvider._getrowcount(self)==0:
            self.cursor.execute("INSERT INTO positions SET key_word_id = '" + str(key_word_id) + "',position = '" + str(position) + "',day = '" + day + "',month = '" + month + "',year = '" + year + "'")
        else:
            result=self.cursor.fetchall()
            id=result[0]['id']
            self.cursor.execute("UPDATE positions SET key_word_id = '" + str(key_word_id) + "',position = '" + str(position) + "',day = '" + day + "',month = '" + month + "',year = '" + year + "' WHERE id="+id)     
   
    def getuseragent(self):
        '''получим юзер-агента'''
        sql="SELECT name FROM useragents ORDER BY RAND() LIMIT 1"
        self.cursor.execute(sql)
        result=self.cursor.fetchall()
        return result[0]['name']