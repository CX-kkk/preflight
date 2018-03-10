# -*- coding: utf-8 -*-
import importlib
import os
import sys
from functools import partial

from Qt import QtCore, QtWidgets, _loadUi, QtGui

from extend_preflight_widget import PreflightWidget
from extend_pub_widget import PubWidget
from gui import basic_gui


class PreviewWidget(QtWidgets.QMainWindow):
    def __init__(self, parent=None, step=''):
        super(PreviewWidget, self).__init__(parent)

        self.step = step
        ui_file = os.path.join(os.path.dirname(__file__), 'pub_win.ui')
        _loadUi(ui_file, self)

        self.preflight_widget = PreflightWidget(step=self.step)
        self.pub_widget = PubWidget(step=self.step)
        step_module = importlib.import_module('check.{}.gui.extend_pub_widget'.format(self.step))
        self.extend_pub_widget = step_module.ExtendPubWidget()

        self.setWindowTitle('{} Publish Tool'.format(self.step.upper()))
        self.init_layout()
        self.init_connectiond()

    def init_layout(self):
        self.listWidget_pub = basic_gui.ListWidget()

        self.listWidget_pub.add_item(self.pub_widget, height=self.pub_widget.height())
        self.listWidget_pub.add_item(self.extend_pub_widget, height=self.extend_pub_widget.height())

        self.label = QtWidgets.QLabel(' Publish')

        self.verticalLayout_publish.addWidget(self.preflight_widget)
        self.verticalLayout_publish.addWidget(self.label)
        self.verticalLayout_publish.addWidget(self.listWidget_pub)

    def init_connectiond(self):
        # self.pushButton_publish.clicked.connect(self.to_publish)
        self.pushButton_cancle.clicked.connect(self.close)


if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    step = 'mdl'
    aa = PreviewWidget(step=step)
    aa.show()
    sys.exit(app.exec_())
