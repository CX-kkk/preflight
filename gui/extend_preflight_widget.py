# -*- coding: utf-8 -*-
import os
import sys
import importlib
from functools import partial

from Qt import QtCore, QtWidgets, _loadUi, QtGui
from hz.resources import HZResources

import basic_gui


class PreflightItem(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PreflightItem, self).__init__(parent)
        self.iconPath = HZResources.get_icon_resources('ic_airplay_black_24dp.png')
        self.buttons = {}

    def create_button(self, func, button):
        button.setMaximumSize(QtCore.QSize(25, 25))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.iconPath), QtGui.QIcon.Normal,
                       QtGui.QIcon.On)
        button.setIcon(icon)
        button.setFlat(True)
        button.clicked.connect(partial(func))
        return button

    def preflight_item(self, label, func_check, func_fix, func_c, set_checked=True):
        widget = QtWidgets.QWidget()
        horizontal_layout = QtWidgets.QHBoxLayout(widget)
        widget.setStatusTip('False')

        self.checkbox_name = QtWidgets.QCheckBox()
        self.checkbox_name.setText(label)
        self.checkbox_name.setObjectName(label)
        self.checkbox_name.setChecked(set_checked)

        spaceritem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        pushbutton_a = self.create_button(func_check, self.button_a)
        pushbutton_b = self.create_button(func_fix, self.button_b)
        pushbutton_c = self.create_button(func_c, self.button_c)

        horizontal_layout.addWidget(self.checkbox_name)
        horizontal_layout.addItem(spaceritem)
        horizontal_layout.addWidget(pushbutton_a)
        horizontal_layout.addWidget(pushbutton_b)
        horizontal_layout.addWidget(pushbutton_c)

        return widget

    def func_check(self):
        pass

    def func_fix(self):
        pass

    def func_c(self):
        pass


class PreflightWidget(PreflightItem):
    def __init__(self, parent=None, step=''):
        super(PreflightWidget, self).__init__(parent)
        ui_file = os.path.join(os.path.dirname(__file__), 'preflight_widget.ui')
        _loadUi(ui_file, self)
        self.step = step
        self.init_ui()
        self.init_layout()

    def init_ui(self):
        self.listWidget_preflight = basic_gui.ListWidget()

    def init_layout(self):
        self.verticalLayout_preflight.addWidget(self.listWidget_preflight)
        step_module = importlib.import_module('check.{}.preflight'.format(self.step))
        for item in dir(step_module):
            if item not in ['__builtins__', '__doc__', '__file__', '__name__', '__package__', '__path__']:
                module = importlib.import_module('check.{}.preflight.{}'.format(self.step, item))
                # instance = module.Main()

                self.button_a = QtWidgets.QPushButton()
                self.button_b = QtWidgets.QPushButton()
                self.button_c = QtWidgets.QPushButton()
                instance = module.Main(self.button_a, self.button_b, self.button_c)
                temp = self.preflight_item(instance.name,
                                           partial(self.func_check, instance.func_check),
                                           instance.func_fix,
                                           instance.func_c,
                                           set_checked=True)
                self.listWidget_preflight.add_item(temp, metadata=instance.name)

    def func_check(self, func=None):
        if func:
            func()
        else:
            print 'Please link a function first.'


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    step = 'mdl'
    aa = PreflightWidget(step=step)
    aa.show()
    sys.exit(app.exec_())
