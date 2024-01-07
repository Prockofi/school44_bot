def rep(new, file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = file.read().split('\n')
    for i in range(len(data)):
        if new[:9] == data[i][:9]:
            data[i] = new
    data = '\n'.join(data)
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(data)

def append(new, file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = file.read().split('\n')
    for i in range(len(data)):
        if new[:9] in data[i]:
            int('None')
    else:
        data.append(new)
    data = '\n'.join(data)
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(data)

def rm(old, file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = file.read().split('\n')
    for i in range(len(data)):
        if old == data[i]:
            data.remove(old)
    data = '\n'.join(data)
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(data)

def filt(data, d):
    for i in range(len(data)):
        try:
            data[i] = data[i].replace(',', '')
            data[i] = data[i].replace(')', '')
            data[i] = data[i].replace('(', '')
        except:
            print('Не получилось')
    return data