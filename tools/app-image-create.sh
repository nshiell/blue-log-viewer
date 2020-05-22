#!/usr/bin/env bash

# Stop on first error
set -e

TOOLS_DIR="$(dirname "$0")"

cd "$TOOLS_DIR"

./app-image-creator/buildset-teardown.sh
./app-image-creator/buildset-create.sh
./app-image-creator/buildset-create-app-image.sh