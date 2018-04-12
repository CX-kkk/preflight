# -*- coding: utf-8 -*-
import os
import sys

from Qt import QtCore, QtWidgets, _loadUi, QtGui
from hz.awesome_ui.widgets import RenderAwesomeUI


class ExtendPubWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, step=''):
        super(ExtendPubWidget, self).__init__(parent)
        ui_file = os.path.join(os.path.dirname(__file__), 'extend_pub_widget.ui')
        # _loadUi(ui_file, self)
        RenderAwesomeUI(ui_file, self)
        self.step = step


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    step = 'mdl'
    aa = ExtendPubWidget(step=step)
    aa.show()
    sys.exit(app.exec_())
