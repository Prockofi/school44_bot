import telebot
from data import Data
from telebot import types
from get_marks import get
from schools_names import search

#Получаем токен бота из файла token
with open('token') as token:
    bot = telebot.TeleBot(token.read())

#Отслеживаем команду /start
@bot.message_handler(commands=["start"])
def repeat_all_messages(message):
    #Определяем кнопки [Помощь] [Дневник]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Помощь"), types.KeyboardButton("Дневник"))
    #Проходимся по всему списку пользователей и определяем зарегистрирован ли он
    with open('users', 'r', encoding='utf-8') as file:
        data = file.read().split('\n')
    for line in data:
        if str(message.chat.id) in line:
            if len(line.split('#')) < 4:
                bot.send_message(message.chat.id, 'Продолжайте регистрацию', reply_markup=markup)
                break
            if len(line.split('#')) > 3:
                bot.send_message(message.chat.id, 'Вы авторизованы!', reply_markup=markup)
                break
    else:
        bot.send_message(message.chat.id, 'Для начала работы, необходимо авторизоваться', reply_markup=markup)
        Data.append(str(message.chat.id), 'users')
        bot.send_message(message.chat.id, 'Введите логин')

#Отслеживаем команду /help
@bot.message_handler(commands=["help"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, 'Доступные команды')

#Берём данные для авторизации
@bot.message_handler(content_types=["text"])
def repeat_all_messages(mess):
    if mess.text == 'Помощь':
        bot.send_message(mess.chat.id, 'Доступные команды')
    elif mess.text == 'Дневник':
        bot.send_message(mess.chat.id, 'Дневник')
    else:
        #Url определён, только для Костромской области (нужно доработать)
        url = 'https://netschool.eduportal44.ru/'
        with open('users', 'r', encoding='utf-8') as file:
            data = file.read().split('\n')
        #Проходим по всем пользователям узнаём, колличество сохранённых данных и от этого выбираем этап регистрации
        for line in data:
            length = len(line.split('#'))
            if str(mess.chat.id) in line:
                if length == 1:
                    line += '#' + mess.text
                    bot.send_message(mess.chat.id, 'Пароль')
                    break
                if length == 2:
                    line += '#' + mess.text
                    bot.send_message(mess.chat.id, 'Название школы')
                    break
                if length == 3:
                    send = bot.send_message(mess.chat.id, 'Выполняется подключение...')
                    try:
                        name_school = search(mess.text, url)
                        line += '#' + name_school
                        Data.replace(line, 'users')
                        user_id, login, password, name_school = line.split('#')
                        get(user_id, login, password, name_school, url)
                        bot.edit_message_text('Подключение установленно! Теперь вы будете получать оповещения об изменениях в вашем дневнике', mess.chat.id, send.id)
                    except:
                        data.remove(line, 'users')
                        bot.edit_message_text('Подключение не удалось! Попробуйте заново /start', mess.chat.id, send.id)
                    break
                if length > 3:
                    bot.send_message(mess.chat.id, 'Вы авторизованы! Напишите /help для получения информации')
                    break
        else:
            bot.send_message(mess.chat.id, 'Для начала работы, необходимо авторизоваться - /start')
        Data.replace(line, 'users')

#Начинаем работу бота
bot.infinity_polling()