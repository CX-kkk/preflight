# -*- coding: utf-8 -*-
import os
import sys

from BQt import QtCore, QtWidgets, uic, QtGui

from step.mdl.check_a import CheckA
from step.mdl.check_b import CheckB


class PreflightItem(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PreflightItem, self).__init__(parent)
        self.iconPath = '/local/bfx_extend_maya/common/bfx_maya/toolset/rig/skinClusterLibrary/icon'

    def preflight_item(self, label, func_a, func_b, func_c):
        def create_button(func):
            button = QtWidgets.QPushButton()
            button.setMaximumSize(QtCore.QSize(25, 25))
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconPath, 'icon_link.png')), QtGui.QIcon.Normal,
                           QtGui.QIcon.On)
            button.setIcon(icon)
            button.setFlat(True)
            print func
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
        if func:
            func()
        else:
            print 'aaa'

    def func_b(self):
        pass

    def func_c(self):
        pass


class PreflightWidget(PreflightItem):
    def __init__(self, parent=None):
        super(PreflightWidget, self).__init__(parent)
        ui_file = os.path.join(os.path.dirname(__file__), 'preflight.ui')
        uic.loadUi(ui_file, self)

        self.init_layout()

    def init_layout(self):
        check_a = CheckA()
        check_b = CheckB()
        self.verticalLayout_preflight.addWidget(self.preflight_item(check_a.name, self.func_a, check_a.func_b, check_a.func_c))
        self.verticalLayout_preflight.addWidget(self.preflight_item(check_b.name, check_b.func_a, check_b.func_b, check_b.func_c))


if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    aa = PreflightWidget()
    aa.show()

    sys.exit(app.exec_())