# KWipe 3.1.3
### KWipe is a secure erase (wipe) application, completely written in PyQt!

![KWipe 3.1.0](https://github.com/PyCoder/KWipe/blob/master/screenshots/difference.png?raw=true)

#### New features:
- Improved write speed up to 4x
- Ported to PyQt6
- Pause and resume
- Protect devices
- Edit algorithms
- Ui update
- Code update

##### Supported Wipe-Modes:
- One
- Zero
- DOD
- DOD-E
- VSITR
- Gutmann 35 
- Gutmann short
- Bruce Schneier
- Britisch HMG Standard 5
- Russian Gost p50739-95
- NSA 130-2
- Canadian OPS II 

##### Supported Language:
- English

##### Deps:
- Python3
- PyQt6
- util-linux (lsblk)
- directio

##### Tested with:
Recurva, Testdisk, Photorec, Ontrack Easy Recovery, Stellar Phoenix Linux Data Recovery, R-Studio 

##### TODO:
- Implement verify (settings)
- Implement change language (settings)
- Clean messy code
- Fix workaround for self.position
- ~~Make package with flatpak~~ (Not possible without breaking sandbox)
- Create kwipe.desktop with PKExec
- ~~Add option to show/hide row headers~~
- Switch to udev/dbus
- Update dated UI

