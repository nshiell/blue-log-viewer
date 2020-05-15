#!/usr/bin/env bash

# Stop on first error
set -e

TOOLS_DIR="$(dirname "$0")"
SOURCE_DIR="../"
BUILD_RIR="$SOURCE_DIR/build"
APP_DIR="$BUILD_RIR/AppDir"
BLV_DIR="$APP_DIR/usr/opt/blue-log-viewer"
APP_BIN_DIR="$APP_DIR/usr/bin"

cd "$TOOLS_DIR"

if [[ ! -d "$APP_BIN_DIR" ]]; then
    mkdir -p "$APP_BIN_DIR"
fi

if [[ ! -f "linuxdeploy-plugin-conda.sh" ]]; then
    wget -c "https://raw.githubusercontent.com/TheAssassin/linuxdeploy-plugin-conda/master/linuxdeploy-plugin-conda.sh"
    chmod +x linuxdeploy-plugin-conda.sh
fi

if [[ ! -f "linuxdeploy-x86_64.AppImage" ]]; then
    wget -c "https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage"
    chmod +x linuxdeploy-x86_64.AppImage
fi

cat > capsvoxgan.desktop <<\EOF
[Desktop Entry]
Version=1.0
Name=CapsVoxGAN
Exec=blue-log-viewer
Terminal=false
Type=Application
Icon=icon
Categories=Graphics;Science;Engineering;
StartupNotify=true
EOF

export CONDA_PYTHON_VERSION=3.7.4
#export CONDA_CHANNELS=pytorch
export CONDA_PACKAGES="pyqt==5.9.2"
./linuxdeploy-plugin-conda.sh --appdir "$APP_DIR"

mkdir -p "$BLV_DIR"
cp -Rfp "$SOURCE_DIR/blueLogViewer" "$BLV_DIR"
cp -Rfp "$SOURCE_DIR/blue-log-viewer.py" "$BLV_DIR"
cp -Rfp "$SOURCE_DIR/test" "$BLV_DIR"


cat > "$APP_BIN_DIR/blue-log-viewer" <<\EOF
#!/usr/bin/env bash

# get actual directory
export RUN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$RUN_DIR/usr/bin/activate"

python "$RUN_DIR/usr/opt/blue-log-viewer/blue-log-viewer.py"
EOF

chmod +x "$APP_BIN_DIR/blue-log-viewer"

./linuxdeploy-x86_64.AppImage --appdir "$APP_DIR" -i ../icon.png -d capsvoxgan.desktop --output appimage

exit

mv $(ls CapsVoxGAN*) ../../CapsVoxGAN.AppImage

rm -r AppDir/
rm -r _temp_home/
rm capsvoxgan.desktop
rm linuxdeploy-plugin-conda.sh
rm linuxdeploy-x86_64.AppImage