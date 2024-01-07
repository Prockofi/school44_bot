#Функция get() принимает id, login, пароль, название школы, url-адрес школы
#Возращает два списка: добавленные оценки и убранные
from get_marks import get
import telebot, time

#Получаем токен бота из файла token
with open('token') as token:
    bot = telebot.TeleBot(token.read())

#Проходимся вечным циклом по файлу с Users
while True:
    #Url определён, только для Костромской области (нужно доработать)
    url = 'https://netschool.eduportal44.ru/'
    with open('users', 'r', encoding='utf-8') as file:
        data = file.read().split('\n')
    #Работаем через цикл с каждой записью, и проверяем, чтобы регистрация была завершена
    for line in data:
        if len(line.split('#')) == 4:
            user_id, login, password, name_school = line.split('#')
            #Получаем оценки, в случае ошибки возращаем пустые списки
            try:
                new, old = get(user_id, login, password, name_school, url)
            except:
                new, old = [], []
            new = '\n' + '\n'.join(new)
            old = '\n' + '\n'.join(old)
            if len(new) > 10:
                bot.send_message(user_id, f'Новые оценки:{new}')
            if len(old) > 10:
                bot.send_message(user_id, f'Эти оценки удалили:{old}')
    #1800 сек => 30 мин ожидания
    time.sleep(30)
        