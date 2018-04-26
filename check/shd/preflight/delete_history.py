# -*- coding: utf-8 -*-
import os

from Qt import QtCore, QtWidgets, _loadUi, QtGui
import pymel.core as pm
import maya.api.OpenMaya as om

from hz.resources import HZResources
from config import config
from herirachy_checking import HerirachyChecking

class DelHistory(object):
    def __init__(self):
        self.name = 'Delete history'
        self.iconPath_red = HZResources.get_icon_resources('ic_build_black_24dp.png')
        self.iconPath_green = HZResources.get_icon_resources('ic_check_circle_black_24dp.png')
        self.unfreezed_models = []

    def change_icon(self, button, condition=True):
        icon = QtGui.QIcon()
        if condition:
            icon.addPixmap(QtGui.QPixmap(self.iconPath_red), QtGui.QIcon.Normal,
                           QtGui.QIcon.On)
        else:
            icon.addPixmap(QtGui.QPixmap(self.iconPath_green), QtGui.QIcon.Normal,
                           QtGui.QIcon.On)
        button.setIcon(icon)

    def get_all_obj_trans(self):
        def get_meshes(grp, obj_trans):
            for trans in grp:
                if pm.listRelatives(trans, s=True):
                    if pm.listRelatives(trans, s=True):
                        obj_trans.append(trans)
                else:
                    children = pm.listRelatives(trans)
                    temp = get_meshes(children, obj_trans)
                    obj_trans.extend(temp)
            return obj_trans

        herirachy_checking = HerirachyChecking()
        herirachy_checking.asset_filter()
        grp = [pm.PyNode(herirachy_checking.mod)]
        obj_trans = get_meshes(grp, [])
        return list(set(obj_trans))




class Main(DelHistory):
    def __init__(self, *args):
        super(Main, self).__init__()
        self.button_check = args[0]
        self.button_fix = args[1]
        self.button_c = args[2]

        self.button_check.setEnabled(False)
        self.button_c.setEnabled(False)

    def func_check(self):
        pass

    def func_fix(self):
        for trans in self.get_all_obj_trans():
            pm.delete(trans, ch=True)
        self.change_icon(self.button_fix, False)

    def func_c(self):
        pass
