# -*- coding: utf-8 -*-
import os

from Qt import QtCore, QtWidgets, _loadUi, QtGui
import pymel.core as pm

from hz.resources import HZResources
from config import config


class FreezeTransform(object):
    def __init__(self):
        self.name = 'Freeze transform'
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
    def org_transform_value():
        transform_attr_list = ["translate", "rotate", "scale"]
        base_transform = dict()

        for axis in ["X", "Y", "Z"]:
            for transformAttr in transform_attr_list:
                if transformAttr != "scale":
                    base_transform[transformAttr + axis] = 0.0
                else:
                    base_transform[transformAttr + axis] = 1.0
        return base_transform

    def check_model_freeze_tranosformations(self, check_model_list):
        re_list = list()
        base_attr_infos = self.org_transform_value()
        for check_model in check_model_list:
            for attr_info in base_attr_infos:
                if pm.getAttr(check_model + "." + attr_info) != base_attr_infos[attr_info]:
                    re_list.append(check_model + "." + attr_info)
        return re_list


class Main(FreezeTransform):
    def __init__(self, *args):
        super(Main, self).__init__()
        self.button_check = args[0]
        self.button_fix = args[1]
        self.button_c = args[2]

        self.button_c.setEnabled(False)

    def func_check(self):
        sel_obj = [pm.PyNode(config.ROOT)]
        unfreeze_trans = self.check_model_freeze_tranosformations(sel_obj)
        print unfreeze_trans
        self.change_icon(self.button_check, unfreeze_trans)

    def func_fix(self):
        extra_shaders = ['aa']
        self.change_icon(self.button_fix, extra_shaders)

    def func_c(self):
        pass
