# -*- coding: utf-8 -*-
import os
import sys

import pymel.core as pm
from Qt import QtCore, QtWidgets, _loadUi, QtGui
from gui import basic_gui
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


class ExtendPubWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, step=''):
        super(ExtendPubWidget, self).__init__(parent)
        ui_file = os.path.join(os.path.dirname(__file__), 'extend_pub_widget.ui')
        _loadUi(ui_file, self)
        # RenderAwesomeUI(ui_file, self)
        self.step = step
        self.extend_layout()

    def extend_layout(self):
        self.listWidget_abc = basic_gui.ListWidget()
        self.verticalLayout_abc.addWidget(self.listWidget_abc)

        assets_dict = get_simple_asset_dict()
        for abc in assets_dict.keys():
            metadata = {'asset_name': abc, 'abc_root': assets_dict[abc]}
            self.listWidget_abc.add_item(basic_gui.MotionItem(abc.name(), enable=True, abc_option=False,
                                                              vray_option=False, arnold_option=False), metadata)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    step = 'anim'
    aa = ExtendPubWidget(step=step)
    aa.show()
    sys.exit(app.exec_())
