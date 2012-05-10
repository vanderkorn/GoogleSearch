#-------------------------------------------------------------------------------
# Created on 14.12.2011
# 
# @author: Van Der Korn
# @file: dataprovider.py
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-

# Abstract class 
from abc import ABCMeta, abstractmethod, abstractproperty

class DataProvider:
    __metaclass__ = ABCMeta
    '''
   Abstract class for operation with a DataBase
    '''
    
    @abstractmethod
    def __init__(self,host,dbname,user,password):
        '''Initialization connection'''
        pass
    
    @abstractmethod
    def connect(self): 
        '''
        Open connection
        '''
        pass  
    
    @abstractmethod
    def close(self): 
        '''
        Close connection
        '''
        pass  
       
    @abstractmethod
    def __del__(self): 
        '''
        Remove object
        '''
        pass      
