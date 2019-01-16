import json
import os

import machine
from emp_utils import config_path, list_item, rainbow, selection, Config

options = {
    'enable_wifi': 0,
    'emp_ide': {
        'enable': 1,
        'wireless': 2
    }
}


class Boot(Config):

    def __init__(self, profile='boot.config', options=options):
        super().__init__(profile=profile, options=options)

    def start(self):

        configs = self.read_profile()
        if configs['enable_wifi']:
            from emp_wifi import Wifi
            Wifi.connect()
        if configs['emp_ide']['enable']:

            if configs['emp_ide']['wireless']:
                import emp_webrepl
                from emp_ide import web_ide as ide
            else:
                from emp_ide import ide

    def set_mode(self):
        print(list_item(0, 'Normal', 'Normal start'))
        print(list_item(1, 'Turn on WiFi',
                        'Automatically connect to WiFi when booting.'))
        print(list_item(2, 'EMP-IDE-SerialPort',
                        'This mode is for developers. You can use EMP-IDE via serialport connection.'))
        print(list_item(3, 'EMP-IDE-WebSocket',
                        'In this mode, You can use EMP-IDE via websocket connection.'))

        mode = selection('Please input your choice [0-3]: ', 3)
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


boot = Boot()


def main():
    try:
        import esp
        esp.osdebug(None)
    except ImportError:
        pass

    boot.start()


main()
