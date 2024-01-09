import telebot
from db import DataBase
from telebot import types
from lessons import Marks
from schools_names import search
from datetime import datetime
import asyncio

#Получаем токен бота из файла token
with open('token') as token:
    bot = telebot.TeleBot(token.read())

#Обращение к базе данных
db = DataBase('users')
mk = Marks()

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
        db.enter(mess.chat.id, {'':''})
        bot.send_message(mess.chat.id, 'Введите логин')

#Отслеживаем команду /help
@bot.message_handler(commands=["help"])
def repeat_all_messages(mess):
    bot.send_message(mess.chat.id, 'Доступные команды')

#Берём данные для авторизации
@bot.message_handler(content_types=["text"])
def repeat_all_messages(mess):
    #Url определён, только для Костромской области (нужно доработать)
    url = 'https://netschool.eduportal44.ru/'
    if mess.text == 'Помощь':
        bot.send_message(mess.chat.id, 'Нужно доработать')
    elif mess.text == 'Дневник':
        #Составляем строку сегодняшней даты
        time = '(' + str(datetime.now().year) + ', ' + str(datetime.now().month) + ', ' + str(datetime.now().day) + ')'
        year = mk.get_year(mess.chat.id)[0]
        for day in year.split('$'):
            if len(day) > 10:
                timecorrect = day[day.index('('):day.index(')')+1]
                day = day[day.index(')')+1:]
                if timecorrect == time:
                    diary = []
                    for line in day.split('#'):
                        diary.append(line.replace('6 ', ''))
                    diary = '\n'.join(diary)
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data=f'{time}<'), types.InlineKeyboardButton(text="Назад", callback_data=f'{time}<'))
                    bot.send_message(mess.chat.id, f"📗 Дневник на {time[1:-1]}\n{diary}", reply_markup=keyboard)
                else:
                    diary = []
                    for line in day.split('#'):
                        diary.append(line.replace('6 ', ''))
                    diary = '\n'.join(diary)
                    send_time = timecorrect
        else:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data=f'{send_time}<'), types.InlineKeyboardButton(text="Вперёд", callback_data=f'{send_time}>'))
            bot.send_message(mess.chat.id, f"📗 Дневник на {send_time[1:-1]}\n{diary}", reply_markup=keyboard)
    else:
        #Проходим по всем пользователям узнаём, колличество сохранённых данных и от этого выбираем этап регистрации
        length = db.not_empty(mess.chat.id)
        if length:
            length = len(length)
            if length == 1:
                db.enter(mess.chat.id, {'Логин':mess.text})
                bot.send_message(mess.chat.id, 'Пароль')
            elif length == 2:
                db.enter(mess.chat.id, {'Пароль':mess.text})
                bot.send_message(mess.chat.id, 'Название школы')
            elif length == 3:
                send = bot.send_message(mess.chat.id, 'Выполняется подключение...')
                try:
                    name_school = search(mess.text, url)
                    db.enter(mess.chat.id, {'Название школы':name_school})
                    user_id, login, password, name_school = db.not_empty(mess.chat.id)
                    mk.get_data(user_id, login, password, name_school, url)
                    bot.edit_message_text('Подключение установленно! Теперь вы будете получать оповещения об изменениях в вашем дневнике', mess.chat.id, send.id)
                except:
                    db.remove(mess.chat.id)
                    bot.edit_message_text('Подключение не удалось! Попробуйте заново /start', mess.chat.id, send.id)
            else:
                bot.send_message(mess.chat.id, 'Вы авторизованы! Напишите /help для получения информации')
        else:
            bot.send_message(mess.chat.id, 'Для начала работы, необходимо авторизоваться - /start')

@bot.callback_query_handler(func=lambda c: '<' in c.data)
def process_callback_button1(callback_query: types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    time = callback_query.data[:-1]
    year = mk.get_year(callback_query.message.chat.id)[0]
    n = ''
    for day in year.split('$'):
        if len(day) > 10:
            timecorrect = day[day.index('('):day.index(')')+1]
            day = day[day.index(')')+1:]
            if timecorrect == time:
                diary = []
                for line in day.split('#'):
                    diary.append(line.replace('6 ', ''))
                diary = '\n'.join(diary)
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data=f'{n}<'), types.InlineKeyboardButton(text="Вперёд", callback_data=f'{n}>'))
                bot.edit_message_text(f"📗 Дневник за {n[1:-1]}\n{diary}", reply_markup=keyboard, chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
                break
            n = timecorrect

@bot.callback_query_handler(func=lambda c: '>' in c.data)
def process_callback_button1(callback_query: types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    time = callback_query.data[:-1]
    year = mk.get_year(callback_query.message.chat.id)[0]
    n = ''
    for day in year.split('$'):
        if len(day) > 10:
            timecorrect = day[day.index('('):day.index(')')+1]
            day = day[day.index(')')+1:]
            if n == time:
                diary = []
                for line in day.split('#'):
                    diary.append(line.replace('6 ', ''))
                diary = '\n'.join(diary)
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data=f'{timecorrect}<'), types.InlineKeyboardButton(text="Вперёд", callback_data=f'{timecorrect}>'))
                bot.edit_message_text(f"📗 Дневник за {timecorrect[1:-1]}\n{diary}", reply_markup=keyboard, chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
                break
            n = timecorrect

#Начинаем работу бота
bot.infinity_polling()