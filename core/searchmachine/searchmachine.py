#-------------------------------------------------------------------------------
# Created on 14.12.2011
# 
# @author: Van Der Korn
# @file: searchmachine.py
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-


# Абстрактный класс поисковой машины
from abc import ABCMeta, abstractmethod, abstractproperty

class SearchMachine:
    __metaclass__ = ABCMeta
    '''
   Абстактный класс поисковой машины
    '''

    @abstractproperty
    def name(self):
        ''' Имя машины'''
        pass
    
    @abstractproperty
    def host(self):
        '''
        Адрес сайта
        '''
        pass
    
    @abstractproperty
    def deep(self):
        '''
        Глубина поиска  
        '''
        pass
    
    @abstractmethod
    def parse(self,keyword): 
        '''
        Парсинг выдачи
        '''
        pass      
    
