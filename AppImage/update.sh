#!/bin/bash

#
# Updates the latest app into src and res directory
#

cp -Rfp ../blue-log-viewer.py ./src
cp -Rfp ../test/ ./src
cp -Rfp ../blueLogViewer/ ./src

exit
cp ../__init__.py ./src
cp ../header.png ./src
cp ../icon.png ./src
cp ../densify ./src
cp ../desktop-icon.png ./res
