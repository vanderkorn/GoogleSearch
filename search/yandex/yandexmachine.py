# -*- coding=utf-8 -*-
'''
Created on 06.12.2011

@author: Ivan Kornilov
'''


import urllib
import urllib2
import json
import re
import time

#Библиотека для работы с curl
import pycurl
import StringIO
import os
import sys,traceback
from xml.parsers.expat import ExpatError
#Библиотека для работы с xml
from xml.dom.minidom import parse, parseString

class YandexMachine:    
    '''  Поисковая машина Yandex'''
    def __init__(self,deep,timeout,host,user,key):
        '''    Констурктор        '''
        self.__name='Yandex' #имя машины
        self.__deep=deep #глубина поиска
        self.__host=host#адрес сайта
        self.__timeout=timeout #таймаут внутренних запросов
        self.__countresults=50#количество результатов на странице
        self.__url='http://xmlsearch.yandex.ru:80/xmlsearch?%s'
        self.__queryXML = "<?xml version='1.0' encoding='utf-8'?><request><query>%s</query><page>%s</page><groupings><groupby attr='d' mode='deep' groups-on-page='%s' docs-in-group='1'/></groupings></request>"
        self.__user=user
        self.__key=key
        self.__param = {}
        if (len(self.__user)!=0):
            self.__param["user"]=str(self.__user)
        if (len(self.__key)!=0):
            self.__param["key"]=str(self.__key)    
       
    def name(self):
        '''Получить имя машины'''
        return self.__name
    
    def host(self):
        '''Получить имя сайта'''
        return  self.__host
    
    def url(self):
        '''Сгенерировать URL'''
        query = urllib.urlencode(self.__param,doseq=0)
        url = self.__url% (query) #подготовили url
        return  url

    def deep(self):
        '''Получить глубину поиска'''
        return self.__deep

    def parse(self, keyword,useragent,region):
        '''Парсинг выдачи'''
        
        num_pages= self.__deep/self.__countresults#количество страниц
        #Формируем XML запрос для передачи xml.yandex.ru

        #Создаем список параметров передаваемых страннице xml.yandex
        self.__param["lr"]=str(region)
        
        for i in range(0,num_pages):
            fullurl = YandexMachine.url(self) #подготовили url
            queryXML=self.__queryXML % (keyword,str(i),str(self.__countresults))
            
            #header = {"User-Agent":useragent}#подставили имя браузера
            xml_doc = self.get_url(fullurl,queryXML)
            try:
                xml_doc = parseString(xml_doc)
            except ExpatError:
                raise
            #Проверяем на ошибку при доступе к xml
            if xml_doc.getElementsByTagName("error"):
                xml_doc.unlink()
                xml_doc = self.get_url(fullurl,queryXML,"91.201.55.106:3128")
                try:
                    xml_doc = parseString(xml_doc)#comment
                except ExpatError:
                    pass
           
            position=YandexMachine.checkhost(self,xml_doc)
            if position!=-1:
                return position
            else:
                time.sleep(self.__timeout/1000)
        return -1
        
    #Функция для получения странниц с передачей POST запроса
    def get_url(self,url,query,proxy=""):
        #инициализируем обьекты
        data = StringIO.StringIO()
        curl = pycurl.Curl()
        #настраиваем pycurl
        curl.setopt(pycurl.FOLLOWLOCATION, 1)
        curl.setopt(pycurl.CONNECTTIMEOUT, 30)
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.WRITEFUNCTION, data.write)
        curl.setopt(pycurl.POST, 1)
        curl.setopt(pycurl.POSTFIELDS, query)
        #Если подключились с проксиком
        timeout_down=800
        timeout_up=1200
        if len(proxy)>0:
            curl.setopt(pycurl.PROXY,proxy)
        #пробуем выполнить запрос
        curl.perform()

        #закрываем соединение
        curl.close()
        #возвращаем полученную странницу
        return data.getvalue()

    def checkhost(self,xml_doc):
        '''Проверить выбранный URl на соответвие хосту'''
        position = 0
        found = 0
        CurrentLenXML=len(xml_doc.getElementsByTagName("domain"))
        scan_deep=self.__countresults
        if CurrentLenXML >= 0 and CurrentLenXML < scan_deep:
            scan_deep=CurrentLenXML
    
        if scan_deep > 0:
            for cur_node in xrange(0,scan_deep):
                #увеличиваем позицию на 1
                position+=1
                #Берем текущий домен из xml
                #print cur_node
                #print len(xml_doc.getElementsByTagName("domain"))
                #if (xml_doc.getElementsByTagName("domain")[cur_node]):
                cur_domain = xml_doc.getElementsByTagName("domain")[cur_node].childNodes[0].data
                #print cur_domain
                #Если домен с www. до урезаем его до без www. , т.к в базе храняться именно такие адреса , иначе оставляем его как есть
                if cur_domain[0:4] == "www.":
                    cur_domain = cur_domain[4:len(cur_domain)]
                #Если текущий домен совпадает с искомым,то ...
                if cur_domain==self.__host:
                    found = 1
                    break
                #Увеличиваем счетчик для взятия след. домена
                cur_node+=1
    
        #Если совпадений с доменом небыло,то позиция равна 0
        if found == 0:
            position = -1
    
        #Уничтожаем переменную с xml
        xml_doc.unlink()
        return position       
        