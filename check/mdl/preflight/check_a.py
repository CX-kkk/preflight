# -*- coding: utf-8 -*-


class CheckA(object):
    def __init__(self):
        self.name = 'check_a'

    def func_a(self):
        print 'check_a_a'

    def func_b(self):
        print 'check_a_b_aaaaaaaaaaaaaaaaaaaa'

    def func_c(self):
        print 'check_a_c'


class Main(CheckA):
    def __init__(self):
        super(Main, self).__init__()
        pass



