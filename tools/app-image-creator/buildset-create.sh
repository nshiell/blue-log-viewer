#!/bin/bash

cd "$(dirname "$0")"

#
# Updates the latest app into src and artwork directories
#

mkdir -p ./buildset/artwork
cp -Rp ./src ./buildset/src

cp -Rfp ../../blue-log-viewer.py ./buildset/src
cp -Rfp ../../blueLogViewer/ ./buildset/src

mkdir -p ./buildset/artwork

cp ../../artwork/blue-log-viewer.png ./buildset/artwork
cp ../../artwork/blue-log-viewer.desktop ./buildset/artwork
