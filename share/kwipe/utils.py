# utils.py
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

import subprocess
import configparser
import json
import os
import sys
import fnmatch
import binascii
import textwrap

# Modification for PyInstaller
bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
path_to_files = os.path.abspath(os.path.join(bundle_dir))

def get_linux_hdd():
    disks = []
    device_list = json.loads(subprocess.check_output(['lsblk -J -d -o NAME,MOUNTPOINT -e 11,1,252'],
                                          shell=True))['blockdevices']
    for device in device_list:
        disks.append('/dev/'+device['name'])
    return disks

def get_partition_info(device, _bytes=False):
    if _bytes:
        cmd = ['lsblk -o MODEL,SIZE,SERIAL,NAME -J ' + device]
    else:
        cmd = ['lsblk -o MODEL,SIZE,SERIAL,NAME -b -J ' + device]
    dev = json.loads(subprocess.check_output(cmd, shell=True))
    model = dev['blockdevices'][0]['model']
    serial = dev['blockdevices'][0]['serial']
    size = dev['blockdevices'][0]['size']
    return model, serial, size

def read_config(file):
    conf = configparser.ConfigParser()
    conf.read(path_to_files+'/config/'+file+'.conf')
    return conf

def write_config(file, conf):
    with open(path_to_files+'/config/'+file+'.conf', 'w') as configfile:
        conf.write(configfile)

def load_default_language():
    default = read_config('settings')['language']
    return default

def supported_languages():
    lang = sorted(fnmatch.filter(os.listdir(path_to_files+'/language/'), '*.qm'))
    return lang

def prepare_data(method, size):
    if method == 'random':
        data = os.urandom(size)
    else:
        hex_data = textwrap.wrap(method, 2)
        data = ''
        c = 0
        for byte in range(size):
            data += hex_data[c]
            c += 1
            if c == len(hex_data):
                c = 0
        data = binascii.unhexlify(data)
    return data