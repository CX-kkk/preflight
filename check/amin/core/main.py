# -*- coding: utf-8 -*-
import importlib
import os
import sys
from functools import partial

import pymel.core as pm
from Qt import QtCore, QtWidgets, _loadUi, QtGui

from gui.main_pub_win import PreviewWidget
from gui import basic_gui
from core.utils import save_maya_file, get_time_range_in_slider
from config import config
from core.general_alembic import batch_export_alembic
from core.basci_alembic import ExportAlembic


def get_simple_asset_dict():
    assets_dict = dict()
    asset_roots = {config.CHR_NODE, config.ENV_NODE, config.PROP_NODE, config.VEH_NODE}
    for asset_root in asset_roots:
        if pm.objExists(asset_root):
            for ref_root in pm.listRelatives(asset_root):
                high_node = '{}_{}'.format(ref_root.name(), config.HIGH_GRP)
                if pm.objExists(high_node):
                    abc_root = pm.PyNode(high_node)
                    assets_dict[ref_root] = abc_root

    return assets_dict


class PrublishWidget(PreviewWidget):
    def __init__(self, parent=None, step=''):
        self.step = step
        super(PrublishWidget, self).__init__(parent, self.step)
        self.extend_layout()

    def extend_layout(self):
        self.listWidget_abc = basic_gui.ListWidget()
        self.extend_pub_widget.verticalLayout_abc.addWidget(self.listWidget_abc)

        assets_dict = get_simple_asset_dict()
        for abc in assets_dict.keys():
            metadata = {'asset_name': abc, 'abc_root': assets_dict[abc]}
            self.listWidget_abc.add_item(basic_gui.MotionItem(abc.name(), enable=True, abc_option=False), metadata)

    def export_abc_cache(self):
        print 'export_abc_cache'
        abc_exporter = ExportAlembic()
        for each in self.listWidget_abc:
            print
            print 'Caching alembic for {}.'.format(each.metadata['asset_name'].name())
            print
            abc_file = each.metadata['asset_name'].name().replace(':', '_')
            self.path = config.get_export_root_path(create=False)
            abc_path = os.path.join(self.path, '{}.abc'.format(abc_file))
            abc_root = each.metadata['abc_root'].name()
            start_frame, end_frame = get_time_range_in_slider()
            batch_export_alembic(abc_exporter, abc_root, abc_path, start_frame, end_frame,
                                 args={'stripNamespaces': 1, 'uvWrite': 1, 'writeVisibility': 1,
                                       'writeFaceSets': 1, 'worldSpace': 1, 'eulerFilter': 1,
                                       'step': 0.5})
        abc_exporter.batchRun()

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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    step = 'amin'
    aa = PrublishWidget(step=step)
    aa.show()
    sys.exit(app.exec_())
