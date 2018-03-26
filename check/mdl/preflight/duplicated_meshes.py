# -*- coding: utf-8 -*-
import os

from Qt import QtCore, QtWidgets, _loadUi, QtGui

from hz.resources import HZResources
import maya.api.OpenMaya as om
import pymel.core as pm

from config import config
from herirachy_checking import HerirachyChecking


class DuplicatedMeshes(object):
    def __init__(self):
        self.name = 'Duplicated meshes'
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
    def ser_child():
        names = []
        paths = []
        herirachy_checking = HerirachyChecking()
        herirachy_checking.asset_filter()
        sel_first = herirachy_checking.mod
        # sel_first = 'aaa_mod'

        def getChildObj(sel_first, names, paths):
            sel_first_NodeType = pm.ls(sel_first, long=True)
            name = sel_first.split('|', -1)[-1]
            path = sel_first_NodeType[0].fullPath()
            nodeType = sel_first_NodeType[0].nodeType()
            if nodeType in ['mesh', 'locator', 'joint']:
                names.append(name)
                paths.append(path)
            sre_objs = pm.listRelatives(sel_first, children=True, path=True)
            if sre_objs != None:
                for obj in sre_objs:
                    names, paths = getChildObj(obj, names, paths)

            return names, paths

        names, paths = getChildObj(sel_first, names, paths)
        return names, paths


    @staticmethod
    def find_func(find_str, find_path):
        rl = dict()
        for i in range(len(find_str)):
            m = find_path[i]
            if find_str.count(find_str[i]) <= 1:
                continue
            if not rl.has_key(find_str[i]):
                rl[find_str[i]] = list()
                rl[find_str[i]].append(m)
            else:
                rl[find_str[i]].append(m)

        if rl: om.MGlobal.displayWarning('Here\'s the duplicated names in scene. Please check them in Script Editor')
        for key in rl:
            print key
            print rl[key]
        print 'Search OverEnd!!!!'
        return rl



class Main(DuplicatedMeshes):
    def __init__(self, *args):
        super(Main, self).__init__()
        print
        print
        print '-------------', args
        print
        print
        self.button_check = args[0]
        self.button_fix = args[1]
        self.button_c = args[2]
        self.duplicated_meshes = []

        self.button_c.setEnabled(False)

    def func_check(self):
        names, paths = self.ser_child()
        self.duplicated_meshes = self.find_func(names, paths)
        self.change_icon(self.button_check, bool(self.duplicated_meshes))

    def func_fix(self):
        if self.duplicated_meshes:
            print
            print self.duplicated_meshes
            print
            om.MGlobal.displayWarning('Please fixed it manully. Check objs with same names in script editor.')
        # self.change_icon(self.button_fix, extra_shaders)

    def func_c(self):
        pass
