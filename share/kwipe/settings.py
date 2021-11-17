# settings.py
#
# Copyright (C) 2012 - 2021 Fabian Di Milia, All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author(s): Fabian Di Milia <fabian.dimilia@gmail.com>

from PyQt5 import QtWidgets
from PyQt5 import uic
import os
import sys
import utils

# Modification for PyInstaller
bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
path_to_files = os.path.abspath(os.path.join(bundle_dir))

class showSettings(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.ui = uic.loadUi(f'{path_to_files}/Ui/settings.ui', self)

        # Read config
        self.conf = utils.read_config('settings')

        # Start Functions
        self.load_algorithm()
        self.load_locked()
        self.load_general()

        # Setup Signal and Slot
        self.pushLock.clicked.connect(self.on_lock)
        self.pushUnlock.clicked.connect(self.on_unlock)
        self.buttonBox.accepted.connect(self.on_save)

    def load_algorithm(self):
        self.textAlgorithm.clear()
        with open(f'{path_to_files}/config/algorithm.conf', 'r') as f:
            self.textAlgorithm.textCursor().insertText(f.read())

    def load_locked(self):
        self.listUnlock.clear()
        self.listLock.clear()
        disks = utils.get_linux_hdd()
        for disk in disks:
            if utils.get_partition_info(disk)[1] not in self.conf['locked']:
                self.listUnlock.addItem(disk)
            else:
                self.listLock.addItem(disk)

    def load_general(self):
        self.comboLanguage.setCurrentText(self.conf['general']['language'])
        self.checkVerify.setChecked(self.conf['general'].getboolean('verify'))
        self.checkUpdate.setChecked(self.conf['general'].getboolean('update'))

    def on_lock(self):
        if self.listUnlock.selectedItems():
            device = self.listUnlock.currentItem().text()
            self.listUnlock.takeItem(self.listUnlock.currentRow())
            self.listLock.addItem(device)

    def on_unlock(self):
        if self.listLock.selectedItems():
            device = self.listLock.currentItem().text()
            self.listLock.takeItem(self.listLock.currentRow())
            self.listUnlock.addItem(device)

    def save_general_tab(self):
        # Language
        self.conf['general']['language'] = self.comboLanguage.currentText()

        ## Checkboxes
        self.conf['general']['verify'] = str(self.checkVerify.isChecked())
        self.conf['general']['update'] = str(self.checkUpdate.isChecked())

    def save_lock_tab(self):
        lock = {}
        for i in range(self.listLock.count()):
            device = self.listLock.item(i).text()
            serial = utils.get_partition_info(device)[1]
            lock[serial] = device
        self.conf['locked'] = lock

    def save_algorithm_tab(self):
        with open(f'{path_to_files}/config/algorithm.conf', 'w') as f:
            f.write(self.textAlgorithm.toPlainText())

    def on_save(self):
        # Write new config
        self.save_general_tab()
        self.save_lock_tab()
        self.save_algorithm_tab()
        utils.write_config('settings', self.conf)
        self.conf = utils.read_config('settings')

        # Reload config
        self.load_general()
        self.load_locked()
        self.load_algorithm()