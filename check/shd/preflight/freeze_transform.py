# -*- coding: utf-8 -*-
import os

from Qt import QtCore, QtWidgets, _loadUi, QtGui
import pymel.core as pm
import maya.api.OpenMaya as om

from config import config
from hz.resources import HZResources
from herirachy_checking import HerirachyChecking

class FreezeTransform(object):
    def __init__(self):
        self.name = 'Freeze transform'
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
        self.unfreezed_models = []
        base_attr_infos = self.org_transform_value()
        for check_model in check_model_list:
            for attr_info in base_attr_infos:
                if pm.getAttr(check_model + "." + attr_info) != base_attr_infos[attr_info]:
                    re_list.append(check_model + "." + attr_info)
                    if check_model not in self.unfreezed_models:
                        self.unfreezed_models.append(check_model.name())
        return re_list

    @staticmethod
    def get_unfreezing_meshes():
        def get_meshes(grp, unfreezing_list):
            for trans in grp:
                if trans.nodeType() == 'transform':
                    unfreezing_list.append(trans)
                    extend_list = get_meshes(pm.listRelatives(trans), unfreezing_list)
                    # unfreezing_list.extend(extend_list)

            return list(set(unfreezing_list))

        herirachy_checking = HerirachyChecking()
        herirachy_checking.asset_filter()
        grp = [pm.PyNode(herirachy_checking.mod)]
        unfreezing_list = []
        unfreezing_meshes = get_meshes(grp, unfreezing_list)
        return unfreezing_meshes


class Main(FreezeTransform):
    def __init__(self, *args):
        super(Main, self).__init__()
        self.button_check = args[0]
        self.button_fix = args[1]
        self.button_c = args[2]

        self.button_c.setEnabled(False)

    def func_check(self):
        sel_obj = self.get_unfreezing_meshes()
        self.unfreeze_trans = self.check_model_freeze_tranosformations(sel_obj)
        if self.unfreeze_trans:
            om.MGlobal.displayWarning(','.join(self.unfreezed_models))
        self.change_icon(self.button_check, self.unfreeze_trans)

    def func_fix(self):
        print self.unfreezed_models
        for trans in self.unfreezed_models:
            pm.makeIdentity(trans, apply=True, t=True, r=True, s=True, n=False, pn=True)
        self.change_icon(self.button_fix, False)
        self.change_icon(self.button_check, False)

    def func_c(self):
        pass
