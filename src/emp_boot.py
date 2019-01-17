import json
import os

import machine
from emp_utils import config_path, list_item, rainbow, selection, Config

options = {
    'enable_wifi': True,
    'emp_ide': {
        'enable': True,
        'wireless': False
    }
}


class Boot(Config):

    def __init__(self, profile='boot.config', options=options):
        super().__init__(profile=profile, options=options)

    def start(self):

        configs = self.read_profile()
        if configs['enable_wifi']:
            import emp_wifi

        if configs['emp_ide']['enable']:
            global ide
            if configs['emp_ide']['wireless']:

                foo = __import__('emp_ide', globals(), locals())
                ide = foo.web_ide
            else:
                foo = __import__('emp_ide', globals(), locals())
                ide = foo.ide

    def set_mode(self):
        print(list_item(0, 'Normal', 'Normal start'))
        print(list_item(1, 'Turn on WiFi',
                        'Automatically connect to WiFi when booting.'))
        print(list_item(2, 'EMP-IDE-SerialPort',
                        'This mode is for developers. You can use EMP-IDE via serialport connection.'))
        print(list_item(3, 'EMP-IDE-WebSocket',
                        'In this mode, You can use EMP-IDE via websocket connection.'))

        mode = selection('Please input your choice: ', 3)
        boot_options = None
        if mode == 0:
            boot_options = [False, False, False]
            print(rainbow('Boot mode: Normal', color='green'))
        elif mode == 1:
            boot_options = [True, False, False]
            print(rainbow('Boot mode: Turn on WiFi', color='green'))

        elif mode == 2:
            boot_options = [False, True, False]
            print(rainbow('Boot mode: EMP-IDE-SerialPort', color='green'))

        elif mode == 3:
            boot_options = [False, True, True]
            print(rainbow('Boot mode: EMP-IDE-WebSocket', color='green'))

        config = {
            'enable_wifi': boot_options[0],
            'emp_ide': {
                'enable': boot_options[1],
                'wireless': boot_options[2]
            }
        }

        self.update_profile(config)

        with open('/boot.py', 'w') as f:
            f.write('import emp_boot')


try:
    import esp
    esp.osdebug(None)
except ImportError:
    pass

boot = Boot()
boot.start()
