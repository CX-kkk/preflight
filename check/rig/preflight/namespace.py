# -*- coding: utf-8 -*-
import os

import maya.api.OpenMaya as om
import pymel.core as pm
from Qt import QtCore, QtWidgets, _loadUi, QtGui
from hz.resources import HZResources



class Namespaces(object):
    def __init__(self):
        self.name = 'Extra namespaces'
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

    def get_namespaces(self):
        nss = pm.system.namespaceInfo(listOnlyNamespaces=True)
        namespaces = filter(lambda x: x not in [u'UI', u'shared'], nss)
        return namespaces

    def clean_namespaces(self):
        shits = []
        for ns in self.namespaces:
            try:
                pm.system.namespace(f=True, moveNamespace=(ns, ":"))
                pm.system.namespace(removeNamespace=ns)
            except:
                shits.append(ns)

        self.namespaces = shits if shits else []
        return self.namespaces


class Main(Namespaces):
    def __init__(self, *args):
        super(Main, self).__init__()
        self.button_check = args[0]
        self.button_fix = args[1]
        self.button_c = args[2]

        self.button_c.setEnabled(False)

    def func_check(self):
        self.namespaces = self.get_namespaces()
        print 'exists namespaces:', self.namespaces
        self.change_icon(self.button_check, self.namespaces)

    def func_fix(self):
        shit_namespace = self.clean_namespaces()
        if shit_namespace:
            om.MGlobal.displayWarning('Failed to clean namespace automatically, please check it manually...')
        self.change_icon(self.button_check, shit_namespace)
        self.change_icon(self.button_fix, shit_namespace)

    def func_c(self):
        pass
