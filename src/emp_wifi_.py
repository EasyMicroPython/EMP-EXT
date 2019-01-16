import json

# import network
from emp_utils import Config, config_path, list_item, rainbow, selection

_options = {
    'default': {
        'essid': '',
    },
    'records': {
        'ChinaNet-Q5uk': '0921608677'
    }

}


class EMPWifi(Config):
    def __init__(self, profile='emp_wifi.json', options=_options):
        super().__init__(profile=profile, options=options)
        # self._wifi = network.WLAN(network.STA_IF)

    def get_records(self):
        profile = self.read_profile()
        return profile['records']

    def is_in_records(self, essid):
        return essid in self.get_records().keys()

    def get_default(self):
        # config = self.read_config()
        # return config.get('default') if config else ()
        return self.read_profile()['default']

    def set_default(self, essid=None):
        if essid is None:
            records = [i for i in self.get_records().keys()]
            for index, item in enumerate(records):
                print(list_item(index, item))

            option = selection(
                'Please select an option as default wifi connection [0-%s]' % str(
                    len(records.keys()) - 1), len(records.keys()) - 1)

            default = {'default': {'essid': records[option]}}
            self.update_profile(default)
        else:
            default = {'default': {'essid': essid}}
            self.update_profile(default)

    def del_record(self, essid=None):
        if essid is None:
            records = self.get_records()
            essids = [i for i in records.keys()]
            for index, item in enumerate(essids):
                print(list_item(index, item))

            option = selection(
                'Please select an option to delete [0-%s]' % str(
                    len(records.keys()) - 1), len(records.keys()) - 1)

            essid = essids[option]
            records.pop(essid)
            records = {'records': records}
            self.update_profile(records)
        elif self.is_in_records(essid):
            records.pop(essid)
            records = {'records': records}
            self.update_profile(records)

        else:
            print(rainbow('The record was not found', color='red'))

    def add_record(self, essid, passwd):
        records = self.get_records()
        if essid in records.keys():
            if passwd == records[essid]:
                pass
            else:
                n = len([0 for i in records.keys() if essid in i])
                new_record = '%s#%s' % (essid, n) if n != 0 else essid
                records[new_record] = passwd

        else:
            records[essid] = passwd

        records = {'records': records}
        self.update_profile(records)

    def scan(self):
        def _list_wifi(index, essid, dbm):
            _index = ('[%s]' % str(index)).center(8).lstrip()
            _essid = rainbow(essid + (40 - len(essid)) * ' ', color='red')
            _dbm = rainbow(dbm.center(10).lstrip(), color='blue')
            print('{0} {1} {2} dBm'.format(_index, _essid, _dbm))

        networks = []
        for i in self._wifi.scan():
            # string decode may raise error
            try:
                nw = dict(essid=i[0].decode(), dbm=str(i[3]))
            except:
                nw = dict(essid=i[0], dbm=str(i[3]))
            finally:
                networks.append(nw)
        # networks = [dict(essid=i[0].decode(),dbm=str(i[3])) for i in self._wifi.scan()]

        for i, item in enumerate(networks):
            _list_wifi(i, item['essid'], item['dbm'])

        return networks

    def auto_connect(self):
        pass

    def connect(self, essid, passwd):
        self._wifi.active(True)
        self._wifi.connect(essid, passwd)
        import time

        for i in range(300):
            if self._wifi.isconnected():
                break
            time.sleep_ms(100)

        if not self._wifi.isconnected():
            self._wifi.active(False)
            print(
                rainbow(
                    'wifi connection error, please reconnect',
                    color='red'))
            return False

        else:
            self._essid = essid
            self.ifconfig()
            if not Wifi.is_in_records(essid):
                Wifi.add_record(essid, passwd)

            return True

    def disconnect(self):
        self._wifi.active(False)

    def ifconfig(self):
        info = self._wifi.ifconfig()
        print(rainbow('You are connected to %s' % self._essid))
        print(rainbow('IP: ' + info[0], color='red'))
        print(rainbow('Netmask: ' + info[1], color='green'))
        print(rainbow('Gateway: ' + info[2], color='blue'))
        return info, self._essid


if __name__ == '__main__':
    wifi = EMPWifi()
    print(wifi.get_records())
    wifi.del_record()
