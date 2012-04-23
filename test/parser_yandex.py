# -*- coding: utf-8 -*- #
import urllib
import re
import MySQLdb
import MySQLdb.cursors
import datetime
import time
import random
import StringIO
import pycurl
import os

#Функция для получения страничек
def get_url(url,cookie):
    #Определяем случайным образом проксик
	number_proxy = random.randint(0,4) + 1
	#Список прокси серверов
	proxy = ("87.118.125.187:9667","87.118.124.187:9667","87.118.91.73:9667","87.118.90.73:9667","87.118.86.206:9667","87.118.87.206:9667")
	#инициализируем обьекты
	data = StringIO.StringIO()
	curl = pycurl.Curl()
	#настраиваем pycurl
	curl.setopt(pycurl.FOLLOWLOCATION, 1)
	curl.setopt(pycurl.CONNECTTIMEOUT, 30)
	curl.setopt(pycurl.URL, url)
	curl.setopt(pycurl.WRITEFUNCTION, data.write)
	curl.setopt(pycurl.COOKIE, cookie)
	curl.setopt(pycurl.PROXY,proxy[number_proxy])
	#пробуем выполнить запрос
	try:
		curl.perform()
	except:
		date = datetime.datetime.now()
		to_log(" " + date.strftime("%d:%m:%Y %H:%M:%S") + ":Не могу соедениться через прокси,пробую еще раз<br>")
		get_url(url,cookie)
	#закрываем соединение
	curl.close()
	#возвращаем результат
	return data.getvalue()


#Функция для получения позиций сайта
def positions(id,key,site_id):
	global timestamp,i
	#Начальная странница для парсинга
	cur_str = 0
	#Максимальная странница для парсинга
	max_str = 5
	#Инициализация счетчика позиций
	position = 0
	#Флаг для сообщения найдено ли совпадение домена,по умолчанию false
	found = 0
	#SQL запрос к базе для получения имени домена и региона сайта
	cursor.execute("SELECT domain,region FROM sites WHERE id = " + str(site_id) )
	res_region = cursor.fetchall()
	#Получем регион текушего ключевика
	region = res_region[0]['region']
	print "region:" + str(region);
	#Получаем имя домена для ключевика
	site_domain = res_region[0]['domain']
	#Генерация печененок для отправки яндексу,что бы он понял какой регион нужен
	cookies = "Cookie_check=1; yandex_gid=" + str(region) + "; path=/; domain=.yandex.ru"
	#Цикл обработки ключевого слова, пока не привышен придел максимально обрабатываемой странницы или пока домен не найден
	while (cur_str<max_str and found!=1):
		#Создаем список параметров передаваемых страннице
		s = urllib.urlencode([("p",cur_str),("text",key),])
		#Формируем полный URL для затравки курла
		urls = "http://yandex.ru/yandsearch?%s" % s
		#Находим все ссылки соответствующие регулярному выражению
		domains = re.findall(r'.*<a tabindex="(.*?)" onmousedown="(.*?)" href="(.*?)" target="(.*?)">.', get_url(urls,cookies))
		#Цикл бежит по всем найденым доменам
		for id_key in range(0,len(domains)):
			#увеличиваем позицию на 1
			position+=1
			print "position:" + str(position)
			#Регуляркой выдераем название домена
			domain = re.match(r'http://(.*?)/',domains[id_key][2])
			domain = domain.group(1)
			#Если домен с www. до урезаем его до без www. , т.к в базе храняться именно такие адреса , иначе оставляем его как есть
			if domain[0:4] == "www.":
				cur_domain = domain[4:len(domain)]
			else:
				cur_domain = domain
            #если текущий домен совпадает с доменом из базы, то ставим флаг found = true и выходим из цикла
			if cur_domain==site_domain:
				found = 1
				break
		#Увеличиваем счетчик текущей странницы
		cur_str+=1
	#Если совпадений с доменом небыло,то позиция равна 0
	if found == 0:
		position = 0

	#Вносив в базу позицию ключевика,обновляем время апдейта кейворда и время обновления всего проекта
	cursor.execute("INSERT INTO positions SET key_word_id = '" + str(id) + "',position = '" + str(position) + "',timestamp = '" + str(timestamp) + "',site_id = '" + str(site_id) + "',day = '" + day + "',month = '" + month + "',year = '" + year + "'");
	cursor.execute("UPDATE sites SET last_update = '" + str(timestamp) + "' WHERE id = '" + str(site_id) + "'")
	cursor.execute("UPDATE key_words SET last_update = '" + str(timestamp) + "' WHERE id = '" + str(id) + "'")

	to_log("<tr><td align=center>" + str(i) + "</td><td align=center>" + str(site_domain) + "</td><td align=center>" + str(key) + "</td><td align=center>" + str(position) + "</td></tr>")


