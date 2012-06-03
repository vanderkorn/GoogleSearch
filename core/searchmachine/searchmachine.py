# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------------
# Created on 14.12.2011
# 
# @author: Van Der Korn
# @file: searchmachine.py
#-------------------------------------------------------------------------------



# Абстрактный класс поисковой машины
from abc import ABCMeta, abstractmethod, abstractproperty

class SearchMachine:
    __metaclass__ = ABCMeta
    '''
  Abstract class search engine
    '''

    @abstractproperty
    def name(self):
        ''' Name engine'''
        pass
    
    @abstractproperty
    def host(self):
        '''
        URL site
        '''
        pass
    
    @abstractproperty
    def deep(self):
        '''
        Deep search
        '''
        pass
    
    @abstractmethod
    def parse(self,keyword): 
        '''
        Parse output
        '''
        pass      
    
