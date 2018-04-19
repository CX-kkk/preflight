# -*- coding: utf-8 -*-
import os
import sys

from Qt import QtCore, QtWidgets, _loadUi, QtGui
from core.utils import get_all_cameras


class ExtendPubWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, step=''):
        super(ExtendPubWidget, self).__init__(parent)
        ui_file = os.path.join(os.path.dirname(__file__), 'extend_pub_widget.ui')
        _loadUi(ui_file, self)
        self.step = step
        self.init_connections()
        self.reload_camera()

    def init_connections(self):
        self.checkBox_export_camera.clicked.connect(self.camera_enable)
        self.checkBox_export_abc.clicked.connect(self.abc_enable)

    def camera_enable(self):
        enable = self.checkBox_export_camera.isChecked()
        self.widget_camera.setEnabled(enable)

    def abc_enable(self):
        enable = self.checkBox_export_abc.isChecked()
        self.widget_cache.setEnabled(enable)

    def load_camera(self):
        cams = get_all_cameras()
        cams = cams if cams else ['------None------']
        self.comboBox_camera.addItems(cams)

    def reload_camera(self):
        self.comboBox_camera.clear()
        self.load_camera()




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    step = 'tex'
    aa = ExtendPubWidget(step=step)
    aa.show()
    sys.exit(app.exec_())
