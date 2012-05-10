#-------------------------------------------------------------------------------
# Created on 14.12.2011
# 
# @author: Van Der Korn
# @file: logger.py
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty

class Logger:
    __metaclass__ = ABCMeta
    '''
    Class Logger
    '''
    
    @abstractmethod
    def open(self): 
        '''
        Open log
        '''
        pass  
    
    @abstractmethod
    def close(self): 
        '''
        Close log
        '''
        pass  
    
    @abstractmethod
    def writelog(self,text): 
        '''
        Write in log
        '''
        pass  
    
    @abstractmethod
    def __del__(self): 
        '''
        Destroy log
        '''
        pass      
