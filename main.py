import telebot, time
from get_mark import get

bot = telebot.TeleBot('TOKEN')

#Отслеживаем команду /start
@bot.message_handler(content_types=["command"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, 'Чтобы бот присылал вам уведомления о изменениях в электронном дневнике, необходимо отправить ему сообщение с логином, паролем, название школы через запятую')

#Берём данные для авторизации и получаем оценки
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    login, password, name_school = message.text.split(',')
    if get(str(message.chat.id), login, password, name_school, 'https://netschool.eduportal44.ru/'):
        bot.send_message(message.chat.id, 'Получилось!')
        time.sleep(1800)
        while True:
            try:
                #Получаем добавленные и удалённые оценки, и выводим их
                new, old = get(str(message.chat.id), login, password, name_school, 'https://netschool.eduportal44.ru/')
                time.sleep(1800)
                str1, str2 = '', ''
                for el in new:
                    str1 += '\n' + str(el)[:-2].replace("',", ' ').replace("'", '')
                for el in old:
                    str2 += '\n' + str(el)[:-2].replace("',", ' ').replace("'", '')
                if len(str1) > 10:
                    bot.send_message(message.chat.id, f'Новые оценки:{str1}')
                if len(str2) > 10:
                    bot.send_message(message.chat.id, f'Эти оценки удалили:{str1}')
            except:
                time.sleep(60)
    else:
        bot.send_massage(massage.chat.id, 'Не удалось подключиться проверьтие данные (Особенно проверьте название школы)')
            
if __name__ == '__main__':
    bot.infinity_polling()