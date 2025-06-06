"""src/pkg/gui/main_window.py"""
import logging
import sys

from os import path

from PyQt5 import QtWidgets, uic

from pkg import DEBUG


logger = logging.getLogger(__name__)
# logging.getLogger("PyQt5").setLevel(logging.WARNING)

ui_file = path.join(path.dirname(__file__), 'main_window.ui')


def start_gui():
    """"""
    gui_app = QtWidgets.QApplication(sys.argv)
    window = uic.loadUi(ui_file)
    window.show()
    gui_app.exec()
