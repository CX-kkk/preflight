# -*- coding: utf-8 -*-


class CheckE(object):
    def __init__(self):
        self.name = 'check_e'

    def func_a(self):
        print 'check_e_a'

    def func_b(self):
        print 'check_e_b'

    def func_c(self):
        print 'check_e_c'


class Main(CheckE):
    def __init__(self):
        super(Main, self).__init__()
        pass
