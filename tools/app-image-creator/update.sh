#!/bin/bash

cd "$(dirname "$0")"

#
# Updates the latest app into src and res directory
#

cp -Rfp ../blue-log-viewer.py ./src
cp -Rfp ../test/ ./src
cp -Rfp ../blueLogViewer/ ./src

mkdir -p res

cp ../artwork/blue-log-viewer.png ./res
cp ../artwork/blue-log-viewer.desktop ./res
