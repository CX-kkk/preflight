# -*- coding: utf-8 -*-
import importlib
import os
import sys
from Qt import QtCore, QtWidgets
from functools import partial

from check.mdl.preflight.herirachy_checking import HerirachyChecking
from config import config
from core.basci_alembic import ExportAlembic
from core.general_alembic import batch_export_alembic
from core.utils import save_maya_file
from gui.main_pub_win import PreviewWidget
from utils.export_shading_group import export_shader_json


class PrublishWidget(PreviewWidget):
    def __init__(self, parent=None, step=''):
        self.step = step
        super(PrublishWidget, self).__init__(parent, self.step)

    def export_abc_cache(self):
        print 'export_abc_cache'
        heriarchy = HerirachyChecking()
        heriarchy.asset_filter()

        abc_exporter = ExportAlembic()
        export_lod = self.extend_pub_widget.get_export_lod()
        # Get export LOD
        if export_lod == config.HIGH_GRP:
            mod_root = heriarchy.high_geo
        elif export_lod == config.MID_GRP:
            mod_root = heriarchy.mid_geo
        elif export_lod == config.LOW_GRP:
            mod_root = heriarchy.low_geo
        elif export_lod == 'all':
            mod_root = heriarchy.high_geo.rsplit('_', 1)[0]
        else:
            raise Exception('Please define LOD type in config.py first')
        # abc_file = mod_root.rsplit('_{}'.format(export_lod), 1)[0]
        print
        print 'Export mod_root: ', mod_root
        print 'Export lod: ', export_lod
        print
        self.path = config.get_export_root_path(create=True)
        abc_path = os.path.join(self.path, '{}.abc'.format(mod_root))
        batch_export_alembic(abc_exporter, mod_root, abc_path, 1, 1,
                             args={'stripNamespaces': 1, 'uvWrite': 1, 'writeVisibility': 1,
                                   'writeFaceSets': 1, 'worldSpace': 1, 'eulerFilter': 1,
                                   'step': 0.5})
        abc_exporter.batchRun()

    def export_arnold_proxy(self):
        print 'export_arnold_proxy'

    def export_cache(self, cache_type):
        if cache_type == 'radioButton_abc':
            self.export_abc_cache()
        elif cache_type == 'radioButton_arnold':
            self.export_arnold_proxy()

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
        for cache_option in self.extend_pub_widget.widget_cache.children():
            if isinstance(cache_option, QtWidgets.QRadioButton):
                if cache_option.isChecked():
                    self.export_cache(cache_option.objectName())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    step = 'mdl'
    aa = PrublishWidget(step=step)
    aa.show()
    sys.exit(app.exec_())
