#! /bin/bash

APPDIR=`dirname $0`

# Else, resources from the AppImage mount to $PATH, and use sandboxed
# Python3 from AppImage
export PATH="$PATH":"${APPDIR}"/usr/bin
${APPDIR}/usr/bin/python3 ${APPDIR}/opt/blue-log-viewer/blue-log-viewer.py $@