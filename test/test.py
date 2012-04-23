# -*- coding: utf-8 -*- #
####################################################################
################  Parser xml.yandex v0.2 by [SF]DarkAngel    #######
####################################################################
######Подключаемые библиотеки######
import StringIO
#Библиотека для работы с curl
import pycurl
#Чет нужное ))))))
import urllib
#Библиотека для работы с БД MySQL
import MySQLdb
import MySQLdb.cursors
#Бибилиотека для работы с
import datetime
import random
import time
#Библиотека для работы с xml
from xml.dom.minidom import parse, parseString
#Библиотека для работы с датой
import os
import sys,traceback
from xml.parsers.expat import ExpatError

############################Глобальные переменные используемые в скрипте######################################
#Файл куда писать логи
file_log = "/home/u8742/u8742.netangels.ru/www/xml.html"
#Количество обработаных ключевых слова
i = 0
#Количество всех ключевых слов
count_keyword=0
#Рабоча через проксик (0 - нет,1 - прокси)
proxy_work=0
###############################################################################################################

############################Функции используемые в скрипте######################################
#Функция для записи в текстовый файл
def to_log(text):
	global f_log
	f_log.write(text+"\n")
	f_log.flush()

#Функция возвращает текущее время в формате ("%d:%m:%Y %H:%M:%S")
def get_time():
	date = datetime.datetime.now()
	return date.strftime("%d:%m:%Y %H:%M:%S")

#Аналог mysql_num_rows из php возврашает количество выбраных результатов
def mysql_num_rows(sql):
	return int(cursor.execute(sql))

#Функция для получения странниц с передачей POST запроса
def get_url(url,query,proxy=""):
 	#инициализируем обьекты
	data = StringIO.StringIO()
	curl = pycurl.Curl()
	#настраиваем pycurl
	curl.setopt(pycurl.FOLLOWLOCATION, 1)
	curl.setopt(pycurl.CONNECTTIMEOUT, 30)
	curl.setopt(pycurl.URL, url)
	curl.setopt(pycurl.WRITEFUNCTION, data.write)
	curl.setopt(pycurl.POST, 1)
	curl.setopt(pycurl.POSTFIELDS, query)
	#Если подключились с проксиком
	timeout_down=800
	timeout_up=1200
	if len(proxy)>0:
		curl.setopt(pycurl.PROXY,proxy)
	#пробуем выполнить запрос
	try:
		curl.perform()
	except:
		exc_type,exc_value,exc_trace=sys.exc_info()
		to_log("<tr><td colspan='5' align=center><b>")
		traceback.print_exception(exc_type, exc_value, exc_trace, limit=2, file=f_log)
		to_log(get_time() + ":Не могу соедениться<br>")
		timeout=random.uniform(timeout_down,timeout_up)
		#to_log(curl.getinfo(pycurl.HTTP_CODE))
		#to_log(curl.getinfo(pycurl.EFFECTIVE_URL))
		to_log("Подождем %s мс<br>" % timeout)
		time.sleep(timeout/1000)#после запроса требуется подождать
	#закрываем соединение
	curl.close()
	#возвращаем полученную странницу
	return data.getvalue()