#Аналог mysql_num_rows из php возврашает количество выбраных результатов
def mysql_num_rows(sql):
	return int(cursor.execute(sql))

def to_log(text):
	global f_log
	f_log.write(text+"\n")
	f_log.flush()

#Переменные используеммые в скрипте
#Количество обработаных ключевых слова
i = 0
#Количество всех ключевых слов
count_keyword=0
#Файл куда будем писать логи
file_log = "log.html"
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
#открываем файл для записи
f_log = open(file_log,'w')
print "Файл '"+file_log+"' открыт для записи логов"
# Конектимся к базе
db = MySQLdb.connect(host="localhost", user="root", passwd="coofiesh",db="seocalc",cursorclass=MySQLdb.cursors.DictCursor)
#Создаем указатель
cursor = db.cursor()
#Для отладки вывода на экран
cursor.execute("SET CHARSET utf8")
#SQL запрос для получения количества необработанных слов за сегодня
#sql = "SELECT key_words.id AS id,key_words.key_word AS key_word,key_words.site_id AS site_id FROM key_words,sites WHERE key_words.site_id=sites.id AND sites.region != '213' AND key_words.last_update != '" + str(timestamp) + "'"
sql = "SELECT key_words.id AS id,key_words.key_word AS key_word,key_words.site_id AS site_id FROM key_words,sites WHERE key_words.site_id=sites.id AND key_words.last_update != '" + str(timestamp) + "'"
#Заносим в переменную количество ключевиков не в московском регионе и не обработах сегодня
count_keyword=mysql_num_rows(sql)
#Начинаем писать лог
to_log("<html><head><title>Log parser</title><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"></head><body><table width=100% border=1><tr><td colspan=4 align=center><b>")
to_log("Начало работы скрипта в " + date.strftime("%d:%m:%Y %H:%M:%S") + ".Количество обрабатоваемых слов " + str(count_keyword) + "</b></td></tr>")
to_log("<tr><td align=center>№</td><td align=center>Домен</td><td align=center>Ключевик</td><td align=center>Позиция</td></tr>")
#Если количество необработаных слов больше нуля то заходим в цикл
while i < count_keyword:
	#Берем очередную порцию ключевых слов.
	#cursor.execute("SELECT key_words.id AS id,key_words.key_word AS key_word,key_words.site_id AS site_id FROM key_words,sites WHERE key_words.site_id=sites.id AND sites.region != '213' AND key_words.last_update != '" + str(timestamp) + "'")
	cursor.execute("SELECT key_words.id AS id,key_words.key_word AS key_word,key_words.site_id AS site_id FROM key_words,sites WHERE key_words.site_id=sites.id AND key_words.last_update != '" + str(timestamp) + "'")
	#Получем наши значения
	result = cursor.fetchall()
	#Пока не кончится список ключевиков
	sql="SELECT id FROM positions WHERE key_word_id = '" + str(result[0]['id']) + "' AND timestamp = '" + str(timestamp) + "'"
	#Если ключевик уже седня сканировался,то пропускаем его
	if mysql_num_rows(sql) > 0:
		continue
	#print str(result[0]['id'])+str(result[0]['key_word'])+str(result[0]['site_id'])
	#тут надо написать функцию с потоками
	positions(result[0]['id'],result[0]['key_word'],result[0]['site_id'])
	db.commit()
	#Увеличиваем перменную на количество обработанных ключевиков
	i+=1
else:
	to_log("<tr><td colspan=4 align=center><b>На сегодня все слова были обработаны</b></td></tr>")
date = datetime.datetime.now()
to_log("<tr><td colspan=4 align=center><b>Окончание работы скрипта в " + date.strftime("%d:%m:%Y %H:%M:%S") + ".Количество обработаных слов " + str(i) + "</b></td></tr></table></body></html>")