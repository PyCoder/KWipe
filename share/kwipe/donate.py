# donate.py
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

# Modification for PyInstaller
bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
path_to_files = os.path.abspath(os.path.join(bundle_dir))

class showDonate(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.ui = uic.loadUi(f'{path_to_files}/Ui/donate.ui', self)

        # Setup signal and slots
        self.pushButton.clicked.connect(self.copy)

    def copy(self):
        QtWidgets.QApplication.clipboard().setText(self.lineEdit.text())