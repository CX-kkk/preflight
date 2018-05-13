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
from core.utils import save_maya_file, get_root_dag
from config import config


class PrublishWidget(PreviewWidget):
    def __init__(self, parent=None, step=''):
        self.step = step
        super(PrublishWidget, self).__init__(parent, self.step)

    def get_export_root_path(self):
        return config.get_export_root_path(create=True)

    def export_shading_json(self, asset_name):
        path = self.get_export_root_path()
        export_shader_json(os.path.join(path, '{}.json'.format(asset_name)))

    def export_shader_mb(self, asset_name):
        print 'export shaders.'
        path = self.get_export_root_path()
        sg_path = os.path.join(path, '{}.mb'.format(asset_name))
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
            save_maya_file()

        # super(PrublishWidget, self).to_publish()
        asset_name = get_root_dag()
        if self.extend_pub_widget.checkBox_export_json.isChecked():
            self.export_shading_json(asset_name)
        if self.extend_pub_widget.checkBox_export_shaders.isChecked():
            self.export_shader_mb(asset_name)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    step = 'shd'
    aa = PrublishWidget(step=step)
    aa.show()
    sys.exit(app.exec_())
