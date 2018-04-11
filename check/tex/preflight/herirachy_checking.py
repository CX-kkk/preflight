# -*- coding: utf-8 -*-
import os

from Qt import QtCore, QtWidgets, _loadUi, QtGui

from hz.resources import HZResources
import pymel.core as pm
import maya.api.OpenMaya as om

from config import config


class HerirachyChecking(object):
    def __init__(self):
        self.name = 'Herirachy checking'
        self.iconPath_red = HZResources.get_icon_resources('ic_build_black_24dp.png')
        self.iconPath_green = HZResources.get_icon_resources('ic_check_circle_black_24dp.png')
        self.high_geo = ''

    def change_icon(self, button, condition=True):
        icon = QtGui.QIcon()
        if condition:
            icon.addPixmap(QtGui.QPixmap(self.iconPath_red), QtGui.QIcon.Normal,
                           QtGui.QIcon.On)
        else:
            icon.addPixmap(QtGui.QPixmap(self.iconPath_green), QtGui.QIcon.Normal,
                           QtGui.QIcon.On)
        button.setIcon(icon)

    def asset_filter(self):
        self.illegal_objs = []
        self.fixing_list = []
        root = pm.ls(assemblies=True, recursive=True)
        lods = []
        for asset in root:
            mod = asset.listRelatives()
            if len(mod) == 1:
                temp_lods = mod[0].listRelatives(f=True)
                for lod in temp_lods:
                    if lod.listRelatives():
                        if lod.fullPath().split('_')[-1].upper() in config.LOD_LIST:
                            if lod.rsplit('_', 1)[-1].upper() == 'HIGH':
                                self.high_geo = lod
                                self.mod = lod.fullPath().split('|')[2]
                            lods.append(lod.fullPath())
                        else:
                            if lod.fullPath() not in self.illegal_objs:
                                self.illegal_objs.append(lod.fullPath())
        return lods

    def hireachy_checking(self):
        fixing_list = []
        lods = self.asset_filter()
        if lods:
            for each in lods:
                if each != '|{0}|{0}_MDL|{0}_{1}'.format(each.split('|')[1], each.rsplit('_', 1)[-1].upper()):
                    fixing_list.append(each)
        return fixing_list

    def hireachy_fixing(self):
        change_dic = {}
        if self.fixing_list:
            for each in self.fixing_list:
                sep = each.split('|')[1:]
                if sep[1] != '{}_MDL'.format(sep[0]):
                    change_dic[sep[1]] = '{}_MDL'.format(sep[0])
                if sep[2] != '{}_{}'.format(sep[0], sep[2].split('_')[-1].upper()):
                    change_dic[sep[2]] = '{}_{}'.format(sep[0], sep[2].split('_')[-1].upper())
        for key in change_dic:
            pm.rename(key, change_dic[key])

        if self.illegal_objs:
            print self.illegal_objs
            om.MGlobal.displayWarning('Please fixed it manully.[Please check it in script editor.]')


class Main(HerirachyChecking):
    def __init__(self, *args):
        super(Main, self).__init__()
        self.button_check = args[0]
        self.button_fix = args[1]
        self.button_c = args[2]

        self.button_c.setEnabled(False)

    def func_check(self):
        self.fixing_list = self.hireachy_checking()
        result = bool(self.fixing_list or self.illegal_objs)
        self.change_icon(self.button_check, result)

    def func_fix(self):
        self.hireachy_fixing()
        self.fixing_list = self.hireachy_checking()
        result = self.fixing_list or self.illegal_objs
        self.change_icon(self.button_fix, result)
        self.change_icon(self.button_check, result)

    def func_c(self):
        pass
