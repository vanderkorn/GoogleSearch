#-------------------------------------------------------------------------------
# Created on 14.12.2011
# 
# @author: Van Der Korn
# @file: siteyandexparse.py
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-


from core.searchmachine.yandexmachine import *
from core.database.yandexmysqlprovider import *
from core.logger.filelogger import *
from core.datetime.datehelper import *
#Бибилиотека для работы с
import datetime
import random
import sys,traceback
import optparse

log=FileLogger(filename="log_1ps.html")
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


connection=YandexMysqlProvider(host='localhost',dbname='seocalc_20100301',user='root',password='')
connection.set_charset(charset='utf8')

keywords=connection.getkeywordsfromsite(site_id)
count_keyword=connection.rowcount
log.writelog("Начало работы скрипта в " + DateHelper.get_time() + ".Количество обрабатоваемых слов " + str(count_keyword) + "</b></td></tr>")
log.writelog("<tr><td align=center>№</td><td>Время</td><td align=center>Домен</td><td align=center>Ключевик</td><td align=center>Позиция</td></tr>")


i=0
timeout_down=800 # таймаут в мс
timeout_up=1200 # таймаут в мс

sleep_i=100
timeout_down_interval=3000 # таймаут через несколько запросов
timeout_up_interval=6000 # таймаут через несколько запросов

timeout_down_error=6000 # таймаут по ошибке
timeout_up_error=9000 # таймаут по ошибке

current_year,current_month,current_day= DateHelper.get_date()
#for dict_keyword in keywords:
while i < count_keyword:
    try:
        try:
            dict_keyword=keywords[i]
            id,keyword,domain,region_id=dict_keyword["id"],dict_keyword["key_word"],dict_keyword["domain"],dict_keyword["region_id"]
            useragent=connection.getuseragent() #получим произвольный юзер-агент
            yaMachine=YandexMachine(50,1000,domain,'LaManshStrait','03.32599484:7b8e071b9f4c9b333d73304ea23f50ba')
            result=yaMachine.parse(keyword, useragent, region_id)
            print result
            log.writelog("<tr><td align=center>" + str(i+1) + "</td><td>"+DateHelper.get_time()+"</td><td align=center>" + str(domain) + "</td><td align=center>" + str(keyword) + "</td><td align=center>" + str(result) + "</td></tr>")
            connection.insertpositionforce(key_word_id=id, position=result, day=current_day, month=current_month, year=current_year)
            timeout=random.uniform(timeout_down,timeout_up)#произвольное вещественное число
            time.sleep(timeout/1000)#после запроса требуется подождать
        except:
            exc_type,exc_value,exc_trace=sys.exc_info();
            log.writelog("<tr><td colspan='5' align=center><b>")
            errorstr=traceback.print_exception(exc_type, exc_value, exc_trace, limit=2)
            log.writelog(errorstr)
            log.writelog("</b></td></tr>")
            log.writelog("<tr><td colspan='5' align=center><b>error:  index i="+str(i)+" </b></td></tr>")
            timeout=random.uniform(timeout_down_error,timeout_up_error)#произвольное вещественное число
            time.sleep(timeout/1000)#после запроса требуется подождать
    finally:
        if (i%sleep_i==0):
            timeout=random.uniform(timeout_down_interval,timeout_up_interval)#произвольное вещественное число
            time.sleep(timeout/1000)#после запроса требуется подождать
        i+=1
log.writelog("<tr><td colspan='5' align=center><b>Окончание работы скрипта в " + DateHelper.get_time() + ".Количество обработаных слов " +str(i)+ "</b></td></tr></table></body></html>")






