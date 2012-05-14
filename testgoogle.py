#-------------------------------------------------------------------------------
# Created on 14.12.2011
# 
# @author: Van Der Korn
# @file: testgoogle.py
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-
'''
Created on 06.12.2011
@author: vanderkorn
'''
from core.searchmachine.googlemachine import *
gMachine=GoogleMachine(50,'fsdfsdfdsgfregreEnJCILGTIkSVLA',1000,'roop.com')
result=gMachine.parse('site home', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2', '81.35.165.122')
print result 
