#!/usr/bin/env bash

# Create Build Directory
mkdir -p build && cd build

# Grab AppImageTools
wget -nc "https://raw.githubusercontent.com/TheAssassin/linuxdeploy-plugin-conda/master/linuxdeploy-plugin-conda.sh"
wget -nc "https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage"
wget -nc "https://github.com/AppImage/AppImageKit/releases/download/12/appimagetool-x86_64.AppImage"
chmod +x linuxdeploy-x86_64.AppImage linuxdeploy-plugin-conda.sh appimagetool-x86_64.AppImage

mkdir -p ./AppDir/opt/Densify/
cp -Rfp ../src/* ./AppDir/opt/Densify/

# Set Environment
export CONDA_CHANNELS='local;conda-forge'
export PIP_REQUIREMENTS='pyqt5'

# Deploy
./linuxdeploy-x86_64.AppImage \
   --appdir AppDir \
    -i ../../artwork/blue-log-viewer.png \
    -d ../../artwork/blue-log-viewer.desktop \
    --plugin conda \
    --custom-apprun ../src/AppRun.sh \
    --output appimage

# Prepare Script to Sign
cp ../src/signAppImage.sh .
