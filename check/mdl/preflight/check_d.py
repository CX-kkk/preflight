# -*- coding: utf-8 -*-


class CheckD(object):
    def __init__(self):
        self.name = 'check_d'

    def func_a(self):
        print 'check_d_a'

    def func_b(self):
        print 'check_d_b'

    def func_c(self):
        print 'check_d_c'


class Main(CheckD):
    def __init__(self):
        super(Main, self).__init__()
        pass
