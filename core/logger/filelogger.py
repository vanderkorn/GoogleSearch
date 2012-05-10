#-------------------------------------------------------------------------------
# Created on 14.12.2011
# 
# @author: Van Der Korn
# @file: filelogger.py
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-

from  logger import Logger

class FileLogger(Logger):
    '''File Logger'''
    
    def __init__(self,filename):
        '''Initialization logger'''
        self.filename=filename
        FileLogger.open(self)
          
    def open(self):
        '''Open log'''
        self.f_log = open(self.filename,'w+')

    def close(self):
        '''Close log'''
        self.f_log.close()

    def writelog(self, text):
        '''Write log'''
        self.f_log.write("%s\n" % text)
        self.f_log.flush()

    def __del__(self):
        '''Destroy log'''
        FileLogger.close(self)

