# A Simple Application To View Apache's error.log file

*This program is not related to Apache or the Apache Software Foundation in any way*

## To Run:
`./apache-log-viewer.py /var/log/apache2/error.log`

*If you are using a dark theme:*
`./apache-log-viewer.py /var/log/apache2/error.log --is-dark`


## If you see something resembling the following:
```
Traceback (most recent call last):
  File "./apache-log-viewer/apache-log-viewer.py", line 3, in <module>
    from PyQt5.QtWidgets import QApplication
ModuleNotFoundError: No module named 'PyQt5'
```

then on Debian/Ubuntu/XUbuntu/Kubuntu/KDE Neon run:
`sudo apt-get install python3-pyqt5`

or on Fedora (Redhat RPM based) use pip3 instead:
```sudo pip3 install pyqt5```


...then try again.


If you see something like:
```Gtk-Message: 20:57:58.431: GtkDialog mapped without a transient parent. This is discouraged.```
or
```qt5ct: using qt5ct Plugin```
or
```Warning```
Don't worry it should still work fine though