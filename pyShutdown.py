# encoding: utf8

import os
import sys
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from functools import partial


# Dark Palette
dark_palette = QtGui.QPalette()
dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(43, 43, 43))
dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(60, 63, 65))
dark_palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(190, 190, 190))
dark_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(50, 53, 55))
dark_palette.setColor(QtGui.QPalette.Text, QtGui.QColor(230, 230, 230))
dark_palette.setColor(QtGui.QPalette.Button, QtGui.QColor(60, 63, 65))
dark_palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(200, 200, 200))
dark_palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(80, 113, 135))
dark_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, QtGui.QColor(80, 80, 80))
dark_palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.white)

# Default Palette
default_palette = QtGui.QPalette()
default_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(245, 245, 245))


time_zero = QtCore.QTime(0, 0, 0)


def launch_ui():
    app = QtWidgets.QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    sys.exit(app.exec_())


class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        uic.loadUi('pysd.ui', self)

        QtWidgets.QApplication.setStyle("Fusion")
        self.setPalette(dark_palette)

        self.base_time = QtCore.QTime(2, 0, 0)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.count_down)

        self.shutdown_radioButton = self.findChild(QtWidgets.QRadioButton, 'shutdown_radioButton')
        self.hibernate_radioButton = self.findChild(QtWidgets.QRadioButton, 'hibernate_radioButton')
        self.sleep_radioButton = self.findChild(QtWidgets.QRadioButton, 'sleep_radioButton')

        self.timeEdit = self.findChild(QtWidgets.QTimeEdit, 'timeEdit')
        self.timeEdit.setTime(self.base_time)
        self.timeEdit.editingFinished.connect(self.time_edited)

        self.set_default_action = self.findChild(QtWidgets.QAction, 'actionSet_default_style')
        self.set_default_action.triggered.connect(partial(self.setPalette, default_palette))
        self.set_dark_action = self.findChild(QtWidgets.QAction, 'actionSet_dark_style')
        self.set_dark_action.triggered.connect(partial(self.setPalette, dark_palette))

        self.start_button = self.findChild(QtWidgets.QPushButton, 'start_button')
        self.start_button.clicked.connect(self.start_timer)
        self.pause_button = self.findChild(QtWidgets.QPushButton, 'pause_button')
        self.pause_button.clicked.connect(self.pause_timer)
        self.stop_button = self.findChild(QtWidgets.QPushButton, 'stop_button')
        self.stop_button.clicked.connect(self.stop_timer)

        self.donow_button = self.findChild(QtWidgets.QPushButton, 'donow_button')
        self.donow_button.clicked.connect(self.do_it)

    def do_it(self):
        func = None
        if self.shutdown_radioButton.isChecked():
            func = shutdown
        elif self.hibernate_radioButton.isChecked():
            func = hibernate
        elif self.sleep_radioButton.isChecked():
            func = sleep
        if func is not None:
            func()

    def start_timer(self):
        self.timer.start()

    def pause_timer(self):
        self.timer.stop()

    def stop_timer(self):
        self.timer.stop()
        self.timeEdit.setTime(self.base_time)

    def time_edited(self):
        self.base_time = self.timeEdit.time()

    def count_down(self):
        if self.timeEdit.time() == time_zero:
            self.timer.stop()
            self.do_it()
        else:
            self.timeEdit.setTime(self.timeEdit.time().addSecs(-1))


def sleep():
    os.system('Powercfg -H OFF')
    os.system('Rundll32.exe Powrprof.dll,SetSuspendState Sleep')


def hibernate():
    os.system('Powercfg -H ON')
    os.system('Rundll32.exe Powrprof.dll,SetSuspendState Sleep')


def shutdown():
    os.system('shutdown -s -t 0')


if __name__ == '__main__':
    launch_ui()
