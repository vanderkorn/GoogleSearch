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
gMachine=GoogleMachine(50,'ABQIAAAAGDwMeqj4mf-zr79lESZrHhQKk7PsQRC9hShJoNd5vIdig4WNghRiNA-G53m6qeS7EnJCILGTIkSVLA',1000,'luxis.ru')
result=gMachine.parse('раскрутка продвижение сайтов', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2', '88.85.195.22')
print result 
