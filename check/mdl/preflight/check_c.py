# -*- coding: utf-8 -*-


class CheckC(object):
    def __init__(self):
        self.name = 'check_c'

    def func_a(self):
        print 'check_c_a'

    def func_b(self):
        print 'check_c_b'

    def func_c(self):
        print 'check_c_c'


class Main(CheckC):
    def __init__(self):
        super(Main, self).__init__()
        pass
