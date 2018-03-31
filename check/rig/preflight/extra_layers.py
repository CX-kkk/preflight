# -*- coding: utf-8 -*-
import os

import maya.api.OpenMaya as om
import pymel.core as pm
from Qt import QtCore, QtWidgets, _loadUi, QtGui
from hz.resources import HZResources



class ExtraLayers(object):
    """
    -- layers check :
                  - display layer
                  - anim layer
                  - render layer
    """
    def __init__(self):
        self.name = 'Extra layers'
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
    def if_exists_extra_layers():
        display_layers = pm.general.ls(type='displayLayer')
        if len(display_layers) > 1:
            return True

        anim_layers = pm.general.ls(type='animLayer')
        if anim_layers:
            return True

        render_layers = pm.general.ls(type='renderLayer')
        if len(render_layers) > 1:
            return True

        return False

    @staticmethod
    def delete_extra_layers():
        try:
            pm.general.delete(
                [layer for layer in pm.general.ls(type='displayLayer') if layer.name() != 'defaultLayer'])
        except:
            return True
        try:
            pm.general.delete([layer for layer in pm.general.ls(type='animLayer')])
        except:
            return True
        try:
            pm.general.delete(
                [layer for layer in pm.general.ls(type='renderLayer') if layer.name() != 'defaultRenderLayer'])
        except:
            return True

        return False


class Main(ExtraLayers):
    def __init__(self, *args):
        super(Main, self).__init__()
        self.button_check = args[0]
        self.button_fix = args[1]
        self.button_c = args[2]

        self.button_c.setEnabled(False)

    def func_check(self):
        if self.if_exists_extra_layers():
            self.change_icon(self.button_check, True)
        else:
            self.change_icon(self.button_check, False)

    def func_fix(self):
        undeleted = self.delete_extra_layers()
        if undeleted:
            om.MGlobal.displayWarning('There\'s still some layers exists, please check it manually.')
        self.change_icon(self.button_check, undeleted)
        self.change_icon(self.button_fix, undeleted)

    def func_c(self):
        pass
