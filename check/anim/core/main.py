# -*- coding: utf-8 -*-
import importlib
import os
import sys
from Qt import QtCore, QtWidgets, _loadUi, QtGui
from functools import partial

import pymel.core as pm

from config import config
from core.basci_alembic import ExportAlembic
from core.general_alembic import batch_export_alembic
from core.utils import save_maya_file, get_time_range_in_slider, write_out_json
from gui.main_pub_win import PreviewWidget


class PrublishWidget(PreviewWidget):
    def __init__(self, parent=None, step=''):
        self.step = step
        super(PrublishWidget, self).__init__(parent, self.step)

    def export_abc_cache(self):
        print 'export_abc_cache'
        abc_exporter = ExportAlembic()
        for each in self.extend_pub_widget.listWidget_abc:
            print
            print 'Caching alembic for {}.'.format(each.metadata['asset_name'].name())
            print
            abc_file = each.metadata['asset_name'].name().replace(':', '_')
            self.path = config.get_export_root_path(create=True)
            abc_path = os.path.join(self.path, '{}.abc'.format(abc_file))
            abc_root = each.metadata['abc_root'].name()
            start_frame, end_frame = get_time_range_in_slider()
            batch_export_alembic(abc_exporter, abc_root, abc_path, start_frame, end_frame,
                                 args={'stripNamespaces': 1, 'uvWrite': 1, 'writeVisibility': 1,
                                       'writeFaceSets': 1, 'worldSpace': 1, 'eulerFilter': 1,
                                       'step': 0.5})
        abc_exporter.batchRun()

    def get_reference_dict(self):
        asset_dict = {}
        for ref in pm.ls(rf=True):
            asset_name = ref.referenceFile().getReferenceEdits()[0].split(':')[1].split('"')[0]
            if asset_name not in asset_dict.keys():
                asset_dict[asset_name] = {}
            asset_dict[asset_name][ref.shortName()] = str(ref.referenceFile().path)
        return asset_dict

    def to_publish(self):
        if self.extend_pub_widget.checkBox_preflight.isChecked():
            print 'Doing preflight'
            for child in self.preflight_widget.listWidget_preflight.data:
                for cb in child.widget.children():
                    if isinstance(cb, QtWidgets.QCheckBox):
                        print cb.isChecked()
                        print cb.objectName()
        if self.extend_pub_widget.checkBox_source_file.isChecked():
            # TODO: get export path
            save_maya_file()

        if self.extend_pub_widget.checkBox_export_abc.isChecked():
            print 'Starting cache alembic...'
            self.export_abc_cache()
            print 'Alembic caches done!'

        # write out json file for lgt import tool
        asset_dict = self.get_reference_dict()
        write_out_json(file_path=os.path.join(self.path, 'rigging_info.json'), dict=asset_dict)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    step = 'anim'
    aa = PrublishWidget(step=step)
    aa.show()
    sys.exit(app.exec_())
