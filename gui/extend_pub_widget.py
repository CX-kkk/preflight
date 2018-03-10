# -*- coding: utf-8 -*-
import os
import sys

from Qt import QtCore, QtWidgets, _loadUi, QtGui


class PubWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, step=''):
        super(PubWidget, self).__init__(parent)
        ui_file = os.path.join(os.path.dirname(__file__), 'pub_widget.ui')
        _loadUi(ui_file, self)
        self.step = step


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    step = 'mdl'
    aa = PubWidget(step=step)
    aa.show()
    sys.exit(app.exec_())
