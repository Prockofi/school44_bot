import telebot, time
from telebot import types
from get_marks import get
from replace_data import rep, append, rm
from schools_name import search

with open('token') as file:
    token = file.read()
bot = telebot.TeleBot(token)

#Отслеживаем команду /start
@bot.message_handler(commands=["start"])
def repeat_all_messages(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Помощь")
    btn2 = types.KeyboardButton("Дневник")
    markup.add(btn1, btn2)
    append(str(message.chat.id), 'users')
    bot.send_message(message.chat.id, 'Для начала работы, необходимо авторизоваться', reply_markup=markup)
    with open('users', 'r', encoding='utf-8') as file:
        data = file.read().split('\n')
    for line in data:
        if (str(message.chat.id) in line) and (len(line.split('#')) > 3):
            bot.send_message(message.chat.id, 'Вы авторизованы! Напишите /help для получения информации')
            break
    else:
        bot.send_message(message.chat.id, 'Логин')
    
@bot.message_handler(commands=["help"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, 'Доступные команды')


#Берём данные для авторизации
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    if(message.text == "Помощь"):
        bot.send_message(message.chat.id, 'Доступные команды')
    elif (message.text == 'Дневник'):
        bot.send_message(message.chat.id, 'Оценки')
    else:
        with open('users', 'r', encoding='utf-8') as file:
            data = file.read().split('\n')
        user = str(message.chat.id)
        for line in data:
            if user == line:
                line += '#' + message.text
                bot.send_message(message.chat.id, 'Пароль')
                break
            if (user in line) and (len(line.split('#')) == 2):
                line += '#' + message.text
                bot.send_message(message.chat.id, 'Название школы')
                break
            if (user in line) and (len(line.split('#')) == 3):
                send = bot.send_message(message.chat.id, 'Выполняется подключение...')
                try:
                    name_school = search(message.text, 'https://netschool.eduportal44.ru/')
                    line += '#' + name_school
                    rep(line, 'users')
                    user_id, login, password, name_school = line.split('#')
                    get(user_id, login, password, name_school, 'https://netschool.eduportal44.ru/')
                    bot.edit_message_text('Подключение установленно! Теперь вы будете получать оповещения об изменениях в вашем дневнике', message.chat.id, send.id)
                except:
                    rm(line, 'users')
                    bot.edit_message_text('Подключение не удалось! Попробуйте заново /start', message.chat.id, send.id)
                break
            if (user in line) and (len(line.split('#')) > 3):
                bot.send_message(message.chat.id, 'Вы авторизованы! Напишите /help для получения информации')
                break
        else:
            bot.send_message(message.chat.id, 'Для начала работы, необходимо авторизоваться - /start')
        rep(line, 'users')

bot.infinity_polling()