#Функция для получения позиций сайта
def positions(id,key,site_id):
	
	global timestamp,i,proxy_work
	#xml странница которую выводим
	page = 0
	#количество сайтов на одной страннице xml ответа
	scan_deep = 50
	#Инициализация счетчика позиций
	position = 0
	#Флаг для сообщения найдено ли совпадение домена,по умолчанию false
	found = 0
	#SQL запрос к базе для получения имени домена и региона сайта
	cursor.execute("SELECT domain,region FROM sites WHERE id = " + str(site_id) )
	res_region = cursor.fetchall()
	#Получем регион текушего ключевика
	region = res_region[0]['region']
	#Получаем имя домена для ключевика
	site_domain = res_region[0]['domain']
    #Формируем XML запрос для передачи xml.yandex.ru
	queryXML = "<?xml version='1.0' encoding='utf-8'?><request><query>"+key+"</query><page>"+str(page)+"</page><groupings><groupby attr='d' mode='deep' groups-on-page='"+str(scan_deep)+"' docs-in-group='1'/></groupings></request>"
	#Создаем список параметров передаваемых страннице xml.yandex
	s = urllib.urlencode([("lr",str(region)),])
	#Формируем полный URL для затравки курла
	urls = "http://xmlsearch.yandex.ru:80/xmlsearch?%s" % s

    #Получаем данные от xml.yandex
	if proxy_work == 0:
		xml_doc = get_url(urls,queryXML)
	else:
		xml_doc = get_url(urls,queryXML,"91.201.55.106:3128")
	#Парсим их

	#to_log(xml_doc)
	xml_doc_old=xml_doc
	try:
		xml_doc = parseString(xml_doc)
	except ExpatError:
		to_log("<tr><td colspan='5' align=center><b>")
		to_log("Invalid xml:"+xml_doc)
		to_log("</b></td></tr>")
		raise
		
	#Проверяем на ошибку при доступе к xml
	if xml_doc.getElementsByTagName("error"):
		#Выдираем сообщение об ощибке
		#error=xml_doc.getElementsByTagName("error")[0].childNodes[0].data
		#Если оно о том что привышен лимит
		#print error.find("Limit exceed for user")
		to_log("Error:"+xml_doc_old)

		#if error.find("Limit exceed for") != -1:
			#Уничтожаем переменную с xml
		xml_doc.unlink()
		#Выставляем флаг работы через proxy
		#proxy_work = 1
		
		#Соединяемся через проксю
		#if proxy_work == 0:
		#	xml_doc = get_url(urls,queryXML)
		#else:
		to_log("Try from proxy...")
		xml_doc = get_url(urls,queryXML,"91.201.55.106:3128")
			
		proxy_work = 0 
		xml_doc_old=xml_doc
		#И отправляем на парсинг заново файл
		try:
			xml_doc = parseString(xml_doc)#comment
		except ExpatError:
			to_log("<tr><td colspan='5' align=center><b>")
			to_log("Invalid xml Proxy:"+xml_doc)
			to_log("</b></td></tr>")
			
		if xml_doc.getElementsByTagName("error"):
			to_log("Error Proxy:"+xml_doc_old)	
		else:
			to_log("Proxy good!")	
		#else:
		#	to_log(get_time() + ":Ошибка "+xml_doc.getElementsByTagName("error")[0].childNodes[0].data)


	###########################Тут происходит работа с xml парсингом############################

	CurrentLenXML=len(xml_doc.getElementsByTagName("domain"))

	if CurrentLenXML >= 0 and CurrentLenXML < scan_deep:
		scan_deep=CurrentLenXML

	if scan_deep > 0:
		for cur_node in xrange(0,scan_deep):
			#увеличиваем позицию на 1
			position+=1
			#Берем текущий домен из xml
			#print cur_node
			#print len(xml_doc.getElementsByTagName("domain"))
			#if (xml_doc.getElementsByTagName("domain")[cur_node]):
			cur_domain = xml_doc.getElementsByTagName("domain")[cur_node].childNodes[0].data
			#print cur_domain
			#Если домен с www. до урезаем его до без www. , т.к в базе храняться именно такие адреса , иначе оставляем его как есть
			if cur_domain[0:4] == "www.":
				cur_domain = cur_domain[4:len(cur_domain)]
			#Если текущий домен совпадает с искомым,то ...
			if cur_domain==site_domain:
				found = 1
				break
    		#Увеличиваем счетчик для взятия след. домена
			cur_node+=1

	#Если совпадений с доменом небыло,то позиция равна 0
	if found == 0:
		position = 0

    #Уничтожаем переменную с xml
	xml_doc.unlink()

	#Вносим в базу позицию ключевика,обновляем время апдейта кейворда и время обновления всего проекта
	cursor.execute("INSERT INTO positions SET key_word_id = '" + str(id) + "',position = '" + str(position) + "',timestamp = '" + str(timestamp) + "',site_id = '" + str(site_id) + "',day = '" + day + "',month = '" + month + "',year = '" + year + "'")
	cursor.execute("UPDATE sites SET last_update = '" + str(timestamp) + "' WHERE id = '" + str(site_id) + "'")
	cursor.execute("UPDATE key_words SET last_update = '" + str(timestamp) + "' WHERE id = '" + str(id) + "'")

	#Пишем в лог файл позицию ключевика
	to_log("<tr><td align=center>" + str(i) + "</td><td>"+get_time()+"</td><td align=center>" + str(site_domain) + "</td><td align=center>" + str(key) + "</td><td align=center>" + str(position) + "</td></tr>")
