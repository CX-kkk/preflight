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
        self.path = config.get_export_root_path(create=True)

    def export_shading_json(self):
        export_shader_json(os.path.join(self.path, 'shader_tex.json'))

    def export_shader_mb(self):
        print 'export shaders.'
        sg_path = os.path.join(self.path, 'shaders_tex.mb')
        export_shaders(sg_path)

    def export_abc_cache(self):
        print 'export abc cache'
        heriarchy = HerirachyChecking()
        heriarchy.asset_filter()
        mod_root = heriarchy.high_geo
        abc_exporter = ExportAlembic()
        abc_file = mod_root.rsplit('_{}'.format(config.HIGH_GRP), 1)[0]
        abc_path = os.path.join(self.path, '{}_tex.abc'.format(abc_file))
        batch_export_alembic(abc_exporter, abc_file, abc_path, 1, 1,
                             args={'stripNamespaces': 1, 'uvWrite': 1, 'writeVisibility': 1,
                                   'writeFaceSets': 1, 'worldSpace': 1, 'eulerFilter': 1,
                                   'step': 0.5})
        abc_exporter.batchRun()

    def export_arnold_proxy(self):
        print 'export_arnold_proxy'

    def export_vray_proxy(self):
        print 'export_vray_proxy'

    def export_cache(self, cache_type):
        if cache_type == 'radioButton_abc':
            self.export_abc_cache()
        elif cache_type == 'radioButton_arnold':
            self.export_arnold_proxy()
        elif cache_type == 'radioButton_vray':
            self.export_vray_proxy()

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
        for cache_option in self.extend_pub_widget.widget_cache.children():
            if isinstance(cache_option, QtWidgets.QRadioButton):
                if cache_option.isChecked():
                    self.export_cache(cache_option.objectName())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    step = 'shd'
    aa = PrublishWidget(step=step)
    aa.show()
    sys.exit(app.exec_())
