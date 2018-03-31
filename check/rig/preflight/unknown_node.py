# -*- coding: utf-8 -*-
import os

import maya.api.OpenMaya as om
import pymel.core as pm
from Qt import QtCore, QtWidgets, _loadUi, QtGui
from hz.resources import HZResources



class UnknownNodes(object):
    def __init__(self):
        self.name = 'Unknown Nodes'
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

    def get_unknown_nodes(self):
        """
        Get unknown nodes.
        :return:
        """
        return pm.general.ls(type='unknown')

    def remove_turtle_nodes(self):
        uns = pm.general.ls(type='unknown')
        if len(uns):
            try:
                pm.general.lockNode(uns, lock=False)
                pm.general.delete(uns)
            except:
                return True


class Main(UnknownNodes):
    def __init__(self, *args):
        super(Main, self).__init__()
        self.button_check = args[0]
        self.button_fix = args[1]
        self.button_c = args[2]

        self.button_c.setEnabled(False)

    def func_check(self):
        unknown_nodes = self.get_unknown_nodes()
        self.change_icon(self.button_check, unknown_nodes)

    def func_fix(self):
        if_deleted = self.remove_turtle_nodes()
        if if_deleted:
            om.MGlobal.displayWarning('Failed to delete unknown nodes...')
        self.change_icon(self.button_check, if_deleted)
        self.change_icon(self.button_fix, if_deleted)

    def func_c(self):
        pass


