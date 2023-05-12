NONE-PYINSTALLER VERSION:
Requirements:
Python3
PyQt6
Qt6
util-linux (lsblk)
directio

Install & Run:
Put "kwipe" Folder somewhere
cd KWipe-*/bin
chmod +x KWipe.sh

On most desktops run:
pkexec ./KWipe.sh

On KDE run:
kdesu ./Kwipe.sh

On Gnome/Unity run:
gksu ./Kwipe.sh

With sudo:
sudo ./KWipe.sh

Without kdesu/gksu/sudo run:
su -c ./KWipe.sh

PYINSTALL VERSION:
Requirements:
All built-in

Install & Run:
chmod +x KWipe

On most desktops run:
pkexec ./KWipe.sh

On KDE run:
kdesu ./Kwipe

On Gnome/Unity run:
gksu ./Kwipe

With sudo:
sudo ./KWipe

Without kdesu/gksu/sudo run:
su -c ./KWipe

INFORMATION:

Algorithm's:
http://www.killdisk.com/notes.htm

### Build Instructions wiht PyInstaller
Instructions to build your own packages with PyInstaller.

1) git-clone https://github.com/PyCoder/KWipe.git
2) pip3 install pyqt6 pyinstaller directio
3) Navigate to /share/kwipe/ where KWipe.py is located
4) python3 -OO -m PyInstaller -D --add-data="language:language" --add-data="icons:icons" --add-data="config:config" --add-data="Ui:Ui" --add-data="docs:docs" --clean KWipe.py

PyInstaller information:
One-File: python3 -OO -m PyInstaller -F --add-data="language:language" --add-data="icons:icons" --add-data="config:config" --add-data="Ui:Ui" --add-data="docs:docs" --clean KWipe.py
One-Dir: python3 -OO -m PyInstaller -D --add-data="language:language" --add-data="icons:icons" --add-data="config:config" --add-data="Ui:Ui" --add-data="docs:docs" --clean KWipe.py
