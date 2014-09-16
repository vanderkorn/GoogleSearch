#-------------------------------------------------------------------------------
# Created on 14.12.2011
# 
# @author: Van Der Korn
# @file: testyandex.py
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-
'''
Created on 06.12.2011
@author: vanderkorn
'''
from core.searchmachine.yandexmachine import *

yaMachine=YandexMachine(50,1000,'norbekovclub.ru','','')
try:
    result=yaMachine.parse('norbekov', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2', '54')
except:
    exc_type,exc_value,exc_trace=sys.exc_info();
    errorstr=traceback.print_exception(exc_type, exc_value, exc_trace, limit=2)
    print errorstr
print result 
