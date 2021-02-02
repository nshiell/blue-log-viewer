#!/bin/bash

# Stop on first error
set -e

cd "$(dirname "$0")"

./icon-svg-to-png.sh
./app-image-create.sh