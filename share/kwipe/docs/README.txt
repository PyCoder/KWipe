NONE-PYINSTALL VERSION:
Requirements:
Python3
PyQt5
Qt5
util-linux (lsblk)

Install & Run:
Put "kwipe" Folder somewhere
cd KWipe-*/bin
chmod +x KWipe.sh

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

PyInstaller:
One-File: python -OO -m PyInstaller -F --add-data="language:language" --add-data="icons:icons" --add-data="config:config" --add-data="Ui:Ui" --clean KWipe.py
One-Dir: python -OO -m PyInstaller -D --add-data="language:language" --add-data="icons:icons" --add-data="config:config" --add-data="Ui:Ui" --clean KWipe.py
