# -*- coding: utf-8 -*-
import importlib
import os
import sys
from functools import partial

from Qt import QtCore, QtWidgets, _loadUi, QtGui

from gui.main_pub_win import PreviewWidget
from core.utils import save_maya_file
from config import config

class PrublishWidget(PreviewWidget):
    def __init__(self, parent=None, step=''):
        self.step = step
        super(PrublishWidget, self).__init__(parent, self.step)
        # self.pub_widget.checkBox_source_file.setEnabled(True)
        # self.pub_widget.checkBox_source_file.setChecked(True)
        # self.pub_widget.checkBox_source_file.setText('Export Rigging file')
        self.path = config.get_export_root_path(create=True)


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



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    step = 'rig'
    aa = PrublishWidget(step=step)
    aa.show()
    sys.exit(app.exec_())
