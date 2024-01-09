class DataBase:
    def __init__(self, name, fields=None):
        with open(f'{name}.db', 'r+', encoding='utf-8') as db:
            if fields:
                db.write('id | ' + ' | '.join(fields))
                self.headers = fields
            else:
                self.headers = (db.read().split('\n'))[0].split(' | ')
            self.name = name

    def enter(self, post_id, fields):
        with open(f'{self.name}.db', 'r', encoding='utf-8') as db:
            data = db.read().split('\n')
            for post in data:
                post_data = post.split(' | ')
                if post_data[0] == str(post_id):
                    new_post_data = post_data.copy()
                    for field in fields.keys():
                        if field in self.headers:
                            new_post_data[self.headers.index(field)] = str(fields.get(field))
                    data.remove(' | '.join(post_data))
                    data.append(' | '.join(new_post_data))
                    break
            else:
                new_post_data = [str(post_id)] + ['None' for i in range(len(self.headers)-1)]
                for field in fields.keys():
                    if field in self.headers:
                        new_post_data[self.headers.index(field)] = str(fields.get(field))
                data.append(' | '.join(new_post_data))
        with open(f'{self.name}.db', 'w', encoding='utf-8') as db:
            db.write('\n'.join(data))

    def remove(self, post_id):
        with open(f'{self.name}.db', 'r', encoding='utf-8') as db:
            data = db.read().split('\n')
            for post in data:
                post_data = post.split(' | ')
                if post_data[0] == str(post_id):
                    data.remove(' | '.join(post_data))
                    break
        with open(f'{self.name}.db', 'w', encoding='utf-8') as db:
            db.write('\n'.join(data))
    
    def get(self, post_id, fields=None):
        with open(f'{self.name}.db', 'r', encoding='utf-8') as db:
            data = db.read().split('\n')
        for post in data:
            post_data = post.split(' | ')
            if post_data[0] == str(post_id):
                if fields:
                    request = []
                    for field in fields:
                        request.append(post_data[self.headers.index(field)])
                    return request
                else:
                    return post_data

    def not_empty(self, post_id):
        with open(f'{self.name}.db', 'r', encoding='utf-8') as db:
            data = db.read().split('\n')
        for post in data:
            post_data = post.split(' | ')
            if post_data[0] == str(post_id):
                request = []
                for field in post_data:
                    if field != 'None':
                        request.append(field)
                return request
        return False