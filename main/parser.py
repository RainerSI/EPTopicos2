from decimal import Decimal
from os import listdir

def read_directory(dir, path=''):
    instance = {}
    for file in listdir(path + dir):
        g = {'states': [], 'action': {}, 'cost': [], 'initialstate': '', 'goalstate': ''}
        with open(path + dir + file) as f:
            tag = None
            action = None
            for line in f:
                data = str(line.strip())
                if data == '':
                    continue
                if 'Grid:' in data:
                    break
                else:
                    if not tag:
                        if 'action' in data:
                            info = data.split(' ')
                            tag = info[0]
                            action = info[1]
                        else:
                            tag = data
                    else:
                        if data == 'end{}'.format(tag):
                            tag = None
                            action = None
                        elif tag == 'action':
                            info = data.split(' ')[:3]
                            from_state = str(info[0])
                            g[tag][action] = g[tag].get(action, {})
                            g[tag][action][from_state] = g[tag][action].get(from_state, [])
                            g[tag][action][from_state].append((info[1], Decimal(info[2])))
                        elif tag == 'states':
                            g[tag] = [s.strip() for s in data.split(',')]
                        elif tag in ['initialstate', 'goalstate']:
                            g[tag] = data
                        elif tag == 'cost':
                            if '0.500' in data:
                                print('cost')
        instance[file] = g
    return instance
