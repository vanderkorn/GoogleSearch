# -*- coding=utf-8 -*-
'''
Created on 13.12.2011

@author: vanderkorn
'''


import MySQLdb
import MySQLdb.cursors

class GoogleMysqlProvider:   
     
    '''Провайдер БД MySQL'''
    def __init__(self,host,dbname,user,password):
        '''констуктор'''
        self.host=host
        self.dbname=dbname
        self.user=user
        self.password=password
        GoogleMysqlProvider.connect(self)

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
        GoogleMysqlProvider.close(self)
        
    def set_charset(self,charset):
        '''Установить кодировку'''
        self.cursor.execute("SET CHARSET %s" %charset)
        
    @property    
    def rowcount(self):
        '''Количество строк в последнем запросе'''
        return GoogleMysqlProvider._getrowcount(self)
    
    def _getrowcount(self):
        '''Количество строк в последнем запросе'''
        return self.cursor.rowcount
        
    def getkeywords(self):
        '''получим ключевые слова'''
        sql = "SELECT key_words.id AS id,key_words.key_word AS key_word,sites.domain AS domain,cities.name AS name,cities.id AS city_id FROM key_words,sites,cities2yandexregionid,cities WHERE key_words.site_id=sites.id AND cities2yandexregionid.yandex_region_id=sites.region AND cities2yandexregionid.city_id=cities.id ORDER By domain"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def getuseragent(self):
        '''получим юзер-агента'''
        sql="SELECT name FROM useragents ORDER BY RAND() LIMIT 1"
        self.cursor.execute(sql)
        result=self.cursor.fetchall()
        return result[0]['name']
    
    def geiipfromcity(self,city_id):
        '''Получить произвольный ип-адрес по городу'''
        sql="SELECT ip FROM `ip_addresses` WHERE city_id=%s ORDER BY RAND() LIMIT 1" %city_id
        self.cursor.execute(sql)
        result=self.cursor.fetchall()
        if GoogleMysqlProvider._getrowcount(self)==0:#если нету ип-адресов по городу возбмем любой
            sql="SELECT ip FROM `ip_addresses` ORDER BY RAND() LIMIT 1"
            self.cursor.execute(sql)
            result=self.cursor.fetchall()
        return result[0]['ip']
    
    def insertposition(self,key_word_id,position,day,month,year):
        '''Вставить позицию google'''
        self.cursor.execute("SELECT * FROM google_positions WHERE key_word_id = '" + str(key_word_id) + "' AND day = '" + day + "' AND month = '" + month + "' AND year = '" + year + "'")
        if GoogleMysqlProvider._getrowcount(self)==0:
            self.cursor.execute("INSERT INTO google_positions SET key_word_id = '" + str(key_word_id) + "',position = '" + str(position) + "',day = '" + day + "',month = '" + month + "',year = '" + year + "'")
    
    def insertpositionforce(self,key_word_id,position,day,month,year):
        '''Вставить позицию google'''
        self.cursor.execute("SELECT * FROM google_positions WHERE key_word_id = '" + str(key_word_id) + "' AND day = '" + day + "' AND month = '" + month + "' AND year = '" + year + "'")
        if GoogleMysqlProvider._getrowcount(self)==0:
            GoogleMysqlProvider.insertposition(self,key_word_id,position,day,month,year)
        else:
            result=self.cursor.fetchall()
            id=result[0]['id']
            self.cursor.execute("UPDATE google_positions SET key_word_id = '" + str(key_word_id) + "',position = '" + str(position) + "',day = '" + day + "',month = '" + month + "',year = '" + year + "' WHERE id="+str(id))     
    
    def getkeywordsfromsite(self,site_id):
        '''получим ключевые слова'''
        sql = "SELECT key_words.id AS id,key_words.key_word AS key_word,sites.domain AS domain,cities.name AS name,cities.id AS city_id FROM key_words,sites,cities2yandexregionid,cities WHERE key_words.site_id=sites.id AND cities2yandexregionid.yandex_region_id=sites.region AND cities2yandexregionid.city_id=cities.id AND sites.id=%s ORDER By domain" % site_id
        self.cursor.execute(sql)
        return self.cursor.fetchall()

