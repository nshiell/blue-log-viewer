# A Simple Application To View Apache's error.log file

## To Run:
`./apache-log-viewer.py /var/www/log/apache2/error.log`

*If you are using a dark theme:*
`./apache-log-viewer.py /var/www/log/apache2/log/apache2/error.log --is-dark`


## If you see something loke the following:
```
Traceback (most recent call last):
  File "./apache-log-viewer/apache-log-viewer.py", line 3, in <module>
    from PyQt5.QtWidgets import QApplication
ModuleNotFoundError: No module named 'PyQt5'
```

On Debian/Ubuntu/XUbuntu/Kubuntu/KDE Neon run:
`sudo apt-get install python3-pyqt5`

...then try again.