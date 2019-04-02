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


Algorithm's:
http://www.killdisk.com/notes.htm


Known Bugs:
Plug-in and replug-in may cause an error in ETA calculation. I'll fix it asap.
