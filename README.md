# KWipe 3.0
### KWipe is a secure erase (wipe) application, completely written in PyQt5!

![KWipe 3.0.0](https://github.com/PyCoder/KWipe/blob/master/screenshots/main.png?raw=true)

### [Donate via PayPal](https://www.paypal.com/donate?business=BRYVTAQ95YPNU&currency_code=USD)
### Donation in Bitcoin:
![3EiDHWZewRv4WUwbyLyBQMzGvqksPYh7VT](https://github.com/PyCoder/KWipe/blob/master/share/kwipe/icons/qr.png?raw=true)

### [3.0 Released with new features!](https://github.com/PyCoder/KWipe/releases/download/3.0.3/KWipe-3.0.3.tar.gz)

#### New features:
- Pause and resume
- Protect devices
- Edit algorithms
- Ui update
- Code update
- Prepared for PyInstaller

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
- PyQt5
- util-linux (lsblk)


##### Tested with:
Recurva, Testdisk, Photorec, Ontrack Easy Recovery, Stellar Phoenix Linux Data Recovery, R-Studio 

##### TODO:
- Implement verify (settings)
- Implement change language (settings)
- Clean messy code
- Fix workaround for self.position
- Fix crash if there is no serial number (Workaround remove maj 7 from lsblk)
- Make package with flatpak
