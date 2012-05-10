#-------------------------------------------------------------------------------
# Created on 14.12.2011
# 
# @author: Van Der Korn
# @file: sitegoogleparse.py
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-
from core.searchmachine.googlemachine import *
from core.database.googlemysqlprovider import *
from core.logger.filelogger import *
from core.datetime.datehelper import *
#Library with work
import datetime
import random
import sys,traceback
import optparse
log=FileLogger(filename="glog_1ps.html")

log.writelog("<html><head><title>Log parser</title><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"></head><body><table width=100% border=1><tr><td colspan='5' align=center><b>")


try:
    p=optparse.OptionParser()
    p.add_option("-s",action="store",dest="site_id")
    p.add_option("--siteidentificator",action="store",dest="site_id")
    
    opts,args=p.parse_args()
    #site_id=15
    site_id=opts.site_id
except:
    exc_type,exc_value,exc_trace=sys.exc_info();
    log.writelog("<tr><td colspan='5' align=center><b>")
    errorstr=traceback.print_exception(exc_type, exc_value, exc_trace, limit=2)
    log.writelog(errorstr)
    log.writelog("</b></td></tr>")

if site_id==None:
    log.writelog("site_id=None")
    raise SystemExit(1)


connection=GoogleMysqlProvider(host='localhost',dbname='seocalc_20100301',user='root',password='')
connection.set_charset(charset='utf8')

keywords=connection.getkeywordsfromsite(site_id)
count_keyword=connection.rowcount

log.writelog("Начало работы скрипта в " + DateHelper.get_time() + ".Количество обрабатоваемых слов " + str(count_keyword) + "</b></td></tr>")
log.writelog("<tr><td align=center>№</td><td>Время</td><td align=center>Домен</td><td align=center>Ключевик</td><td align=center>Позиция</td></tr>")

i=0
timeout_down=8000 # timeout in ms
timeout_up=12000 # timeout in ms

sleep_i=100
timeout_down_interval=30000 # timeout through some requests
timeout_up_interval=60000 # timeout through some requests

timeout_down_error=60000 # timeout for error
timeout_up_error=90000 # timeout for error

current_year,current_month,current_day= DateHelper.get_date()
#for dict_keyword in keywords:
while i < count_keyword:
    try:
        try:
            dict_keyword=keywords[i]
            id,keyword,domain,name,city_id=dict_keyword["id"],dict_keyword["key_word"],dict_keyword["domain"],dict_keyword["name"],dict_keyword["city_id"]
            useragent=connection.getuseragent() #get random user agent
            ip=connection.geiipfromcity(city_id) #get random IP from city
            gMachine=GoogleMachine(50,'ABQIAAAAGDwMeqj4mf-zr79lESZrHhQKk7PsQRC9hShJoNd5vIdig4WNghRiNA-G53m6qeS7EnJCILGTIkSVLA',1000,domain)
            result=gMachine.parse(keyword, useragent, ip)
            print result
            log.writelog("<tr><td align=center>" + str(i+1) + "</td><td>"+DateHelper.get_time()+"</td><td align=center>" + str(domain) + "</td><td align=center>" + str(keyword) + "</td><td align=center>" + str(result) + "</td></tr>")
            connection.insertpositionforce(key_word_id=id, position=result, day=current_day, month=current_month, year=current_year)
            timeout=random.uniform(timeout_down,timeout_up)#random real number
            time.sleep(timeout/1000)#after request it is required to wait
        except:
            exc_type,exc_value,exc_trace=sys.exc_info();
            log.writelog("<tr><td colspan='5' align=center><b>")
            errorstr=traceback.print_exception(exc_type, exc_value, exc_trace, limit=2)
            log.writelog(errorstr)
            log.writelog("</b></td></tr>")
            log.writelog("<tr><td colspan='5' align=center><b>error:  index i="+str(i)+" </b></td></tr>")
            timeout=random.uniform(timeout_down_error,timeout_up_error)#random real number
            time.sleep(timeout/1000)#after request it is required to wait
    finally:
        if (i%sleep_i==0):
            timeout=random.uniform(timeout_down_interval,timeout_up_interval)#random real number
            time.sleep(timeout/1000)#after request it is required to wait
        i+=1
log.writelog("<tr><td colspan='5' align=center><b>Окончание работы скрипта в " + DateHelper.get_time() + ".Количество обработаных слов " +str(i)+ "</b></td></tr></table></body></html>")





