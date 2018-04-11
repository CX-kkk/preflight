# -*- coding: utf-8 -*-
import importlib
import os
import sys
from functools import partial

import pymel.core as pm
from Qt import QtCore, QtWidgets, _loadUi, QtGui

from gui.main_pub_win import PreviewWidget
from gui import basic_gui
from core.utils import save_maya_file
from config import config


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
        self.path = config.EXPORT_PATH
        self.extend_layout()

    def extend_layout(self):
        self.listWidget_abc = basic_gui.ListWidget()
        self.extend_pub_widget.verticalLayout_abc.addWidget(self.listWidget_abc)

        assets_dict = get_simple_asset_dict()
        for abc_name in map(lambda x: x.name(), assets_dict.keys()):
            metadata = 'add info here'
            self.listWidget_abc.add_item(basic_gui.MotionItem(abc_name, enable=True, abc_option=False), metadata)

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
            save_maya_file(self.path)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    step = 'ani'
    aa = PrublishWidget(step=step)
    aa.show()
    sys.exit(app.exec_())
