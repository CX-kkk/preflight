# -*- coding: utf-8 -*

from Qt import QtCore, QtWidgets, _loadUi, QtGui


def show_message_box(title, text):
    message_box = QtWidgets.QMessageBox()
    message_box.setWindowTitle(title)
    message_box.setText(text)
    message_box.exec_()


def show_question_box(widget, title, text):
    ret = QtWidgets.QMessageBox.question(widget, title, text, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                         QtWidgets.QMessageBox.No)
    return ret


