#-------------------------------------------------------------------------------
# Created on 14.12.2011
# 
# @author: Van Der Korn
# @file: yandexmysqlprovider.py
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-


from  mysqlprovider import MysqlProvider
import MySQLdb
import MySQLdb.cursors

class YandexMysqlProvider(MysqlProvider):    
    '''DataBase Provider MySQL for Yandex'''
    
    def getkeywordsfromsite(self,site_id):
        '''Get keywords from site'''
        sql = "SELECT key_words.id AS id,key_words.key_word AS key_word,sites.domain AS domain,sites.region AS region_id FROM key_words,sites WHERE key_words.site_id=sites.id AND sites.id=%s ORDER By domain" % site_id
        self.cursor.execute(sql)
        return self.cursor.fetchall()  
    
    def insertpositionforce(self,key_word_id,position,day,month,year):
        '''Insert position yandex output (force)'''
        self.cursor.execute("SELECT * FROM positions WHERE key_word_id = '" + str(key_word_id) + "' AND position = '" + str(position) + "' AND day = '" + day + "' AND month = '" + month + "' AND year = '" + year + "'")
        if MysqlProvider._getrowcount(self)==0:
            self.cursor.execute("INSERT INTO positions SET key_word_id = '" + str(key_word_id) + "',position = '" + str(position) + "',day = '" + day + "',month = '" + month + "',year = '" + year + "'")
        else:
            result=self.cursor.fetchall()
            id=result[0]['id']
            self.cursor.execute("UPDATE positions SET key_word_id = '" + str(key_word_id) + "',position = '" + str(position) + "',day = '" + day + "',month = '" + month + "',year = '" + year + "' WHERE id="+id)     
    
    def getuseragent(self):
        '''Get User-Agent'''
        sql="SELECT name FROM useragents ORDER BY RAND() LIMIT 1"
        self.cursor.execute(sql)
        result=self.cursor.fetchall()
        return result[0]['name']
