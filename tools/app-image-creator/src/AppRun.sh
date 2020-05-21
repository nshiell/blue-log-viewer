#! /bin/bash

APPDIR=`dirname $0`

if python3 -c "import PyQt5"; then
    python3 ${APPDIR}/opt/Densify/blue-log-viewer.py $@
else
    export PATH="$PATH":"${APPDIR}"/usr/bin
    ${APPDIR}/usr/bin/python3 ${APPDIR}/opt/Densify/blue-log-viewer.py $@
fi