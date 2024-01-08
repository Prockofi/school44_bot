class DataBase:
    def __init__(self, name, args=False):
        self.name = name
        if args:
            with open(f'{name}.db', 'w', encoding='utf-8') as db:
                db.write('id | ' + ' | '.join(args))
                self.names = args
        else:
            with open(f'{self.name}.db', 'r', encoding='utf-8') as db:
                data = db.read().split('\n')
                self.names = data[0].split(' | ')

    def place(self, row_id, args=[]):
        with open(f'{self.name}.db', 'r', encoding='utf-8') as db:
            data = db.read().split('\n')
        for row in data:
            data_row = row.split(' | ')
            if data_row[0] == str(row_id):
                new_row = data_row.copy()
                for el in args:
                    if el in self.names:
                        new_row[self.names.index(el)] = str(args.get(el))
                data.remove(' | '.join(data_row))
                data.append(' | '.join(new_row))
                with open(f'{self.name}.db', 'w', encoding='utf-8') as db:
                    db.write('\n'.join(data))
                break
        else:
            new_row = [f'{str(row_id)}'] + ['None' for i in range(len(self.names)-1)]
            for el in args:
                if el in self.names:
                    new_row[self.names.index(el)] = str(args.get(el))
            data.append(' | '.join(new_row))
            with open(f'{self.name}.db', 'w', encoding='utf-8') as db:
                db.write('\n'.join(data))

    def get(self, row_id, args={}):
        with open(f'{self.name}.db', 'r', encoding='utf-8') as db:
            data = db.read().split('\n')
        for row in data:
            data_row = row.split(' | ')
            if args == {}:
                if data_row[0] == str(row_id):
                    return data_row
            else:
                if data_row[0] == str(row_id):
                    request = []
                    for el in args:
                        request.append(data_row[self.names.index(el)+1])
                    return request

    def not_empty(self, row_id):
        with open(f'{self.name}.db', 'r', encoding='utf-8') as db:
            data = db.read().split('\n')
        for row in data:
            data_row = row.split(' | ')
            if data_row[0] == str(row_id):
                request = []
                for el in data_row:
                    if el != 'None':
                        request.append(el)
                return request
        return False

    def remove(self, row_id):
        with open(f'{self.name}.db', 'r', encoding='utf-8') as db:
            data = db.read().split('\n')
        for row in data:
            data_row = row.split(' | ')
            if data_row[0] == str(row_id):
                data.remove(' | '.join(data_row))
                with open(f'{self.name}.db', 'w', encoding='utf-8') as db:
                    db.write('\n'.join(data))
                break

    def all(self):
        with open(f'{self.name}.db', 'r', encoding='utf-8') as db:
            data = db.read().split('\n')
        return data[1:]