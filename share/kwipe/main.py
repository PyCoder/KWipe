# main.py
#
# Copyright (C) 2012 - 2019  Fabian Di Milia, All rights reserved.
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

from PyQt5 import QtGui, QtCore, QtWidgets, Qt, uic
from about import showAbout
from version import VERSION, URL
from os import urandom
from datetime import datetime, timedelta
import urllib.request, urllib.error, os, binascii, subprocess, json, re

_DEBUG = False
_MEGABYTE = 1048576

class KWipe(QtWidgets.QMainWindow):
    # Algorithm
    ONE = ('00000000',)
    ZERO = ('FFFFFFFF',)
    NSA_130_2 = ('random','random')
    GOST =(ZERO[0], 'random',  'random')
    HMG_IS_5 = (ZERO[0], ONE[0], 'random')
    DOD_E = (ZERO[0], ONE[0], 'random')
    DOD_ECE = (ZERO[0], 'random', ONE[0], 'random', ZERO[0], 'random', ZERO)
    CANADIAN_OPS_II = [ZERO[0], ONE[0], ZERO[0], ONE[0], ZERO[0], ONE[0], 'random']
    VSITR = (ZERO[0], ONE[0], ZERO[0], ONE[0], ZERO[0], ONE[0], 'random')
    BRUCE_SCHNEIER = (ONE[0], ZERO[0], 'random', 'random', 'random', 'random', 'random')
    GUTMAN = ('random', 'random', 'random', 'random', '55555555', 'AAAAAAAA', '92492424', '49249292', '24924949',
           'FFFFFFFF', '11111111', '22222222', '33333333', '44444444', '55555555', '66666666', '77777777', '88888888', '99999999', 'AAAAAAAA', 'BBBBBBBB', 'CCCCCCCC',
              'DDDDDDDD', 'EEEEEEEE', '00000000', '92492424', '49249292', '24924949', '6DB6DBDB', 'B6DB6D6D', 'DB6DB6B6',
              'random', 'random', 'random', 'random')
    
    # Ugly hack dic
    control_list = {}
    
    def __init__(self):       
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('../share/Ui/kwipe.ui', self)
        
        # Start functions 
        self.check_permission()
        self.create_action_menu()
        self.create_device_tree()
        self.check_update()

        # Setup Window Title
        text = 'KWipe %s' % VERSION
        self.setWindowTitle(text)

        # Setup QComboBox, Spacer and Label
        self.comboMethod = QtWidgets.QComboBox()
        self.comboMethod.addItems(['One', 'Zero', 'NSA 130-2', 'Gost', 'HMG IS 5', 'DOD_E', 'DOD_ECE','OPS II', 'VSITR', 'Schneier', 'Gutman'])
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

        # Setup filesystem watcher for block devices
        fs_watcher = QtCore.QFileSystemWatcher(['/dev/block'], self)
        fs_watcher.directoryChanged.connect(self.create_device_tree)

    def on_erase(self):
        if self.treeWidget.currentItem():
            # Set device
            device = str(self.treeWidget.currentItem().text(0))

            if device not in self.control_list:

                # Security Question
                ret = QtWidgets.QMessageBox.warning(self, self.tr('Warning!'), self.tr('You are about to erase %s.\nAre you sure, you want to proceed?') % device, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if ret == ret == QtWidgets.QMessageBox.Yes:

                    # Remove entry if already exists
                    rows = self.tableWidget.rowCount()
                    if rows != 0:
                        for row in range(rows - 1, -1, -1):
                            if str(self.tableWidget.item(row, 0).text()) == device:
                                self.tableWidget.removeRow(row)

                    # Setup Item's
                    passItem = QtWidgets.QTableWidgetItem()
                    passItem.setTextAlignment(Qt.Qt.AlignCenter)
                    speedItem = QtWidgets.QTableWidgetItem()
                    speedItem.setTextAlignment(Qt.Qt.AlignCenter)
                    etaItem = QtWidgets.QTableWidgetItem()
                    etaItem.setTextAlignment(Qt.Qt.AlignCenter)
                    deviceItem = QtWidgets.QTableWidgetItem(device)
                    deviceItem.setTextAlignment(Qt.Qt.AlignCenter)
                    comboMethodItem = QtWidgets.QTableWidgetItem(self.comboMethod.currentText())
                    comboMethodItem.setTextAlignment(Qt.Qt.AlignCenter)

                    if self.comboMethod.currentIndex() == 0:
                        algo = self.ONE
                        passItem.setText('0/1')
                    elif self.comboMethod.currentIndex() == 1:
                        algo = self.ZERO
                        passItem.setText('0/1')
                    elif self.comboMethod.currentIndex() == 2:
                        algo = self.NSA_130_2
                        passItem.setText('0/2')
                    elif self.comboMethod.currentIndex() == 3:
                        algo = self.GOST
                        passItem.setText('0/3')
                    elif self.comboMethod.currentIndex() == 4:
                        algo = self.HMG_IS_5
                        passItem.setText('0/3')
                    elif self.comboMethod.currentIndex() == 5:
                        algo = self.DOD_E
                        passItem.setText('0/3')
                    elif self.comboMethod.currentIndex() == 6:
                        algo = self.DOD_ECE
                        passItem.setText('0/7')
                    elif self.comboMethod.currentIndex() == 7:
                        algo = self.CANADIAN_OPS_II
                        passItem.setText('0/7')
                    elif self.comboMethod.currentIndex() == 8:
                        algo = self.VSITR
                        passItem.setText('0/7')
                    elif self.comboMethod.currentIndex() == 9:
                        algo = self.BRUCE_SCHNEIER
                        passItem.setText('0/7')
                    else:
                        algo = self.GUTMAN
                        passItem.setText('0/35')

                    # Get Size
                    size = int(self.get_partition_size(device)[1])

                    # Create ProgressBar
                    progressBar = QtWidgets.QProgressBar()
                    progressBar.setRange(0, 99)

                    # Creating TableWidget Items
                    self.tableWidget.insertRow(self.tableWidget.rowCount())
                    self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, deviceItem)
                    self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, comboMethodItem)
                    self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, passItem)
                    self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, speedItem)
                    self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 4, etaItem)
                    self.tableWidget.setCellWidget(self.tableWidget.rowCount() - 1, 5, progressBar)

                    # Setup Thread and start it
                    thread = Thread(algo, device, size)
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

    def on_cancel(self):
        row = self.tableWidget.currentRow()
        if row != -1:
            device = str(self.tableWidget.item(row, 0).text())
            if self.control_list and device in self.control_list.keys():
                self.control_list[device][0].stop()

    def on_clear(self):
        rows = self.tableWidget.rowCount()
        if rows != 0:
            for row in range(rows -1, -1, -1):
                if str(self.tableWidget.item(row, 0).text()) not in self.control_list:
                    self.tableWidget.removeRow(row)

    def on_finish(self):
        for k,v in self.control_list.copy().items():
            if self.sender() == v[0]:
                if self.sender().terminated:
                    v[1].setFormat(self.tr('Aborted'))
                else:
                    v[1].setFormat(self.tr('Completed'))
                del self.control_list[k]
            
    def create_action_menu(self):
        # TreeView Menu
        erase = QtWidgets.QAction(QtGui.QIcon('../share/icons/erase.png'), self.tr('Erase'), self)
        refresh = QtWidgets.QAction(QtGui.QIcon('../share/icons/refresh.png'), self.tr('Refresh'), self)
        erase.triggered.connect(self.on_erase)
        refresh.triggered.connect(self.create_device_tree)
        self.treeWidget.addAction(erase)
        self.treeWidget.addAction(refresh)

        # TableView Menu
        cancel = QtWidgets.QAction(QtGui.QIcon('../share/icons/cancel.png'), self.tr('Cancel'), self)
        clear = QtWidgets.QAction(QtGui.QIcon('../share/icons/clear.png'), self.tr('Clear'), self)
        cancel.triggered.connect(self.on_cancel)
        clear.triggered.connect(self.on_clear)
        self.tableWidget.addAction(cancel)
        self.tableWidget.addAction(clear)

    def create_device_tree(self):
        if os.getuid() == 0:
            self.treeWidget.clear()
            devices = self.get_linux_hdd()
            item = None
            sufix=True

            for disk, parts in sorted(devices.items()):
                model, size = self.get_partition_size(disk, sufix)
                item = QtWidgets.QTreeWidgetItem([disk])
                item.setIcon(0, QtGui.QIcon('./icons/hdd.png'))
                item.setToolTip(0, self.tr('Model: %s \nDrive Size: %s') % (model, size))

                for part in parts:
                    size = self.get_partition_size(part[0], sufix)[1]
                    child = QtWidgets.QTreeWidgetItem([part[0]])
                    child.setToolTip(0, self.tr('Partition Size: %s') % size)
                    item.addChild(child)

                    if part[1]:
                        item.setDisabled(1) # Disable mounted devices?!
                self.treeWidget.addTopLevelItem(item)

    def get_linux_hdd(self):
        disks = {}
        device_list = subprocess.check_output(['lsblk -x NAME -o NAME,TYPE,MOUNTPOINT -p -r -n -e 11,1'], shell=True).decode().split('\n')
        for device in device_list:
            if device:
                device = list(filter(None, device.split(' ')))
                if device[1] == 'disk':
                    disks[device[0]] = []
                elif device[1] == 'part':
                    for key in disks.keys():
                        if key in device[0] and len(device) == 3:
                            disks[key].append((device[0], True))
                        elif key in device[0]:
                            disks[key].append((device[0], False))
        return disks

    def get_partition_size(self, device, sufix=False):
        if sufix:
            cmd = ['lsblk -o MODEL,SIZE -J %s' % device]
        else:
            cmd = ['lsblk -o MODEL,SIZE -b -J %s' % device]
        dev = json.loads(subprocess.check_output(cmd, shell=True))
        size = dev['blockdevices'][0]['size']
        model = dev['blockdevices'][0]['model']
        return model, size

    def check_update(self):
        try:
            release = urllib.request.urlopen(URL).read()[:-1].decode()
            if VERSION < release:
                QtWidgets.QMessageBox.information(self, self.tr('Update available!'),
                    self.tr('''<center><b>KWipe v%s available!</b><br>Please visit:<br>
                    <a href=https://github.com/PyCoder/KWipe> https://github.com/PyCoder/KWipe</a></center>''') % release, QtWidgets.QMessageBox.Close)
        except (urllib.error.URLError, urllib.error.HTTPError):
            pass

    def about(self):
        ab = showAbout()
        ab.exec_()
        
    def check_permission(self):
        if os.getuid() != 0:
            self.msg = QtWidgets.QMessageBox(self)   
            self.msg.setIcon(QtWidgets.QMessageBox.Information)
            self.msg.setWindowTitle(self.tr('No root permisson!'))
            self.msg.setText(self.tr('Running KWipe without root permission'))
            self.msg.addButton(QtWidgets.QMessageBox.Close)
            self.msg.setVisible(True)
            self.toolBar.setEnabled(False)

