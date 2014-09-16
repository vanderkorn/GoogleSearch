#-------------------------------------------------------------------------------
# Created on 14.12.2011
# 
# @author: Van Der Korn
# @file: datehelper.py
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-
import datetime
import time
import os
class DateHelper(object):
     '''Helper class for working datetime'''
   
     def __init__(self):
        os.environ['TZ'] = "Europe/Moscow"
    
     @staticmethod
     def get_time():
        date = datetime.datetime.now()
        return date.strftime("%d:%m:%Y %H:%M:%S")
     @staticmethod
     def get_date():
        date = datetime.datetime.now()
        year = date.strftime("%Y")
        month = date.strftime("%m")
        day = date.strftime("%d")
        return (year,month,day)
