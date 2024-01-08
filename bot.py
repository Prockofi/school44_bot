import telebot
from db import DataBase
from telebot import types
from get_marks import get
from schools_names import search

#Получаем токен бота из файла token
with open('token') as token:
    bot = telebot.TeleBot(token.read())

#Обращение к базе данных
db = DataBase('users')

#Отслеживаем команду /start
@bot.message_handler(commands=["start"])
def repeat_all_messages(mess):
    #Определяем кнопки [Помощь] [Дневник]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Помощь"), types.KeyboardButton("Дневник"))
    #Проходимся по всему списку пользователей и определяем зарегистрирован ли он
    length = db.not_empty(mess.chat.id)
    if length:
        if len(length) < 4:
            bot.send_message(mess.chat.id, 'Продолжайте регистрацию', reply_markup=markup)
        if len(length) == 4:
            bot.send_message(mess.chat.id, 'Вы авторизованы!', reply_markup=markup)
    else:
        bot.send_message(mess.chat.id, 'Для начала работы, необходимо авторизоваться', reply_markup=markup)
        db.place(mess.chat.id)
        bot.send_message(mess.chat.id, 'Введите логин')

#Отслеживаем команду /help
@bot.message_handler(commands=["help"])
def repeat_all_messages(mess):
    bot.send_message(mess.chat.id, 'Доступные команды')

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
        #Проходим по всем пользователям узнаём, колличество сохранённых данных и от этого выбираем этап регистрации
        length = db.not_empty(mess.chat.id)
        if length:
            length = len(length)
            if length == 1:
                db.place(mess.chat.id, {'Логин':mess.text})
                bot.send_message(mess.chat.id, 'Пароль')
            elif length == 2:
                db.place(mess.chat.id, {'Пароль':mess.text})
                bot.send_message(mess.chat.id, 'Название школы')
            elif length == 3:
                send = bot.send_message(mess.chat.id, 'Выполняется подключение...')
                try:
                    name_school = search(mess.text, url)
                    db.place(mess.chat.id, {'Название школы':name_school})
                    user_id, login, password, name_school = db.not_empty(mess.chat.id)
                    get(user_id, login, password, name_school, url)
                    bot.edit_message_text('Подключение установленно! Теперь вы будете получать оповещения об изменениях в вашем дневнике', mess.chat.id, send.id)
                except:
                    db.remove(mess.chat.id)
                    bot.edit_message_text('Подключение не удалось! Попробуйте заново /start', mess.chat.id, send.id)
            else:
                bot.send_message(mess.chat.id, 'Вы авторизованы! Напишите /help для получения информации')
        else:
            bot.send_message(mess.chat.id, 'Для начала работы, необходимо авторизоваться - /start')

#Начинаем работу бота
bot.infinity_polling()