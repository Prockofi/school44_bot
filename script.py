from get_marks import get
#Функция get() принимает id, login, пароль, название школы, url-адрес школы
#Возращает два списка: добавленные оценки и убранные

import time
import telebot
with open('token') as file:
    token = file.read()
bot = telebot.TeleBot(token)

#Проходимся вечным циклом по файлу с Users
while True:
    with open('users', 'r', encoding='utf-8') as file:
        data = file.read().split('\n')
    #Работтаем через цикл с каждой записью
    maxlen = max([len(x) for x in data])
    if maxlen > 10:
        for line in data:
            if line != '':
                user_id, login, password, name_school, url_school = line.split(',')
                #Получаем оценки, в случае ошибки возращаем пустые списки
                try:
                    new, old = get(user_id, login, password, name_school, url_school)
                except:
                    new, old = [[], []]
                str1, str2 = '', ''
                for el in new:
                    str1 += '\n' + str(el)[:-2].replace("',", ' ').replace("'", '')
                for el in old:
                    str2 += '\n' + str(el)[:-2].replace("',", ' ').replace("'", '')
                if len(str1) > 10:
                    bot.send_message(user_id, f'Новые оценки:{str1}')
                if len(str2) > 10:
                    bot.send_message(user_id, f'Эти оценки удалили:{str2}')
    #1800 сек => 30 мин ожидания
    time.sleep(30)
        