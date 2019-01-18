import gc
import json
import os


class Config:

    def __init__(self, path='config', profile=None, options=None):
        self.path = path
        self.profile = profile
        self.options = options
        self._init_profile()

    def _init_profile(self):
        try:
            os.listdir(self.path)
        except OSError:
            os.mkdir(self.path)
        finally:
            assert type(self.profile) == str, 'Profile must be a string'
            if self.profile in os.listdir(self.path):
                pass
            else:
                with open('%s/%s' % (self.path, self.profile), 'w') as f:
                    f.write(json.dumps(self.options))

    def read_profile(self):
        with open('%s/%s' % (self.path, self.profile), 'r') as f:
            return json.loads(f.read())

    def update_profile(self, kwargs):
        profile = self.read_profile()
        for key, value in zip(kwargs.keys(), kwargs.values()):
            profile[key] = value

        with open('%s/%s' % (self.path, self.profile), 'w') as f:
            f.write(json.dumps(profile))


def is_folder(path):
    try:
        os.listdir(path)
        return True
    except:
        return False


def post_ip(ip):
    import urequests
    urequests.post('http://www.1zlab.com/ide/post/ip/?esp_ip=%s,' % ip)


def traverse(path):
    n = dict(name=path, children=[])
    for i in os.listdir(path):
        if is_folder(path + '/' + i):
            n['children'].append(traverse(path + '/' + i))
        else:
            n['children'].append(dict(name=path + '/' + i))
    return n


def config_path():
    try:
        return len(os.listdir('config'))
    except:
        os.mkdir('config')
    finally:
        return len(os.listdir('config'))


def webrepl_pass():
    try:
        with open('config/webrepl.pass', 'r') as f:

            return f.read() if len(f.read()) > 0 else '1zlab'
    except:
        with open('config/webrepl.pass', 'w') as f:
            f.write('1zlab')
        return '1zlab'


def rainbow(output, color=None):
    if color:
        if color == 'green':
            return '\033[1;32m%s\033[0m' % output
        if color == 'red':
            return '\033[1;31m%s\033[0m' % output
        if color == 'blue':
            return '\033[1;34m%s\033[0m' % output
    else:
        return output


def left_just(output, length=None):
    if length == None:
        length = len(output)
    return output + (length - len(output)) * ' '


def right_just(output, length):
    if length == None:
        length = len(output)
    return (length - len(output)) * ' ' + output


def list_item(index, title, subtile=None):

    # esp8266 don't support center
    index = '[%s]' % str(index)
    index = index + (8-len(index)) * ' '

    title = left_just(rainbow(title, color='green'))
    if subtile:
        subtile = '\n' + len(index) * ' ' + subtile
    else:
        subtile = ''
    return index + title + subtile


def selection(hint, range):

    index = input(rainbow('%s [0-%s] ' % (hint, range), color='blue'))
    if int(index) > range or int(index) < 0:
        print(rainbow('out of range!', color='red'))
        selection(hint, range)
    else:
        return int(index)


def set_boot_mode():
    print(list_item(0, 'Normal', 'Normal start'))
    print(list_item(1, 'Turn on WiFi',
                    'Automatically connect to WiFi when booting.'))
    print(list_item(2, 'EMP-IDE-SerialPort',
                    'This mode is for developers. You can use EMP-IDE via serialport connection.'))
    print(list_item(3, 'EMP-IDE-WebSocket',
                    'In this mode, You can use EMP-IDE via websocket connection.'))

    mode = selection('Please input your choice: ', 3)
    boot_scripts = None
    if mode == 0:
        boot_scripts = ''
        print(rainbow('Boot mode: Normal', color='green'))
    elif mode == 1:
        boot_scripts = 'import emp_wifi'
        print(rainbow('Boot mode: Turn on WiFi', color='green'))

    elif mode == 2:
        boot_scripts = 'from emp_ide import ide'
        print(rainbow('Boot mode: EMP-IDE-SerialPort', color='green'))

    elif mode == 3:
        boot_scripts = 'from emp_webide import ide'
        print(rainbow('Boot mode: EMP-IDE-WebSocket', color='green'))

    with open('/boot.py', 'w') as f:
        f.write(boot_scripts)

    reboot = input('Reboot right now? [y/n]\n')
    if reboot in ['', 'y', 'Y', 'yes', 'Yes', 'YES']:
        import machine
        machine.reset()


def mem_analyze(func):
    def wrapper(*args, **kwargs):
        memory_alloc = 'memory alloced: %s kb' % str(gc.mem_alloc() / 1024)
        memory_free = 'memory free: %s kb' % str(gc.mem_free() / 1024)
        gc.collect()
        memory_after_collect = 'after collect: %s kb available' % str(
            gc.mem_free() / 1024)
        print(rainbow(memory_alloc, color='red'))
        print(rainbow(memory_free, color='green'))
        print(rainbow(memory_after_collect, color='blue'))
        func(*args, **kwargs)
        memory_after_func_excute = 'after %s excuted: %s kb available' % (
            func.__name__, str(gc.mem_free() / 1024))
        print(rainbow(memory_after_func_excute, color='red'))

    return wrapper


def sync_time():
    import urequests
    from machine import RTC
    rtc = RTC()
    print('before sync: ', rtc.datetime())
    time = urequests.get('http://www.1zlab.com/api/get-time/').json()
    # print(time)
    rtc.init(tuple(time['rtc']))
    print('after sync: ', rtc.datetime())
