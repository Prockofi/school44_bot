import telebot, time
from get_marks import get

with open('token') as file:
    token = file.read()
bot = telebot.TeleBot(token)

#Отслеживаем команду /start
@bot.message_handler(commands=["start"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, 'Чтобы бот присылал вам уведомления об изменениях в электронном дневнике, необходимо отправить ему сообщение с логином, паролем, названием школы через запятую')

#Берём данные для авторизации
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    try:
        login, password, name_school = message.text.split(',')
        get(str(message.chat.id), login, password, name_school, 'https://netschool.eduportal44.ru/')
        line = str(message.chat.id) + ',' + login + ',' + password + ',' + name_school + ',' + 'https://netschool.eduportal44.ru/'
        with open('users', 'r', encoding='utf-8') as file:
            data = file.read().split('\n')
            print(file.read())
            if not (line in data):
                data.append(line)
            str1 = ''
            for line in data:
                str1 += '\n' + ''.join(line)
            str1 = str1.replace('\n\n', '\n')
        with open('users', 'w', encoding='utf-8') as file:
            file.write(str1)
        bot.send_message(message.chat.id, '🟢 Получилось!')
    except:
        bot.send_message(message.chat.id, '🔴 Не удалось! ')

bot.infinity_polling()