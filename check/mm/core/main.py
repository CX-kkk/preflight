# -*- coding: utf-8 -*-
import os
import sys

import pymel.core as pm
from Qt import QtCore, QtWidgets, _loadUi, QtGui

from core.basci_alembic import ExportAlembic
from core.general_alembic import batch_export_alembic
from core.utils import save_maya_file
from gui.main_pub_win import PreviewWidget
from gui import msg_box
from config import config


class PrublishWidget(PreviewWidget):
    def __init__(self, parent=None, step=''):
        self.step = step
        super(PrublishWidget, self).__init__(parent, self.step)
        self.path = config.get_export_root_path(create=True)

    def export_abc_cache(self):
        print 'export abc cache'
        abc_exporter = ExportAlembic()
        abc_file = pm.ls(sl=True)
        if len(abc_file) == 0:
            warning_text = 'You haven\'t select any objects to export. go on?'
            result = msg_box.show_question_box(self, 'Warning', warning_text)
            if not result:
                return
        elif len(abc_file) == 1:
            pass
        else:
            warning_text = 'You selected {0} objects, it\'ll gonna export {0} abc files, go on?'.format(str(len(abc_file)))
            result = msg_box.show_question_box(self, 'Warning', warning_text)
            if not result:
                return
        for each in abc_file:
            abc_path = os.path.join(self.path, '{}.abc'.format(each.replace(':','_')))
            batch_export_alembic(abc_exporter, each, abc_path, 1, 1,
                                 args={'stripNamespaces': 1, 'uvWrite': 1, 'writeVisibility': 1,
                                       'writeFaceSets': 1, 'worldSpace': 1, 'eulerFilter': 1,
                                       'step': 0.5})
            abc_exporter.batchRun()

    def export_cache(self, cache_type):
        if cache_type == 'radioButton_abc_from_selection':
            self.export_abc_cache()
        elif cache_type == 'radioButton_abc_from_heriarchy':
            pass

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
        for cache_option in self.extend_pub_widget.widget_cache.children():
            if isinstance(cache_option, QtWidgets.QRadioButton):
                if cache_option.isChecked():
                    self.export_cache(cache_option.objectName())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    step = 'mm'
    aa = PrublishWidget(step=step)
    aa.show()
    sys.exit(app.exec_())
