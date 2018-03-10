# -*- coding: utf-8 -*-
from collections import namedtuple

from Qt import QtCore, QtWidgets, _loadUi, QtGui


WidgetData = namedtuple("WidgetData", ["widget", "metadata"])


class ListWidget(QtWidgets.QWidget):
    def __init__(self, height=30):
        super(ListWidget, self).__init__()

        self.height = height
        self.data = list()
        self.pool = QtWidgets.QListWidget()
        self.pool.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        self.init_ui()

    def __getitem__(self, index):
        clean_data = list()
        for item in self.data:
            if item.widget:
                clean_data.append(item)
        return clean_data[index]

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(self.pool)

        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def add_item(self, item, metadata=None, height=None):
        assert isinstance(item, QtWidgets.QWidget)
        list_item = QtWidgets.QListWidgetItem()
        self.data.append(WidgetData(item, metadata))
        qsize = QtCore.QSize()
        height = height if height else self.height
        qsize.setHeight(height)
        list_item.setSizeHint(qsize)
        self.pool.addItem(list_item)
        self.pool.setItemWidget(list_item, self.data[-1].widget)