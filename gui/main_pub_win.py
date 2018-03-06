# -*- coding: utf-8 -*-
import os
import sys
from functools import partial

from Qt import QtCore, QtWidgets, _loadUi, QtGui

from extend_preflight_widget import PreflightWidget


class PreviewWidget(QtWidgets.QMainWindow):
    def __init__(self, parent=None, step=''):
        super(PreviewWidget, self).__init__(parent)

        self.step = step

        self.preflight_widget = PreflightWidget(step=self.step)
        ui_file = os.path.join(os.path.dirname(__file__), 'pub_win.ui')
        _loadUi(ui_file, self)

        self.setWindowTitle('{} Publish Tool'.format(self.step.upper()))

        self.init_layout()

    def init_layout(self):
        self.verticalLayout_flame.addWidget(self.preflight_widget)
        # self.verticalLayout_flame.addWidget(self.pub_widget)




if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    step = 'xxx'
    aa = PreviewWidget(step='mdl')
    aa.show()
    sys.exit(app.exec_())
