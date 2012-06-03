#-------------------------------------------------------------------------------
# Created on 14.12.2011
# 
# @author: Van Der Korn
# @file: googlemachine.py
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-


from  searchmachine import SearchMachine
import urllib
import urllib2
import json
import re
import time

class GoogleMachine(SearchMachine):    
    '''  Search engine Google'''
    def __init__(self,deep,key,timeout,host):
        '''    Constructor        '''
        self.__name='Google' #name engine
        self.__deep=deep #deep search - max 64 items
        self.__key=key #keyword google
        self.__host=host#name site
        self.__timeout=timeout #timeout internal request
        self.__countresults=8#count results on page
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
        '''Get name engine'''
        return self.__name
    
    def host(self):
        '''Get name site'''
        return  self.__host
    
    def url(self):
        '''Generate URL'''
        query = urllib.urlencode(self.__param,doseq=0)
        url = self.__url% (query)
        return  url

    def deep(self):
        '''Get deep search'''
        return self.__deep
    
    def parse(self, keyword,useragent,ip):
        '''Parse output Google'''
        self.__param["q"]=keyword.strip("\r\n")
        self.__param["userip"]=ip# user IP
        num_pages= self.__deep/self.__countresults#count pages
        
        for i in range(1,num_pages+1):
            start=(i-1)*8  
            self.__param["start"]=start
            fullurl = GoogleMachine.url(self) #prepare url
        
            header = {"User-Agent":useragent}#added a browser name
            page_request = urllib2.Request(url=fullurl, headers=header)#prepare request
    
            results = urllib2.urlopen(url=page_request)#run request
            encoding='utf-8'
            resultsjson = json.loads(results.read(),encoding)
            data = resultsjson['responseData']
            
            try:
                hits = data['results']
            except:
                return -1

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
        '''To check selected URl on compliance to a host'''
        strpat='(.*)%s(.*)'%(self.__host)
        patternhost=re.compile(strpat)
        if patternhost.search(source)!=None:
            return True
        return False
            
        
