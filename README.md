# KWipe
### KWipe is a secure erase (wipe) application, completely written in PyQt5!

Video: https://www.youtube.com/watch?v=bXG-aEDUNXc

##### Supported Wipe-Modes:
- One
- Zero
- DOD
- DOD-E
- VSITR
- Gutman
- Bruce Schneier
- Britisch HMG Standard 5
- Russian Gost p50739-95
- NSA 130-2
- Canadian OPS II 

##### Supported Language:
- English
- German
- Czech
- Romanian
- Russian

##### Deps:
- Python3
- PyQt5
- util-linux (lsblk)


##### Tested with:
Recurva, Testdisk, Photorec, Ontrack Easy Recovery, Stellar Phoenix Linux Data Recovery, R-Studio 


##### INFO:
Some recovery tools can show you a "false-positive" result, caused by the still existing MFT if you only overwrite the partition and not the whole disk!

### Known issues
The settings and help entry in the menu is not working cause I didn't implement it rn.
