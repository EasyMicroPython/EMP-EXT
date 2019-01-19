import json

import network
from emp_utils import Config, list_item, rainbow, selection

options = {
    'default': {
        'essid': '',
    },
    'records': {
        'example_essid': 'example_passwd'
    }
}


class WiFi(Config):
    def __init__(self, profile='emp_wifi.json', options=options):
        super().__init__(profile=profile, options=options)
        self._wifi = network.WLAN(network.STA_IF)
        self._essid = ''

    def get_records(self):
        profile = self.read_profile()
        return profile['records']

    def is_in_records(self, essid):
        return essid in self.get_records().keys()

    def get_default(self):
        return self.read_profile()['default']

    def set_default(self, essid=None):
        if essid is None:
            records = list(self.get_records().keys())
            for index, item in enumerate(records):
                print(list_item(index, item))

            option = selection(
                'Please select an option as default wifi connection [0-%s]' % str(
                    len(records) - 1), len(records) - 1)

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
                    len(list(records.keys())) - 1), len(list(records.keys())) - 1)

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
                # n = len([0 for i in records.keys() if essid in i])
                # new_record = '%s#%s' % (essid, n) if n != 0 else essid
                # records[new_record] = passwd
                records[essid] = passwd

        else:
            records[essid] = passwd

        records = {'records': records}
        self.update_profile(records)

    def get_passwd(self, essid):
        if self.is_in_records(essid):
            return self.get_records()[essid]
        else:
            return None

    def scan(self, noreturn=True, noprint=False):
        self._wifi.active(True)
        print(rainbow('==> Scaning networks...', color='green'))

        def _list_wifi(index, essid, dbm):
            try:
                _index = ('[%s]' % str(index)).center(8).lstrip()
                _essid = rainbow(essid + (40 - len(essid)) * ' ', color='red')
                _dbm = rainbow(dbm.center(10).lstrip(), color='blue')
            except AttributeError:
                _index = ('[%s]' % str(index)).lstrip()
                _essid = rainbow(essid + (40 - len(essid)) * ' ', color='red')
                _dbm = rainbow(dbm.lstrip(), color='blue')
            if not noprint:
                print('{0} {1} {2} dBm'.format(_index, _essid, _dbm))

        networks = []
        for i in self._wifi.scan():
            # string decode may raise error
            try:
                nw = dict(essid=i[0].decode('utf-8'), dbm=str(i[3]))
            except:
                nw = dict(essid=str(i[0], 'ascii'), dbm=str(i[3]))
            finally:
                networks.append(nw)
        # networks = [dict(essid=i[0].decode(),dbm=str(i[3])) for i in self._wifi.scan()]

        for i, item in enumerate(networks):
            _list_wifi(i, item['essid'], item['dbm'])

        if not noreturn:
            return networks

    def auto_connect(self):
        if self._wifi.isconnected():
            print(
                rainbow('You have already established a Wifi connection.', color='blue'))

        else:
            if len(list(self.get_records().keys())) == 0:
                # 没有记录就直接连接
                self.connect()

            else:
                # 先查找是否有default值
                default_essid = self.get_default()['essid']
                # default 值不能为空
                if default_essid:
                    essids_in_records = [default_essid] + \
                        list(self.get_records().keys())
                else:
                    essids_in_records = list(self.get_records().keys())

                records = self.get_records()

                networks = [i['essid'] for i in self.scan(noreturn=False)]
                for essid in essids_in_records:

                    if essid in networks:
                        print(
                            rainbow('==> Trying to automatically connect to %s ...' % essid, color='blue'))
                        if self.connect(essid=essid, passwd=records[essid], noreturn=False, apexist=True):
                            print(
                                rainbow('==> Automatically connect to %s successfully' % essid, color='green'))
                            return
                        else:
                            print(
                                rainbow('==> Automatic connection to %s failed' % essid, color='red'))
                            self.del_record(essid)
                            continue

                print(rainbow('!!! No record available.', color='red'))
                self.connect()

    def _do_connect(self, essid, passwd):
        self._wifi.active(True)
        self._wifi.connect(essid, passwd)
        import time

        for i in range(300):
            if self._wifi.isconnected():
                break
            try:
                time.sleep_ms(100)
            except AttributeError:
                time.sleep(0.1)

        if not self._wifi.isconnected():
            self._wifi.active(False)
            print(rainbow('!!! WiFi connection error, please reconnect', color='red'))
            return False

        else:
            self._essid = essid
            self.ifconfig(noreturn=False)
            if not self.is_in_records(essid):
                self.add_record(essid, passwd)
            return True

    def connect(self, essid=None, passwd=None, noreturn=True, apexist=None):

        if essid is not None:
            if apexist is None:
                apexist = essid in [i['essid']
                                    for i in self.scan(noreturn=False, noprint=True)]

            if apexist:
                if passwd is not None:
                    result = self._do_connect(essid, passwd)
                    if not noreturn:
                        return result
                else:
                    # 只传入essid 便去查找记录以获得密码
                    passwd = self.get_passwd(essid)
                    if passwd is not None:
                        result = self._do_connect(
                            essid, self.get_passwd(essid))
                        if not noreturn:
                            return result
                    else:
                        print(rainbow('!!! The record was not found.', color='red'))
                        if not noreturn:
                            return False
            else:
                print(rainbow('!!! AP[ %s ] not found.' % essid, color='red'))
                if not noreturn:
                    return False

        else:
            networks = [i['essid'] for i in self.scan(noreturn=False)]
            select = selection('Choose a WiFi to connect', len(networks)-1)
            passwd = input('Password: ')
            essid = networks[select]
            result = self._do_connect(essid, passwd)
            if not noreturn:
                return result

    def disconnect(self):
        self._wifi.active(False)

    def ifconfig(self, noreturn=True):
        info = self._wifi.ifconfig()
        print(rainbow('==> You are connected to %s' %
                      self._essid, color='green'))
        print(rainbow(' --> IP: ' + info[0], color='blue'))
        print(rainbow(' --> Netmask: ' + info[1], color='blue'))
        print(rainbow(' --> Gateway: ' + info[2], color='blue'))
        if not noreturn:
            return info, self._essid


wifi = WiFi()
wifi.auto_connect()
