#-------------------------------------------------------------------------------
# Created on 14.12.2011
# 
# @author: Van Der Korn
# @file: yandexmachine.py
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-


from  searchmachine import SearchMachine
import urllib
import urllib2
import json
import re
import time

#Library for work with curl
import pycurl
import StringIO
import os
import sys,traceback
from xml.parsers.expat import ExpatError
#Library for work with xml
from xml.dom.minidom import parse, parseString

class YandexMachine(SearchMachine):    
    '''  Search engine Yandex'''
    def __init__(self,deep,timeout,host,user,key):
        '''    Constructor        '''
        self.__name='Yandex' #name engine
        self.__deep=deep #deep search
        self.__host=host#name site
        self.__timeout=timeout #timeout internal request
        self.__countresults=50#count results on page
        self.__url='http://xmlsearch.yandex.ru/xmlsearch?%s'
        self.__queryXML = "<?xml version='1.0' encoding='utf-8'?><request><query>%s</query><page>%s</page><groupings><groupby attr='d' mode='deep' groups-on-page='%s' docs-in-group='1'/></groupings></request>"
        self.__user=user
        self.__key=key
        self.__param = {}
        if (len(self.__user)!=0):
            self.__param["user"]=str(self.__user)
        if (len(self.__key)!=0):
            self.__param["key"]=str(self.__key)    
       
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

    def parse(self, keyword,useragent,region):
        '''Parse output Google'''
        
        num_pages= self.__deep/self.__countresults#count pages
        #Generate XML request for transmission xml.yandex.ru

        #Create the parameter list transferred to page xml.yandex
        self.__param["lr"]=str(region)
        
        for i in range(0,num_pages):
            fullurl = YandexMachine.url(self) #prepare url
            queryXML=self.__queryXML % (keyword,str(i),str(self.__countresults))
            
            #header = {"User-Agent":useragent}# added a browser name
            xml_doc = self.get_url(fullurl,queryXML)
            try:
                xml_doc = parseString(xml_doc)
            except ExpatError:
                raise
            #Check error in case of access to
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
        
    # Function for receiving pages with transmission of POST of request
    def get_url(self,url,query,proxy=""):
        #initialize objects
        data = StringIO.StringIO()
        curl = pycurl.Curl()
        #set up pycurl
        curl.setopt(pycurl.FOLLOWLOCATION, 1)
        curl.setopt(pycurl.CONNECTTIMEOUT, 30)
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.WRITEFUNCTION, data.write)
        curl.setopt(pycurl.POST, 1)
        curl.setopt(pycurl.POSTFIELDS, query)
        #If connect with proxy
        timeout_down=800
        timeout_up=1200
        if len(proxy)>0:
            curl.setopt(pycurl.PROXY,proxy)
        #Try run request
        curl.perform()

        #close connection
        curl.close()
        #return the received page
        return data.getvalue()

    def checkhost(self,xml_doc):
        '''Check selected URl on compliance to a host'''
        position = 0
        found = 0
        CurrentLenXML=len(xml_doc.getElementsByTagName("domain"))
        scan_deep=self.__countresults
        if CurrentLenXML >= 0 and CurrentLenXML < scan_deep:
            scan_deep=CurrentLenXML
    
        if scan_deep > 0:
            for cur_node in xrange(0,scan_deep):
                #Increase a line item on 1
                position+=1
                #Take the current domain fromxml
                #print cur_node
                #print len(xml_doc.getElementsByTagName("domain"))
                #if (xml_doc.getElementsByTagName("domain")[cur_node]):
                cur_domain = xml_doc.getElementsByTagName("domain")[cur_node].childNodes[0].data
                #print cur_domain
                #If the domain with www. to we cut down it to without www., as such addresses are stored in basis, differently we leave it as is
                if cur_domain[0:4] == "www.":
                    cur_domain = cur_domain[4:len(cur_domain)]
                #If the current domain matches with required
                if cur_domain==self.__host:
                    found = 1
                    break
                #Increase the counter for taking a next domain
                cur_node+=1
    
        #If coincidence to the domain wasn't, the line item is equal 0
        if found == 0:
            position = -1
    
        # Destroy a variable with xml
        xml_doc.unlink()
        return position       
        
