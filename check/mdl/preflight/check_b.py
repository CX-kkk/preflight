# -*- coding: utf-8 -*-


class CheckB(object):
    def __init__(self):
        self.name = 'check_b'

    def func_a(self):
        print 'check_b_a'

    def func_b(self):
        print 'check_b_b'

    def func_c(self):
        print 'check_b_c'


class Main(CheckB):
    def __init__(self):
        super(Main, self).__init__()
        pass
