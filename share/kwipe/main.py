# main.py
#
# Copyright (C) 2012 - 2021  Fabian Di Milia, All rights reserved.
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

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import uic
from datetime import datetime, timedelta
from about import showAbout
from version import VERSION, URL
from settings import showSettings
from donate import showDonate
import urllib.request
import urllib.error
import os
import sys
import utils

# Modification for PyInstaller
bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
path_to_files = os.path.abspath(os.path.join(bundle_dir))

## TODO IMPORTANT!!!
"""
Clean the messy code!
Make make the functions shorter!!!
Rename some variables (awful names!!)
implement verify
make translations
Multi selection
Stop / Start all
"""
_DEBUG = False
_MEGABYTE = 1048576

class KWipe(QtWidgets.QMainWindow):
    # Ugly hack dic
    control_list = {}

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi(path_to_files+'/Ui/kwipe.ui', self)

        # Start functions 
        self.check_permission()
        self.create_action_menu()
        self.create_device_tree()
        self.check_update()

        # Setup Window Title
        text = 'KWipe {}'.format(VERSION)
        self.setWindowTitle(text)

        # Setup QComboBox, Spacer and Label
        self.comboMethod = QtWidgets.QComboBox()
        self.comboMethod.addItems(utils.read_config('algorithm').sections())
        spacer = QtWidgets.QWidget(self.toolBar)
        spacer.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        self.toolBar.addWidget(spacer)
        labelMethod = QtWidgets.QLabel(self.tr('Method: '), self.toolBar)
        self.toolBar.addWidget(labelMethod)
        self.toolBar.addWidget(self.comboMethod)

        # Setup Signal and Slot
        self.action_erase.triggered.connect(self.on_erase)
        self.action_cancel.triggered.connect(self.on_cancel)
        self.action_refresh.triggered.connect(self.create_device_tree)
        self.action_clear.triggered.connect(self.on_clear)
        self.action_about.triggered.connect(self.about)
        self.action_settings.triggered.connect(self.settings)
        self.action_donate.triggered.connect(self.donate)

        # Setup filesystem watcher for block devices
        fs_watcher = QtCore.QFileSystemWatcher(['/dev/block', path_to_files+'/config/settings.conf', path_to_files+'/config/algorithm.conf'], self)
        fs_watcher.directoryChanged.connect(self.reload_config)
        fs_watcher.fileChanged.connect(self.reload_config)

    def reload_config(self):
        self.create_device_tree()
        self.create_combobox()

    def create_combobox(self):
        self.comboMethod.clear()
        self.comboMethod.addItems(utils.read_config('algorithm').sections())

    def on_erase(self):
        if self.deviceTableWidget.currentRow() >= 0:
            device = self.deviceTableWidget.item(self.deviceTableWidget.currentRow(), 0).text()
            serial = self.deviceTableWidget.item(self.deviceTableWidget.currentRow(), 2).text()

            # Check if the device is protected ## TODO ugly should be its own function!
            if serial not in utils.read_config('settings')['locked']:
                if device not in self.control_list:
                    # Security Question
                    ret = QtWidgets.QMessageBox.warning(self, self.tr('Warning!'),
                                                        self.tr('You are about to erase %s.\n'
                                                                'Are you sure, you want to proceed?') % device,
                                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                    if ret == QtWidgets.QMessageBox.Yes:
                        # Remove entry if already exists
                        rows = self.workTableWidget.rowCount()
                        if rows != 0:
                            for row in range(rows - 1, -1, -1):
                                if str(self.workTableWidget.item(row, 0).text()) == device:
                                    self.workTableWidget.removeRow(row)

                        # Setup algo and rounds  ## TODO ugly should be its own function!
                        if serial in utils.read_config('resume').sections():
                            resume = QtWidgets.QMessageBox.question(self, self.tr('Resume?'), self.tr('Do you wanna resume the last job?'), QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                            if resume == QtWidgets.QMessageBox.Yes:
                                algo, pattern, current_round, position, diff_offset = self.resume_status(serial, True)
                            else:
                                algo, pattern, current_round, position, diff_offset = self.resume_status(serial, False)
                                self.remove_status(serial)
                        else:
                            algo, pattern, current_round, position, diff_offset = self.resume_status(serial, False)

                        # Setup Item's
                        passItem = QtWidgets.QTableWidgetItem()
                        passItem.setText('{}/{}'.format(current_round, len(pattern)))
                        speedItem = QtWidgets.QTableWidgetItem()
                        etaItem = QtWidgets.QTableWidgetItem()
                        deviceItem = QtWidgets.QTableWidgetItem(device)
                        comboMethodItem = QtWidgets.QTableWidgetItem(algo)

                        # Get Size
                        size = utils.get_partition_info(device)[2]

                        # Create ProgressBar
                        progressBar = QtWidgets.QProgressBar()
                        progressBar.setRange(0, 99)

                        # Creating TableWidget Items ## TODO use a list and for loop with enumerate?
                        self.workTableWidget.insertRow(self.workTableWidget.rowCount())
                        self.workTableWidget.setItem(self.workTableWidget.rowCount() - 1, 0, deviceItem)
                        self.workTableWidget.setItem(self.workTableWidget.rowCount() - 1, 1, comboMethodItem)
                        self.workTableWidget.setItem(self.workTableWidget.rowCount() - 1, 2, passItem)
                        self.workTableWidget.setItem(self.workTableWidget.rowCount() - 1, 3, speedItem)
                        self.workTableWidget.setItem(self.workTableWidget.rowCount() - 1, 4, etaItem)
                        self.workTableWidget.setCellWidget(self.workTableWidget.rowCount() - 1, 5, progressBar)

                        # Setup Thread and start it
                        thread = Thread(pattern, device, size, current_round,position, diff_offset, verify=False) ## TODO verify
                        thread.start()
                        thread.setPriority(0)

                        # Signal and Slots
                        thread.finished.connect(self.on_finish)
                        thread.current_data.connect(progressBar.setValue)
                        thread.finalize.connect(progressBar.setFormat)
                        thread.current_pass.connect(passItem.setText)
                        thread.current_speed.connect(speedItem.setText)
                        thread.current_eta.connect(etaItem.setText)
                        thread.current_status_msg.connect(progressBar.setToolTip)

                        # Save Pointers to control QThread
                        self.control_list[device] = (thread, progressBar)

                        # Get item from status and change it from ready to running!
                        activity = self.deviceTableWidget.item(self.deviceTableWidget.currentRow(), 4)
                        activity.setText(self.tr('running'))
                        activity.setForeground(QtGui.QBrush(QtGui.QColor('green')))
            else:
                QtWidgets.QMessageBox.warning(self, self.tr('Warning!'), self.tr('Please unlock device first.'), QtWidgets.QMessageBox.Ok)

    def resume_status(self, serial, resume=True):
        if resume:
            conf = utils.read_config('resume')
            algo = conf[serial]['algo']
            pattern = utils.read_config('algorithm')[algo]['pattern'].split(',')
            current_round = conf[serial].getint('round')
            position = conf[serial].getint('position')
            diff_offset = conf[serial].getint('offset')
        else:
            algo = self.comboMethod.currentText()
            pattern = utils.read_config('algorithm')[self.comboMethod.currentText()]['pattern'].split(',')
            current_round = 0
            position = 0
            diff_offset = 0
        return algo, pattern, current_round, position, diff_offset

    def save_status(self, device, algo, current_round, position, offset):
        conf = utils.read_config('resume')
        serial = utils.get_partition_info(device)[1]
        conf[serial] = {'algo': algo,
                        'round': current_round,
                        'position': position,
                        'offset': offset}
        utils.write_config('resume', conf)

    def remove_status(self, serial):
        conf = utils.read_config('resume')
        if serial in conf.sections():
            del conf[serial]
            utils.write_config('resume', conf)

    def on_cancel(self):
        row = self.workTableWidget.currentRow()
        if row != -1:
            device = str(self.workTableWidget.item(row, 0).text())
            if self.control_list and device in self.control_list.keys():
                self.control_list[device][0].stop()
                self.save_status(device,
                                 str(self.workTableWidget.item(row, 1).text()),
                                 self.control_list[device][0].current_round,
                                 self.control_list[device][0].position,
                                 self.control_list[device][0].offset)
    def on_clear(self):
        rows = self.workTableWidget.rowCount()
        if rows != 0:
            for row in range(rows -1, -1, -1):
                if str(self.workTableWidget.item(row, 0).text()) not in self.control_list:
                    self.workTableWidget.removeRow(row)

    def on_verify(self):
        pass ## TODO has to be implemented!

    def on_finish(self):
        for k, v in self.control_list.copy().items():
            if self.sender() == v[0]:
                if self.sender().terminated:
                    v[1].setFormat(self.tr('Aborted'))
                else:
                    v[1].setFormat(self.tr('Completed'))
                    serial = utils.get_partition_info(k)[1]
                    self.remove_status(serial)
                del self.control_list[k]


    def create_action_menu(self):
        # TreeView Menu
        erase = QtWidgets.QAction(QtGui.QIcon(path_to_files+'/icons/erase.png'), self.tr('Erase'), self)
        refresh = QtWidgets.QAction(QtGui.QIcon(path_to_files+'/icons/refresh.png'), self.tr('Refresh'), self)
        erase.triggered.connect(self.on_erase)
        refresh.triggered.connect(self.create_device_tree)
        self.deviceTableWidget.addAction(erase)
        self.deviceTableWidget.addAction(refresh)

        # TableView Menu
        cancel = QtWidgets.QAction(QtGui.QIcon(path_to_files+'/icons/cancel.png'), self.tr('Cancel'), self)
        clear = QtWidgets.QAction(QtGui.QIcon(path_to_files+'/icons/clear.png'), self.tr('Clear'), self)
        cancel.triggered.connect(self.on_cancel)
        clear.triggered.connect(self.on_clear)
        self.workTableWidget.addAction(cancel)
        self.workTableWidget.addAction(clear)

    def create_device_tree(self): ## TODO rename _items and _item
        if os.getuid() == 0:
            self.deviceTableWidget.clearContents()
            self.deviceTableWidget.setRowCount(0)
            devices = utils.get_linux_hdd()
            _bytes = True

            for disk in devices:
                self.deviceTableWidget.insertRow(self.deviceTableWidget.rowCount())
                _items = list(utils.get_partition_info(disk, _bytes))
                _items.insert(0,disk)
                for column, item in enumerate(_items):
                    _item = QtWidgets.QTableWidgetItem()
                    _item.setText(str(item))
                    self.deviceTableWidget.setItem(self.deviceTableWidget.rowCount() - 1, column, _item)

                activity = QtWidgets.QTableWidgetItem()
                if utils.get_partition_info(disk)[1] in utils.read_config('settings')['locked']:
                    activity.setText(self.tr('locked'))
                    activity.setForeground(QtGui.QBrush(QtGui.QColor('red')))
                elif disk in self.control_list.keys():
                    activity.setText(self.tr('running'))
                    activity.setForeground(QtGui.QBrush(QtGui.QColor('green')))
                else:
                    activity.setText(self.tr('ready'))
                self.deviceTableWidget.setItem(self.deviceTableWidget.rowCount() - 1, 4, activity)

                # Changing width of the column for model and serial
                self.deviceTableWidget.setColumnWidth(1,200)
                self.deviceTableWidget.setColumnWidth(2,200)

    def check_update(self):
        if utils.read_config('settings')['general'].getboolean('update'):
            try:
                release = urllib.request.urlopen(URL).read()[:-1].decode()
                if VERSION < release:
                    QtWidgets.QMessageBox.information(self, self.tr('Update available!'),
                                                      self.tr('''<center><b>KWipe v{} available!</b><br>Please visit:<br>
                                                  <a href=https://github.com/PyCoder/KWipe>
                                                  https://github.com/PyCoder/KWipe</a></center>''').format(release),
                                                      QtWidgets.QMessageBox.Close)
            except (urllib.error.URLError, urllib.error.HTTPError):
                pass

    def donate(self):
        d = showDonate()
        d.exec()

    def about(self):
        ab = showAbout()
        ab.exec_()

    def settings(self):
        settings = showSettings()
        settings.exec_()

    def check_permission(self):
        if os.getuid() != 0:
            self.msg = QtWidgets.QMessageBox(self)
            self.msg.setIcon(QtWidgets.QMessageBox.Information)
            self.msg.setWindowTitle(self.tr('No root permission!'))
            self.msg.setText(self.tr('Running KWipe without root permission'))
            self.msg.addButton(QtWidgets.QMessageBox.Close)
            self.msg.setVisible(True)
            self.toolBar.setEnabled(False)
            self.menuBar.setEnabled(False)

class Thread(QtCore.QThread):
    current_data = QtCore.pyqtSignal(int)
    current_pass = QtCore.pyqtSignal(str)
    current_speed = QtCore.pyqtSignal(str)
    current_eta = QtCore.pyqtSignal(str)
    current_status_msg = QtCore.pyqtSignal(str)
    finalize = QtCore.pyqtSignal(str)
    terminated = False

    def __init__(self, algo, device, size, current_round, position, diff_offset, verify): ## TODO verify
        QtCore.QThread.__init__(self)
        self.algo = algo
        self.device = device
        self.size = size
        self.current_round = current_round
        self.position = position
        self.diff_offset = diff_offset
        self.verify = verify
        self.semaphore = QtCore.QSemaphore(1)

    def run(self):
        limit = int(self.size / _MEGABYTE) * _MEGABYTE
        rest = int(self.size - limit)

        with open(self.device, 'r+b') as f:
            f.seek(self.position)
            for method in self.algo[self.current_round:]:
                if self.semaphore.available() != 0:
                    data = utils.prepare_data(method, _MEGABYTE)
                    rest_data = utils.prepare_data(method, rest)

                    # start time for eta and mbps and correction in case if we resume!
                    start_time = datetime.now() - timedelta(seconds=self.diff_offset)

                    for total_bytes_written in range(self.position, self.size, _MEGABYTE):
                        if self.semaphore.available():

                            # Write to file/device, flush and fsync it
                            if total_bytes_written == limit and rest !=0:
                                f.write(rest_data)
                            else:
                                f.write(data)
                            f.flush()
                            os.fsync(f.fileno())

                            # DEBUG
                            if _DEBUG:
                                print('Device:', self.device, 'Size:', self.size, 'Bytes written:', total_bytes_written + _MEGABYTE, 'Position of FP:', f.tell())

                            # Set the offset-time
                            self.offset = (datetime.now() - start_time).seconds

                            # Calculate percent in python (workaround for QProgressBar qint32)
                            percent = int((total_bytes_written / self.size) * 100)
                            self.current_data.emit(percent)

                            seconds = int((self.size - total_bytes_written) / (total_bytes_written / (self.offset or 1))) if total_bytes_written else 0
                            eta = str(timedelta(seconds=seconds))
                            mbps = str(round(total_bytes_written / _MEGABYTE / (self.offset or 1), 1))
                            self.current_speed.emit(mbps)
                            self.current_eta.emit(eta)
                            self.position = f.tell()
                        else:
                            self.terminated = True
                            status_msg = self.tr('Only %s %% overwritten!') % (round(total_bytes_written / (self.size / 100), 2))
                            self.current_status_msg.emit(status_msg)
                            break

                    # Start again and emit pass
                    f.seek(0)
                    if not self.terminated: ## Workaround for the moment
                        self.position = 0
                    self.current_round += 1
                    self.current_pass.emit(str(self.current_round) + '/' + str(len(self.algo)))
                else:
                    self.terminated = True
                    break
            self.finalize.emit(self.tr('Finalize'))
    def stop(self):
        self.semaphore.acquire()
