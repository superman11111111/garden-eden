from random import randint
import bot
import json
import os
import sys
from config import *


class Command:
    def __init__(self, name, exec, args=()):
        self.name = name
        self.exec = exec
        self.args = args

def get_config(config_file=CONFIG_FILE):
    if not config_file:
        global CONFIG_FILE
        config_file = CONFIG_FILE
    if os.path.isfile(config_file):
        config = json.loads(open(config_file, 'r').read())
    else:
        open(config_file, 'w+').close()
        config = {}
    return config

def save_config(new_config, config_file=CONFIG_FILE):
    if not config_file:
        global CONFIG_FILE
        config_file = CONFIG_FILE
    open(config_file, 'w').write(json.dumps(new_config))


def change_config(config_path, value, save=False):
    config = get_config()
    tmp_dict = config
    for p in config_path[:-1]:
        tmp_dict = tmp_dict[p]
    tmp_dict[config_path[-1]] = value
    if save:
        print('Modified config saved to', CONFIG_FILE)
        save_config(config)

def _w_obj(obj, max_depth, path=[]):
    _obj_type = type(obj)
    if _obj_type is list:
        _obj_length = len(obj)
        _keys = range(_obj_length)
        _values = obj
    elif _obj_type is dict:
        _obj_length = len(obj)
        _keys = obj.keys()
        _values = obj.values()
    else:
        print(f'Current Value {_obj_type}:', obj)
        _inp = input(f'New Value:   ')
        if _obj_type is bool:
            if _inp == 'True' or _inp == 'true' or _inp == '1':
                _new_value = True
            if _inp == 'False' or _inp == 'false' or _inp == '0':
                _new_value = False
        else:
            _new_value = _obj_type(_inp)
        change_config(path, _new_value, save=True)
        return 0
    _keys = list(_keys)
    _values = list(_values)
    for i in range(_obj_length):
        _k = _keys[i]
        _v = _values[i]
        print(f'{i}:', _k, type(_v))
    print()
    _i = int(input(f'Choose [from 0 to {_obj_length-1}]: ') or 0)
    _val = _values[_i]
    _type = type(_val)
    path.append(_keys[_i])
    print('->'.join([str(x) for x in path]))
    return _w_obj(obj[_keys[_i]], max_depth, path)


def set_config_file():
    global CONFIG_FILE
    _l = len(open(CONFIG_FILE, 'r').read())
    print('Current config file:', CONFIG_FILE, f'length: {_l}')
    _files = [x for x in os.listdir('.') if os.path.isfile(os.path.join('.', x))]
    for i in range(len(_files)):
        print(i, _files[i])
    while True:
        try:
            _sel = int(input(f'Choose [from 0 to {len(_files)-1}]: '))
            if _sel > -1:
                if _sel <= len(_files):
                    break
                else:
                    print('Number', _sel, 'is too big!')
            else:
                print('Only non negative numbers!')
        except ValueError:
            print('Invalid input, Try again!')
    CONFIG_FILE = _files[_sel]
    try:
        config = get_config(CONFIG_FILE)
    except json.decoder.JSONDecodeError:
        print(CONFIG_FILE, 'does not contain valid config data!')
        return 1
    with open('config.py', 'r+') as f:
        _r = f.read().splitlines()
        for i in range(len(_r)):
            if 'CONFIG_FILE' in _r[i]:
                _r[i] = f'CONFIG_FILE = \"{CONFIG_FILE}\"'
        f.seek(0)
        f.write('\n'.join(_r))
        f.truncate()
        f.close()
    print('New config file is now', CONFIG_FILE)
    return 0
    

def edit_config():
    return _w_obj(get_config(), 2)


def clear_screen():
    print(chr(27) + "[2J")


def clear_line():
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")
    # print("\033[A                             \033[A")


def clear_lines(n=1):
    for i in range(n):
        clear_line()


def get_drop_time(bot_config):
    config = get_config()
    change_config(['bot_config', 'sneakers', 0, 'drop_time'], bot.get_drop_date(bot_config), save=True)
    return 0 


def get_options():
    config = get_config()
    bot_config = config['bot_config']
    options = [
        Command('RUN', bot.get_sneaker, (bot_config, )),
        Command('WAIT_FOR_DROP', bot.wait_for_drop, (bot_config, )),
        Command('CONFIG_FILE', set_config_file),
        Command('EDIT_CONFIG', edit_config),
        Command('GET_DROP_TIME', get_drop_time, (bot_config, )),
    ]
    return options

def init():
    options = get_options()
    _ll = max(len(c.name) for c in options)
    _out = ''
    for i in range(len(options)):
        _cmd = options[i]
        _out += f'{i}: {_cmd.name} {(_ll*2-len(_cmd.name))*" "}({_cmd.exec.__name__})\n'
    print()
    _try = 0
    while True:
        _try += 1
        try:
            _sel = int(input(_out + f'\nChoose: [0-{len(options)-1}]: '))
        except ValueError:
            print('Invalid value, Try again!')
            continue
        clear_lines(_try*(len(options)+3))
        if _sel > -1 and _sel < len(options): 
            for i in range(len(options)):
                if i == _sel:
                    _cmd = options[i]
                    print('Executing', _cmd.exec.__name__, 'with', len(_cmd.args), 'arguments')
                    r = _cmd.exec(*_cmd.args)
                    print(_cmd.exec.__name__, 'returned', r)
                    _try = 0
                    if (r == 0):
                        break


            
init()