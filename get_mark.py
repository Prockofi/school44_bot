import asyncio, datetime
from netschoolapi import NetSchoolAPI as ns

global result

#Функция получения данных из дневника
#На вход принимает логин, пароль, имя школы и url-адресс школы
#Возращает данные в виде списка - ['5 Инфор (2023, 12, 28)']
async def main(login, password, school, school_url):
    global result
    result = ''
    connect = ns(school_url)
    await connect.login(login, password, school)

    #Получение данных в период с 1 сентября по 31 мая
    data = await connect.diary(start=datetime.date(2023, 9, 1), end=datetime.date(2024, 5, 31))
    data = str(data).split(' subject=')

    #Конвертируем полученную строку в список
    for line in data:
        for el in line.split():
            if ('mark=' in el) and (len(el) == 7):
                result += el[5:6] + ' '
                result += str(line.split())[3:8] + ' '
                result += str(line.split())[str(line.split()).index('day=datetime.date(') + 17:str(line.split()).index('day=datetime.date(') + 37] + '#'
    await connect.logout()
    result = result.split('#')

#Основная функция выполнения, которую необходимо вызвать из бота
def get(user_id, login, password, school, school_url):
    asyncio.run(main(login, password, school, school_url))
    #Получаем сохраннёные в файле оценки
    with open('marks', 'r', encoding="utf-8") as file:
        read = file.read().split('\n')
    for line in read:
        if user_id in line:
            read_data = line[9:].split('#')
            break
        else:
            read_data = ["None"]

    #Сравниваем новые и старые оценки
    new_mark, old_mark = compare(result, read_data)

    #Сохраняем новые оценки в виде строки, которая начинается с user_id
    #Каждая оценка записываеться через #
    with open('marks', 'w', encoding="utf-8") as file:
        s = ''
        for el in result:
            s += el + '#'
        s = user_id + '#' + s
        read.remove(s)
        read.append(s)
        save_data = ''
        for el in read:
            save_data += el + '\n'
        save_data = save_data.replace('\n\n', '\n')
        file.write(save_data)
    return new_mark, old_mark

#Сравниваем оценки записанные в файл с актуальными оценками
def compare(new_data, old_data):
    new_mark, old_mark = [], []
    for i in new_data:
        if not (i in old_data):
            new_mark.append(i)
    for i in old_data:
        if not (i in new_data):
            old_mark.append(i)
    return new_mark, old_mark
