#! /bin/bash

APPDIR=`dirname $0`

# This is a way that if I think the users HOST Python install can run
# the app, use that in preference to the version inside this AppImage
# that way if PyQt has deep integrations with the desktop i.e. Kvantum etc
# They will be applied, this is bending the design concept of an AppImage
# But becuase of the way PyQt works, I believe yhis is the best approach

# Don't forget to keep $@ on the end of the exec lines
# so command line args are passed down

# Simple test, if test fails will print an error to stderr, and continue running
if python3 -c "import PyQt5"; then
    # Good, use host "python3"
    python3 ${APPDIR}/opt/Densify/blue-log-viewer.py $@
else
    # Else, resources from the AppImage mount to $PATH, and use sandboxed
    # Python3 from AppImage
    export PATH="$PATH":"${APPDIR}"/usr/bin
    ${APPDIR}/usr/bin/python3 ${APPDIR}/opt/Densify/blue-log-viewer.py $@
fi