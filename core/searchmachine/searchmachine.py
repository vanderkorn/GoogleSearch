# -*- coding=utf-8 -*-
'''
Created on 06.12.2011

@author: Ivan Kornilov

'''

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
    
