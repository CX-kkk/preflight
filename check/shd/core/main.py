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
from check.shd.core.export_shaders import export_shaders
from core.utils import save_maya_file
from config import config


class PrublishWidget(PreviewWidget):
    def __init__(self, parent=None, step=''):
        self.step = step
        super(PrublishWidget, self).__init__(parent, self.step)

    def get_export_root_path(self):
        return config.get_export_root_path(create=True)

    def export_shading_json(self):
        path = self.get_export_root_path()
        export_shader_json(os.path.join(path, 'shader.json'))

    def export_shader_mb(self):
        print 'export shaders.'
        path = self.get_export_root_path()
        sg_path = os.path.join(path, 'shaders.mb')
        export_shaders(sg_path)

    def to_publish(self):
        if self.extend_pub_widget.checkBox_preflight.isChecked():
            print 'preflight'
            for child in self.preflight_widget.listWidget_preflight.data:
                print '--------------------'
                print child, dir(child)
                for cb in child.widget.children():
                    if isinstance(cb, QtWidgets.QCheckBox):
                        print cb.isChecked()
                        print cb.objectName()
        if self.extend_pub_widget.checkBox_source_file.isChecked():
            # TODO: get export path
            save_maya_file()

        # super(PrublishWidget, self).to_publish()
        if self.extend_pub_widget.checkBox_export_json.isChecked():
            self.export_shading_json()
        if self.extend_pub_widget.checkBox_export_shaders.isChecked():
            self.export_shader_mb()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    step = 'shd'
    aa = PrublishWidget(step=step)
    aa.show()
    sys.exit(app.exec_())
