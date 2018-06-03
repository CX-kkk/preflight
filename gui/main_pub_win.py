# -*- coding: utf-8 -*-
import importlib
import os
import sys

from Qt import QtCore, QtWidgets, _loadUi, QtGui
from hz.toolkit import start
import hz.email as email

from core.utils import save_maya_file
from extend_preflight_widget import PreflightWidget
from gui import basic_gui


class PreviewWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, step=''):
        super(PreviewWidget, self).__init__(parent)

        self.step = step
        ui_file = os.path.join(os.path.dirname(__file__), 'pub_win.ui')
        _loadUi(ui_file, self)

        self.preflight_widget = PreflightWidget(step=self.step)
        # self.pub_widget = PubWidget(step=self.step)
        step_module = importlib.import_module('check.{}.gui.extend_pub_widget'.format(self.step))
        self.extend_pub_widget = step_module.ExtendPubWidget()

        self.setWindowTitle('{} Publish Tool'.format(self.step.lower()))
        self.init_layout()
        self.init_connectiond()

    def init_layout(self):
        self.verticalLayout_publish.addWidget(self.preflight_widget)
        self.verticalLayout_publish.addWidget(self.extend_pub_widget)
        # spacerItem = QtWidgets.QSpacerItem(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # self.verticalLayout_publish.addItem(spacerItem)
        self.verticalLayout_publish.setStretch(0, 100)

        # aa = QtWidgets.QHBoxLayout()
        # aa.setStretch(0,100)

        self.setLayout(self.verticalLayout_publish.parent())


    def init_connectiond(self):
        self.pushButton_publish.clicked.connect(self.to_publish)
        self.pushButton_cancle.clicked.connect(self.close)

    def to_publish(self, foleder_path):
        if self.checkBox_auto_open_file.isChecked():
            # foleder_path = r'X:\pipelinernd_rnd-0000\_library\assets\environment\env_jojohome'
            start(foleder_path)
        if self.checkBox_auto_send_email.isChecked():
            email.send_publish_email(foleder_path)



if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    step = 'mdl'
    aa = PreviewWidget(step=step)
    aa.show()
    sys.exit(app.exec_())
