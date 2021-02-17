#!/usr/bin/env python3
# KWipe.py
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

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from main import KWipe
import sys
import os
import utils

# Modification for PyInstaller
bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
path_to_files = os.path.abspath(os.path.join(bundle_dir))

def loadLang():
    # from en_US to en
    system_lang = QtCore.QLocale.system().name()[:-3]
    _kwipe_trans = QtCore.QTranslator()
    _qt_trans = QtCore.QTranslator()
    for lang in utils.supported_languages():
        if system_lang == lang.split('_')[1][:-3]:
            _kwipe_trans.load(lang, path_to_files+'/language/')
    _qt_trans.load('qt_' + QtCore.QLocale.system().name(), QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath))
    return _kwipe_trans, _qt_trans

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    kwipe_trans, qt_trans = loadLang()
    app.installTranslator(kwipe_trans)
    app.installTranslator(qt_trans)
    main = KWipe()
    main.show()
    sys.exit(app.exec_())
