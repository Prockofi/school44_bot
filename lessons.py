import asyncio
import datetime
from db import DataBase
from netschoolapi import NetSchoolAPI

class Marks:
    def __init__(self):
        self.lessons = DataBase('lessons')
    
    async def main(self, user_id, login, password, school, school_url):
        connect = NetSchoolAPI(school_url)
        await connect.login(login, password, school)
        get_data = await connect.diary(start=datetime.date(2023, 9, 1), end=datetime.date(2024, 5, 31))
        await connect.logout()

        get_data = str(get_data).split('Day')
        year = {}
        for get_day in get_data:
            day = []
            for el in get_day.split('Lesson('):
                if len(str(el)) > 10:
                    line = ''

                    index = el.find(', mark=')
                    if index != -1:
                        if (el[index+7:index+8] in ['1', '2', '3', '4', '5']) and (el[index+7:index+8] != ''):
                            line += el[index+7:index+8]
                        else:
                            line += '6'
                    else:
                        line = '6' + line

                    index = el.find('subject=')
                    if index != -1:
                        lesson = el[index+8:index+40].split("'")
                        line += ' ' + lesson[1]
                
                    index = el.find('day=datetime.date(')
                    if index != -1:
                        if ', ' == el[index+29:index+31]:
                            time = el[index+17:index+29]
                        elif ',' == el[index+30:index+31]:
                            time = el[index+17:index+30]
                        else:
                            time = el[index+17:index+31]
                    
                    day.append(line)
                if len(str(day)) > 10:
                    year[time] = day
        write_data = ''
        for day in year.keys():
            write_data += '$' + day + '#'.join(year.get(day))
        return str(write_data)

    def get_data(self, user_id, login, password, school, school_url):
        self.year = asyncio.run(self.main(user_id, login, password, school, school_url))
        read_data = self.lessons.get(user_id, {'lessons'})
        self.lessons.enter(user_id, {'lessons':self.year})
        if not read_data:
            read_data = ['None']
        return self.compare(self.filter(self.year).split('#'), self.filter(read_data[0]).split('#')), self.year

    def compare(self, new_data, old_data):
        new_mark, old_mark = [], []
        for el in new_data:
            if not (el in old_data):
                new_mark.append(el)
        for el in old_data:
            if not (el in new_data):
                old_mark.append(el)
        return new_mark, old_mark

    def filter(self, data):
        marks = ''
        for day in data.split('$'):
            if len(str(day)) > 10:
                time = day[day.index('('):day.index(')')+1]
                for mark in day[day.index(')')+1:].split('#'):
                    marks += '#' + mark + ' ' + time
        return marks

    def get_year(self, user_id):
        return self.lessons.get(user_id, {'lessons'})