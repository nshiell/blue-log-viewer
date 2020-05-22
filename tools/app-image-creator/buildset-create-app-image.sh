#!/usr/bin/env bash

# Stop on first error
set -e

cd "$(dirname "$0")"

# Create Build Directory
mkdir -p ../../release

# Grab AppImageTools
wget -nc "https://raw.githubusercontent.com/TheAssassin/linuxdeploy-plugin-conda/master/linuxdeploy-plugin-conda.sh"
wget -nc "https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage"
chmod +x linuxdeploy-x86_64.AppImage linuxdeploy-plugin-conda.sh

mkdir -p ./AppDir/opt/blue-log-viewer
cp -Rfp ./buildset/src/* ./AppDir/opt/blue-log-viewer
rm ./AppDir/opt/blue-log-viewer/AppRun.sh

# Set Environment
export CONDA_CHANNELS='local;conda-forge'
export PIP_REQUIREMENTS='pyqt5'

# Deploy
./linuxdeploy-x86_64.AppImage \
   --appdir AppDir \
    -i ./buildset/artwork/blue-log-viewer.png \
    -d ./buildset/artwork/blue-log-viewer.desktop \
    --plugin conda \
    --custom-apprun ./buildset/src/AppRun.sh \
    --output appimage

rm -Rf ./_temp_home
rm -Rf ./AppDir

mv Blue*.AppImage ../../release

cd ../../release
echo -e "\e[32m" # green text
echo "Released into: $(pwd)"
ls -l
echo -e "\e[0m"