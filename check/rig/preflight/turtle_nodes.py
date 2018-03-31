# -*- coding: utf-8 -*-
import os

import maya.api.OpenMaya as om
import maya.mel as mel
import pymel.core as pm
from Qt import QtCore, QtWidgets, _loadUi, QtGui
from hz.resources import HZResources



class UnloadedTurtle(object):
    def __init__(self):
        self.name = 'Turtle Nodes'
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

    def get_turtle_nodes(self):
        """
        If Turtle plug-in is loaded.
        :return:
        """
        plugins = pm.system.pluginInfo(q=True, pu=True)
        if not plugins:
            return
        if 'Turtle' in plugins:
            return True

    def remove_turtle_nodes(self):
        # mel.eval('ilrClearScene')
        try:
            pm.system.unloadPlugin('Turtle', f=True)
            return False
        except:
            return True


class Main(UnloadedTurtle):
    def __init__(self, *args):
        super(Main, self).__init__()
        self.button_check = args[0]
        self.button_fix = args[1]
        self.button_c = args[2]

        self.button_c.setEnabled(False)

    def func_check(self):
        if_turtle_loaded = self.get_turtle_nodes()
        self.change_icon(self.button_check, if_turtle_loaded)

    def func_fix(self):
        if_removed = self.remove_turtle_nodes()
        if if_removed:
            om.MGlobal.displayWarning('Failed to unloadPlugin Turtle...')
        self.change_icon(self.button_check, if_removed)
        self.change_icon(self.button_fix, if_removed)

    def func_c(self):
        pass
