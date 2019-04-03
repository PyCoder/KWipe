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
- Russian Ghost p50739-95
- NSA 130-2
- Canadian OPS II 

##### Supported Language:
- English
- German
- Czech
- Romanian

##### Deps:
- Python3
- PyQt5
- util-linux (lsblk)


##### Tested with:
Recurva, Testdisk, Photorec, Ontrack Easy Recovery, Stellar Phoenix Linux Data Recovery, R-Studio 


##### INFO:
Some recovery-tools can show you a "false-positive" result on NTFS, if you wipe only the NTFS partition and not the whole disk.
This is, because tools like Recurva read the still existing MFT of NTFS! 
