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

class GoogleMachine:    
    '''  Поисковая машина Google'''
    def __init__(self,deep,key,timeout,host):
        '''    Констурктор        '''
        self.__name='Google' #имя машины
        self.__deep=deep #глубина поиска
        self.__key=key #ключ google
        self.__host=host#адрес сайта
        self.__timeout=timeout #таймаут внутренних запросов
        self.__countresults=8#количество результатов на странице
        self.__url='http://ajax.googleapis.com/ajax/services/search/web?%s'
        self.__param = {
                        'v':'1.0',
                        'key':self.__key ,
                        'rsz':self.__countresults,
                        'hl':'ru',
                        'filter':'1',
                        'gl':'ru'
                        }

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
    
    def parse(self, keyword,useragent,ip):
        '''Парсинг выдачи'''
        self.__param["q"]=keyword.strip("\r\n")
        self.__param["userip"]=ip# пользовательский ип
        num_pages= self.__deep/self.__countresults#количество страниц
        
        for i in range(1,num_pages+1):
            start=(i-1)*8  
            self.__param["start"]=start
            fullurl = GoogleMachine.url(self) #подготовили url
        
            header = {"User-Agent":useragent}#подставили имя браузера
            page_request = urllib2.Request(url=fullurl, headers=header)#подготовили запрос
    
            results = urllib2.urlopen(url=page_request)#выполнили запрос
            encoding='utf-8'
            resultsjson = json.loads(results.read(),encoding)
            data = resultsjson['responseData']
            hits = data['results']
            
            j=1
            for h in hits: 
                if GoogleMachine.checkhost(self,h['url']):
                    return start+j
                j+=1
            time.sleep(self.__timeout/1000)
        return -1
        
#    def unquote_u(self,source):
#        result = source
#        if '%u' in result:
#                result = result.replace('%u','\\u').decode('unicode_escape')
#        result = urllib.unquote(result)
#        return result
    
    def checkhost(self,source):
        '''Проверить выбранный URl на соответвие хосту'''
        strpat='(.*)%s(.*)'%(self.__host)
        patternhost=re.compile(strpat)
        if patternhost.search(source)!=None:
            return True
        return False
            
        