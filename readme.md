# A Simple Application To View Apache's error.log file

![Log Viewer - Main Window](https://nshiell.com/img/blue-log-viewer/product-ubuntu-v1-2-0.png)

*This program is not related to Apache or the Apache Software Foundation in any way*

## To Run on GNU/Linux:
`./blue-log-viewer.py /var/log/apache2/error.log`

#### If you see something resembling the following:
```
Traceback (most recent call last):
  File "./blue-log-viewer.py", line 3, in <module>
    from PyQt5.QtWidgets import QApplication
ModuleNotFoundError: No module named 'PyQt5'
```

##### then on Debian / Ubuntu / XUbuntu / Kubuntu / KDE Neon run:
`sudo apt-get install python3-pyqt5`

##### or on Fedora (Redhat RPM based) use pip3 instead:
```sudo pip3 install pyqt5```


...then try again.

_______________________________________________________

## To Run on Mac OSX:
![Log Viewer - Main Window](https://nshiell.com/img/blue-log-viewer/product-osx-v1-2-0.png)
I use https://brew.sh/ to get it to install - you can try pip3 etc

`python3.7 blue-log-viewer.py`

#### If you see something resembling the following:
```
Traceback (most recent call last):
  File "./blue-log-viewer.py", line 3, in <module>
    from PyQt5.QtWidgets import QApplication
ModuleNotFoundError: No module named 'PyQt5'
```
##### Then run
```brew install pyqt5```

...then try again.
