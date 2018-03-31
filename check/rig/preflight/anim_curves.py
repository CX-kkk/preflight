# -*- coding: utf-8 -*-
# Description:  Publish Toolkit - Check - Module
#                   - Animation curve in scene ?
import os

import maya.api.OpenMaya as om
import maya.cmds as cmds
import pymel.core as pm
from Qt import QtCore, QtWidgets, _loadUi, QtGui
from hz.resources import HZResources

CURVE_TYPE = [
    # 'animCurve',
    'animCurveTA',
    'animCurveTL',
    'animCurveTT',
    'animCurveTU',
    # 'animCurveUA',
    # 'animCurveUL',
    # 'animCurveUT',
    # 'animCurveUU'
]


class AnimCurves(object):
    """
    Check Animation curve in scene. There's not supposed to have anim curves in Rigging files.
    """
    def __init__(self):
        self.name = 'Anim curves'
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

    def get_anim_curves(self):
        illegal_anim_curves = []
        all_curves = pm.general.ls(type=CURVE_TYPE)
        for item in all_curves:
            if cmds.listConnections(item.nodeName(), s=True, d=False):
                continue
            if cmds.listConnections('{}.message'.format(item.nodeName())):
                continue
            if cmds.listConnections(item.nodeName(), type='frameCache'):
                continue
            illegal_anim_curves.append(item)
        return illegal_anim_curves


class Main(AnimCurves):
    def __init__(self, *args):
        super(Main, self).__init__()
        self.button_check = args[0]
        self.button_fix = args[1]
        self.button_c = args[2]

        self.button_c.setEnabled(False)

    def func_check(self):
        self.illegal_anim_curves = self.get_anim_curves()
        if len(self.illegal_anim_curves):
            self.change_icon(self.button_check, True)
            om.MGlobal.displayWarning('Animation curves in scene...\n{}\nFailed...'.format(self.illegal_anim_curves))
        else:
            self.change_icon(self.button_check, False)

    def func_fix(self):
        if not self.illegal_anim_curves:
            self.change_icon(self.button_check, False)
            self.change_icon(self.button_fix, False)
            return
        try:
            pm.general.lockNode(self.illegal_anim_curves, lock=False)
            pm.general.delete(self.illegal_anim_curves)
            self.illegal_anim_curves = []
            self.change_icon(self.button_check, False)
            self.change_icon(self.button_fix, False)
        except:
            self.change_icon(self.button_fix, True)
            om.MGlobal.displayWarning('There\s still some anim curves in current scene. Please ask TD for help.')

    def func_c(self):
        pass
