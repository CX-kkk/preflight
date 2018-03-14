# -*- coding: utf-8 -*-
import os

from Qt import QtCore, QtWidgets, _loadUi, QtGui

from hz.resources import HZResources


class CheckC(object):
    def __init__(self):
        self.name = 'check_c'
        self.iconPath_red = HZResources.get_icon_resources('ic_build_black_24dp.png')
        self.iconPath_green = HZResources.get_icon_resources('ic_check_circle_black_24dp.png')

    def change_icon(self, button, condition=True):
        icon = QtGui.QIcon()
        if condition:
            icon.addPixmap(QtGui.QPixmap(self.iconPath_red), QtGui.QIcon.Normal,
                           QtGui.QIcon.On)
        else:
            icon.addPixmap(QtGui.QPixmap(self.iconPath_green), QtGui.QIcon.Normal,
                           QtGui.QIcon.On)
        button.setIcon(icon)

    def func_check(self, button=None):
        extra_shaders = ['aa']
        self.change_icon(button, extra_shaders)

    def func_fix(self, button=None):
        extra_shaders = ['aa']
        self.change_icon(button, extra_shaders)

    def func_c(self, button=None):
        extra_shaders = ['aa']
        self.change_icon(button, extra_shaders)


class Main(CheckC):
    def __init__(self):
        super(Main, self).__init__()
        pass
