from lessons import Marks
import telebot, time

#Получаем токен бота из файла token
with open('token') as token:
    bot = telebot.TeleBot(token.read())

#Обращение к базе данных
mk = Marks()

#Проходимся вечным циклом по файлу с Users
while True:
    #Url определён, только для Костромской области (нужно доработать)
    url = 'https://netschool.eduportal44.ru/'
    with open('users.db', 'r', encoding='utf-8') as file:
        data = file.read().split('\n')
    #Работаем через цикл с каждой записью, и проверяем, чтобы регистрация была завершена
    for line in data[1:]:
        if len(line.split(' | ')) == 4:
            user_id, login, password, name_school = line.split(' | ')
            #Получаем оценки, в случае ошибки возращаем пустые списки
            try:
                (new, old), year = mk.get_data(user_id, login, password, name_school, url)
            except:
                new, old = '', ''
            for i in range(len(new)):
                if '6 ' in new[i]:
                    new[i] = new[i].replace('6 ', '')
            new = '\n' + '\n'.join(new)
            for i in range(len(old)):
                if '6 ' in new[i]:
                    old[i] = old[i].replace('6 ', '')
            old = '\n' + '\n'.join(old)
            if len(new) > 10:
                bot.send_message(user_id, f'Новые оценки:{new}')
            if len(old) > 10:
                bot.send_message(user_id, f'Эти оценки удалили:{old}')
    #1800 сек => 30 мин ожидания
    time.sleep(900)
        