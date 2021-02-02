#!/usr/bin/env bash

# Stop on first error
set -e

DIR="$(dirname "$0")"

cd "$DIR"

if [[ ! -d "svg-to-png-using-chromium" ]]; then
    git clone git@github.com:nshiell/svg-to-png-using-chromium.git svg-to-png-using-chromium
fi

docker run -it \
    -v "$PWD/svg-to-png-using-chromium:/usr/src/app" \
    -v "$PWD/../artwork/icon.svg:/usr/src/app/icon.svg" \
    markadams/chromium-xvfb-py3 bash -c \
        "pip3 install pillow && python3 ./svg-to-png-using-chromium.py --width 256 icon.svg && chown $(id -u ${USER}):$(id -g ${USER}) icon.png"

mv svg-to-png-using-chromium/icon.png ../artwork/blue-log-viewer.png

echo -ne "\e[32m" # green text
echo -ne "Created png: $(realpath $PWD/../artwork/blue-log-viewer.png)"
echo -e "\e[0m"
