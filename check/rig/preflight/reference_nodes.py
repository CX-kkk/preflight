# -*- coding: utf-8 -*-
import os

import maya.api.OpenMaya as om
import pymel.core as pm
from Qt import QtCore, QtWidgets, _loadUi, QtGui
from hz.resources import HZResources



class ReferencesNodes(object):
    """
    Remove reference nodes
    """
    def __init__(self):
        self.name = 'References Nodes'
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
    def get_referenced_nodes():
        return pm.general.ls(type='reference')

    def remove_referenced_nodes(self):
        for ref_node in self.referenced_nodes:
            if ref_node.referenceFile() != None:
                try:
                    ref_node.referenceFile().load()
                    ref_node.referenceFile().importContents(removeNamespace=True)
                except:
                    print 'Load {} reference failed...'.format(ref_node)
            else:
                ref_node.unlock()
                pm.general.delete(ref_node)

        return pm.general.ls(type='reference')


class Main(ReferencesNodes):
    def __init__(self, *args):
        super(Main, self).__init__()
        self.button_check = args[0]
        self.button_fix = args[1]
        self.button_c = args[2]

        self.button_c.setEnabled(False)

    def func_check(self):
        self.referenced_nodes = self.get_referenced_nodes()
        self.change_icon(self.button_check, self.referenced_nodes)

    def func_fix(self):
        referenced_nodes = self.remove_referenced_nodes()
        if referenced_nodes:
            om.MGlobal.displayWarning('Auto fix failed...Please remove reference nodes manually..')
        self.change_icon(self.button_check, referenced_nodes)
        self.change_icon(self.button_fix, referenced_nodes)

    def func_c(self):
        pass
