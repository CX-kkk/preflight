# -*- coding: utf-8 -*-
import importlib
import os
import sys
from functools import partial

from Qt import QtCore, QtWidgets, _loadUi, QtGui

from gui.main_pub_win import PreviewWidget
from utils.export_shading_group import export_shader_json
from check.mdl.preflight.herirachy_checking import HerirachyChecking
from core.general_alembic import batch_export_alembic
from core.basci_alembic import ExportAlembic
from check.tex.core.export_shaders import export_shaders


class PrublishWidget(PreviewWidget):
    def __init__(self, parent=None, step=''):
        self.step = step
        super(PrublishWidget, self).__init__(parent, self.step)
        self.pub_widget.checkBox_source_file.setEnabled(True)
        self.pub_widget.checkBox_source_file.setChecked(True)
        self.path = 'D:/dev/jojo/temp_test/temp'


    def to_publish(self):
        super(PrublishWidget, self).to_publish()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    step = 'rig'
    aa = PrublishWidget(step=step)
    aa.show()
    sys.exit(app.exec_())
