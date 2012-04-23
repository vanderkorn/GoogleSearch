# -*- coding=utf-8 -*-

'''
Created on 14.12.2011

@author: vanderkorn
'''

from abc import ABCMeta, abstractmethod, abstractproperty

class Logger:
    __metaclass__ = ABCMeta
    '''
    Класс журналирования
    '''
    
    @abstractmethod
    def open(self): 
        '''
        Открыть журнал
        '''
        pass  
    
    @abstractmethod
    def close(self): 
        '''
        Закрыть журнал
        '''
        pass  
    
    @abstractmethod
    def writelog(self,text): 
        '''
        Записать в журнал
        '''
        pass  
    
    @abstractmethod
    def __del__(self): 
        '''
         Уничтожить журнал
        '''
        pass      