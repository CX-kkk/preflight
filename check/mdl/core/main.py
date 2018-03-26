# -*- coding: utf-8 -*-
import importlib
import os
import sys
from functools import partial

from Qt import QtCore, QtWidgets, _loadUi, QtGui

from gui.main_pub_win import PreviewWidget
from check.mdl.gui.export_shading_group import export_json
from check.mdl.preflight.herirachy_checking import HerirachyChecking
from core.general_alembic import batch_export_alembic
from core.basci_alembic import ExportAlembic


class PrublishWidget(PreviewWidget):
    def __init__(self, parent=None, step=''):
        self.step = step
        super(PrublishWidget, self).__init__(parent, self.step)
        self.path = 'D:/dev/jojo/temp_test/temp'

    def export_json(self):
        export_json(os.path.join(self.path,'test.json'))

    def export_abc_cache(self):
        print 'export_abc_cache'
        heriarchy = HerirachyChecking()
        heriarchy.asset_filter()
        mod_root = heriarchy.high_geo
        abc_exporter = ExportAlembic()
        abc_file = mod_root.rsplit('_HIGH', 1)[0]
        abc_path = os.path.join(self.path, '{}.abc'.format(abc_file))
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
        super(PrublishWidget, self).to_publish()
        print 'It\'s from inheritation'
        if self.extend_pub_widget.checkBox_export_json.isChecked():
            self.export_json()
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
