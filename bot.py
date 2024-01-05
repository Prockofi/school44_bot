import telebot, time
from get_marks import get
from replace_data import rep, append, rm

with open('token') as file:
    token = file.read()
bot = telebot.TeleBot(token)

#Отслеживаем команду /start
@bot.message_handler(commands=["start"])
def repeat_all_messages(message):
    append(str(message.chat.id), 'users')
    bot.send_message(message.chat.id, 'Для начала работы, необходимо авторизоваться')
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
    bot.send_message(message.chat.id, 'Список доступных действий:')


#Берём данные для авторизации
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
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
            line += '#' + message.text
            rep(line, 'users')
            bot.send_message(message.chat.id, 'Выполняется подключение...')
            user_id, login, password, name_school = line.split('#')
            try:
                get(user_id, login, password, name_school, 'https://netschool.eduportal44.ru/')
                bot.send_message(message.chat.id, 'Подключение установленно! Теперь вы будете получать оповещения об изменениях в вашем дневнике')
            except:
                rm(line, 'users')
                bot.send_message(message.chat.id, 'Подключение не удалось! Попробуйте заново /start')
            break
        if (user in line) and (len(line.split('#')) > 3):
            bot.send_message(message.chat.id, 'Вы авторизованы! Напишите /help для получения информации')
            break
    else:
        bot.send_message(message.chat.id, 'Для начала работы, необходимо авторизоваться - /start')
    rep(line, 'users')

bot.infinity_polling()