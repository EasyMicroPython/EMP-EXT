class Config:

    def __init__(self, path='/config', profile=None, options=None):
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


options = {
    'enable_wifi': 0,
    'emp_ide': {
        'enable': 1,
        'wireless': 2
    }
}


class Boot(Config):

    def __init__(self, profile='boot.config', options=None):
        super().__init__(profile=profile, options=options)


b = dict(enable_wifi=1)
a = Boot(profile='test2')
a.read_profile()
a.update_profile(b)
a.read_profile()