###############################################################################################################

###################################################################################################################
########################################      Тело основного скрипта           ####################################
###################################################################################################################
#Открываем файл для записи логов
f_log = open(file_log,'w+')
#Устанавливаем московское время
os.environ['TZ'] = "Europe/Moscow"
time.tzset()
#Получаем текушую дату
date = datetime.datetime.now()
year = date.strftime("%Y")
month = date.strftime("%m")
day = date.strftime("%d")
#Получаем таймстамп для текушего года,месяца и дня
timestamp = int(time.mktime((int(year),int(month),int(day),0,0,0,0,0,-1)))
# Конектимся к базе
db = MySQLdb.connect(host="localhost", user="root", passwd="coofiesh",db="seocalc_20100301",cursorclass=MySQLdb.cursors.DictCursor)
#Создаем указатель
cursor = db.cursor()
#UTF
cursor.execute("SET CHARSET utf8")
#SQL запрос для получения количества необработанных слов за сегодня
sql = "SELECT key_words.id AS id,key_words.key_word AS key_word,key_words.site_id AS site_id FROM key_words,sites WHERE key_words.site_id=sites.id AND key_words.last_update != '" + str(timestamp) + "'"
#Заносим в переменную количество ключевиков не в московском регионе и не обработах сегодня
count_keyword=mysql_num_rows(sql)
#Запишем в лог начало HTML каркаса и о том что скрипт начал свою работу.
to_log("<html><head><title>Log parser</title><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"></head><body><table width=100% border=1><tr><td colspan='5' align=center><b>")
to_log("Начало работы скрипта в " + get_time() + ".Количество обрабатоваемых слов " + str(count_keyword) + "</b></td></tr>")
to_log("<tr><td align=center>№</td><td>Время</td><td align=center>Домен</td><td align=center>Ключевик</td><td align=center>Позиция</td></tr>")
#Если количество необработаных слов больше нуля то заходим в цикл
while i < count_keyword:
	
	#Берем очередное ключевое слово.
	cursor.execute("SELECT key_words.id AS id, key_words.key_word AS key_word, key_words.site_id AS site_id FROM key_words, sites WHERE key_words.site_id=sites.id AND key_words.last_update != '" + str(timestamp) + "'")
	#Получаем значения из базы.
	result = cursor.fetchall()
	#Пытаемся выбрать текущий ключевик из уже проверенных
	try:
		try:
			sql="SELECT id FROM positions WHERE key_word_id = '" + str(result[0]['id']) + "' AND timestamp = '" + str(timestamp) + "'"
			#Если ключевик уже сканировался,то пропускаем его
			if mysql_num_rows(sql) > 0:
				continue
			#Если у нас все хорошо отправляем ключевик на парсинг
			#if int(result[0]['id']) != int(689):
			#print result[0]['id']
			positions(result[0]['id'],result[0]['key_word'],result[0]['site_id'])
			timeout_down=80
			timeout_up=120
			timeout=random.uniform(timeout_down,timeout_up)#произвольное вещественное число
			to_log("Подождем %s мс<br>" % timeout)
			time.sleep(timeout/1000)
		except:
			exc_type,exc_value,exc_trace=sys.exc_info();
			to_log("<tr><td colspan='5' align=center><b>")
			traceback.print_exception(exc_type, exc_value, exc_trace, limit=2, file=f_log)
			to_log("</b></td></tr>")
			to_log("<tr><td colspan='5' align=center><b>error:  index i="+str(i)+" count="+str(count_keyword)+"</b></td></tr>")
	finally:	
		#Подтверждаем изменения в базе данных
		db.commit()
		#Увеличиваем перменную на количество обработанных ключевиков
		i+=1
else:
	#Если нечего сканировать сообщим об этом пользователю
	to_log("<tr><td colspan='5' align=center><b>На сегодня все слова были обработаны</b></td></tr>")

#Пишем в лог файл конец HTML каркаса и о том что скрипт завершил свою работу
to_log("<tr><td colspan='5' align=center><b>Окончание работы скрипта в " + get_time() + ".Количество обработаных слов " + str(i) + "</b></td></tr></table></body></html>")
f_log.close()