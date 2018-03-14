# -*- coding: utf-8 -*-
# import pymel.core as pm
import os

from Qt import QtCore, QtWidgets, _loadUi, QtGui

from hz.resources import HZResources


class ExtraShdersInMdl(object):
    def __init__(self):
        self.name = 'Extra shaders'
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
        # shaders = pm.ls(mat=True)
        # default_shaders = [pm.PyNode(u'lambert1'), pm.PyNode(u'particleCloud1')]
        # extra_shaders = list( set(shaders)-set(default_shaders) )
        extra_shaders = ['aa']
        self.change_icon(button, extra_shaders)


    def func_fix(self, button=None):
        extra_shaders = ['aa']
        self.change_icon(button, extra_shaders)

    def func_c(self, button=None):
        extra_shaders = []
        self.change_icon(button, extra_shaders)


class Main(ExtraShdersInMdl):
    def __init__(self):
        super(Main, self).__init__()
        pass
