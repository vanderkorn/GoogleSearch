# -*- coding=utf-8 -*-
'''
Created on 13.12.2011

@author: vanderkorn
'''
# Абстрактный класс поисковой машины
from abc import ABCMeta, abstractmethod, abstractproperty

class DataProvider:
    __metaclass__ = ABCMeta
    '''
   Абстактный класс работы с БД
    '''
    
    @abstractmethod
    def __init__(self,host,dbname,user,password):
        '''Инициализаровать соединение'''
        pass
    
    @abstractmethod
    def connect(self): 
        '''
        Открыть соединения
        '''
        pass  
    
    @abstractmethod
    def close(self): 
        '''
        Закрытие соединения
        '''
        pass  
       
    @abstractmethod
    def __del__(self): 
        '''
        При уничтожении объекта
        '''
        pass      