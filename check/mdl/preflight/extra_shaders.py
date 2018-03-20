# -*- coding: utf-8 -*-
import os

from Qt import QtCore, QtWidgets, _loadUi, QtGui
import pymel.core as pm
import maya.mel as mel

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

    @staticmethod
    def get_extra_shaders():
        shaders = pm.ls(mat=True)
        default_shaders = [pm.PyNode(u'lambert1'), pm.PyNode(u'particleCloud1')]
        extra_shaders = []
        for shader in list(set(shaders) - set(default_shaders)):
            for sg in shader.listConnections(type='shadingEngine'):
                if not sg.listConnections(type='mesh'):
                    extra_shaders.append(shader)
        return extra_shaders




class Main(ExtraShdersInMdl):
    def __init__(self, *args):
        super(Main, self).__init__()
        self.button_check = args[0]
        self.button_fix = args[1]
        self.button_c = args[2]

        self.button_c.setEnabled(False)

    def func_check(self):
        extra_shaders = self.get_extra_shaders()
        self.change_icon(self.button_check, extra_shaders)

    def func_fix(self):
        mel.eval('MLdeleteUnused')
        extra_shaders = self.get_extra_shaders()
        if extra_shaders:
            print 'Check if referenced shaders inside.'
        self.change_icon(self.button_fix, extra_shaders)

    def func_c(self):
        pass