class Thread(QtCore.QThread):
    current_data = QtCore.pyqtSignal(int)
    current_pass = QtCore.pyqtSignal(str)
    current_speed = QtCore.pyqtSignal(str)
    current_eta = QtCore.pyqtSignal(str)
    finalize = QtCore.pyqtSignal(str)
    current_status_msg = QtCore.pyqtSignal(str)
    terminated = False
    
    def __init__(self, algo, device, size):
        QtCore.QThread.__init__(self)
        self.algo = algo
        self.device = device
        self.size = size
        self.semaphore = QtCore.QSemaphore(1)
   
    def run(self):
        stat = 0
        limit = int(self.size / _MEGABYTE) * _MEGABYTE
        rest = int(self.size - limit)

        with open(self.device, 'w+b') as f:
            for method in self.algo:
                if self.semaphore.available() != 0:
                    if method == 'random':
                        data = urandom(_MEGABYTE)
                        rest_data = urandom(rest)
                    else:
                        data = binascii.unhexlify(method) * 262144 # Converted to 1 MiB
                        rest_data = binascii.unhexlify(method) * int(rest / 4)

                    # start time for eta and mbps
                    start_time = datetime.now()

                    for total_bytes_written in range(0, self.size, _MEGABYTE):
                        if self.semaphore.available():

                            # Write to file/device, flush and fsync it
                            if total_bytes_written == limit and rest != 0:
                                f.write(rest_data)
                            else:
                                f.write(data)
                            f.flush()
                            os.fsync(f.fileno())

                            # DEBUG
                            if _DEBUG:
                                print('Device:', self.device, 'Size:', self.size, 'Limit:', limit, 'Rest:', rest, 'Bytes written:', total_bytes_written + _MEGABYTE)

                            # Set the offset-time
                            offset = (datetime.now() - start_time).seconds

                            # Calculate percent in python (workaround for QProgressBar qint32)
                            percent = int((total_bytes_written / self.size) * 100)
                            self.current_data.emit(percent)

                            seconds = int((self.size - total_bytes_written) / (total_bytes_written / (offset or 1))) if total_bytes_written else 0
                            eta = str(timedelta(seconds=seconds))
                            mbps = str(round(total_bytes_written / _MEGABYTE / (offset or 1), 1))
                            self.current_speed.emit(mbps)
                            self.current_eta.emit(eta)

                        else:
                            self.terminated = True
                            status_msg = self.tr('Only %s %% overwritten!') % (round(total_bytes_written / (self.size / 100), 2))
                            self.current_status_msg.emit(status_msg)
                            break

                    # Start again and emit pass
                    f.seek(0)
                    stat += 1
                    self.current_pass.emit(str(stat) + '/' + str(len(self.algo)))
                else:
                    self.terminated = True
                    break
            self.finalize.emit(self.tr('Finalize'))

    def stop(self):
        self.semaphore.acquire()
