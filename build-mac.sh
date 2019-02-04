# ssh nicholas@192.168.56.1:Documents/blue-log-viewer/build-mac.sh . | sh -
# chmod +x build-mac.sh
# ./build-mac.sh

# Stop on first error
#set -e
set -o xtrace

echo "Enter Password of remote server"

ssh -D 1080 -q -N -f nicholas@192.168.56.1
#curl --socks5-hostname 127.0.0.1:1080 https://github.com

echo "Enter Password of remote server"
scp -rp nicholas@192.168.56.1:Documents/blue-log-viewer . && \
hdiutil attach ./blue-log-viewer/resources/Command_Line_Tools_macOS_10.12_for_Xcode_9.2.dmg && \
installer -store -pkg \
    "/Volumes/Command Line Developer Tools/Command Line Tools (macOS Sierra version 10.12).pkg" \
    -target / && \
chmod +x ./blue-log-viewer/resources/homebrew-installer.sh && \
env http_proxy=socks5h://127.0.0.1:1080 \
    HTTPS_PROXY=socks5h://127.0.0.1:1080 \
    ALL_ROXY=socks5h://127.0.0.1:1080 \
    ./blue-log-viewer/resources/homebrew-installer.sh && \
env http_proxy=socks5h://127.0.0.1:1080 \
    HTTPS_PROXY=socks5h://127.0.0.1:1080 \
    ALL_ROXY=socks5h://127.0.0.1:1080 \
    brew install pyqt5 && \
cd blue-log-viewer && \
python3.7 blue-log-viewer.py
