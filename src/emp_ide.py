import gc
import json
import os
import sys

from emp_utils import is_folder, traverse
from emp_utils import WebREPL


def emp_sender(func):
    def wrapper(*args, **kwargs):
        rsp = func(*args, **kwargs)
        repl_type = rsp['repl_type']
        if repl_type == 0:
            sys.stdout.write(
                b'==> PDU START\n\n%s\n\n==> PDU END\n\r' % json.dumps(rsp))
        else:
            WebREPL.send(json.dumps(rsp) + '\n\r')

        gc.collect()
    return wrapper


class IDE:
    def __init__(self, repl_type=0):
        repl_types = (0, 1)
        if repl_type in repl_types:
            self.repl_type = repl_types[repl_type]
        else:
            assert False, 'repl type can only be 0 or 1'

    @emp_sender
    def device_info(self):
        return {'repl_type': self.repl_type, 'func': 'device_info', 'data': dict(
            platform=sys.platform,
            version=sys.version,
            implementation=[sys.implementation[0],
                            list(sys.implementation[1])],
            maxsize=sys.maxsize / 1024 / 1024)}

    @emp_sender
    def memory_status(self):
        gc.collect()
        return {'repl_type': self.repl_type, 'func': 'memory_status', 'data': dict(alloced=gc.mem_alloc() / 1024, free=gc.mem_free() / 1024)}

    @emp_sender
    def memory_analysing(self, filename):
        gc.collect()
        fsize = os.stat(filename)[6]
        mf = gc.mem_free()
        return {'repl_type': self.repl_type, 'func': 'memory_analysing', 'data': dict(fsize=fsize, mf=mf, filename=filename)}

    @emp_sender
    def tree(self, path='/'):
        return {'repl_type': self.repl_type, 'func': 'tree', 'data': traverse(path)}

    @emp_sender
    def get_code(self, filename):
        gc.collect()
        with open(filename, 'rb') as f:
            code = f.read()
            rsp = {'repl_type': self.repl_type, 'func': 'get_code',
                   'data': dict(code=code.decode("utf-8"), filename=filename)}
            self.memory_status()
        return rsp

    def new_folder(self, folder):
        try:
            os.mkdir(folder)
        except:
            pass
        self.tree()

    def new_file(self, filename):
        with open(filename, 'w') as f:
            print(f.write(''))
        self.tree()

    def del_folder(self, path):
        for i in os.listdir(path):
            if is_folder(path + '/' + i):
                self.del_folder(path + '/' + i)
            else:
                os.remove(path + '/' + i)

        os.rmdir(path)
        self.tree()

    def del_file(self, filename):
        os.remove(filename)
        self.tree()

    def rename(self, old_name, new_name):
        try:
            os.rename(old_name, new_name)
            self.tree()
        except:
            pass

    def emp_install(self, pkg):
        try:
            upip.install(pkg)
        except:
            import upip
            upip.install(pkg)


ide = IDE(0)
