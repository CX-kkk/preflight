# -*- coding: utf-8 -*-
import os
import sys
import importlib
from functools import partial

from Qt import QtCore, QtWidgets, _loadUi, QtGui
from hz.resources import HZResources

from check.mdl.check_a import CheckA
from check.mdl.check_b import CheckB



class PreflightItem(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PreflightItem, self).__init__(parent)
        self.iconPath = HZResources.get_icon_resources('ic_airplay_black_24dp.png')

    def preflight_item(self, label, func_a, func_b, func_c):
        def create_button(func):
            button = QtWidgets.QPushButton()
            button.setMaximumSize(QtCore.QSize(25, 25))
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(self.iconPath), QtGui.QIcon.Normal, QtGui.QIcon.On)
            button.setIcon(icon)
            button.setFlat(True)
            button.clicked.connect(func)
            return button

        widget = QtWidgets.QWidget()
        horizontal_layout = QtWidgets.QHBoxLayout(widget)

        checkbox_name = QtWidgets.QCheckBox()
        checkbox_name.setText(label)
        checkbox_name.setChecked(True)

        spaceritem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        pushbutton_a = create_button(func_a)
        pushbutton_b = create_button(func_b)
        pushbutton_c = create_button(func_c)

        horizontal_layout.addWidget(checkbox_name)
        horizontal_layout.addItem(spaceritem)
        horizontal_layout.addWidget(pushbutton_a)
        horizontal_layout.addWidget(pushbutton_b)
        horizontal_layout.addWidget(pushbutton_c)

        return widget

    def func_a(self, func=None):
        pass

    def func_b(self):
        pass

    def func_c(self):
        pass


class PreflightWidget(PreflightItem):
    def __init__(self, parent=None, step=''):
        super(PreflightWidget, self).__init__(parent)
        ui_file = os.path.join(os.path.dirname(__file__), 'preflight_widget.ui')
        _loadUi(ui_file, self)
        self.step = step
        self.init_layout()

    def init_layout(self):
        step_module = importlib.import_module('check.{}'.format(self.step))
        for item in dir(step_module):
            if item not in ['__builtins__', '__doc__', '__file__', '__name__', '__package__', '__path__']:
                module = importlib.import_module('check.{}.{}'.format(self.step, item))
                instance = module.Main()
                self.verticalLayout_preflight.addWidget(self.preflight_item(instance.name,
                                                                            partial(self.func_a, instance.func_a),
                                                                            instance.func_b, instance.func_c))

    def func_a(self, func=None):
        if func:
            func()
        else:
            print 'aaa'


if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    step = 'mdl'
    aa = PreflightWidget(step=step)
    aa.show()
    sys.exit(app.exec_())