#!/bin/bash
cd "$(dirname "$0")"

if [[ -d ./_temp_home ]]; then
    rm -rf ./_temp_home
fi

if [[ -d ./AppDir ]]; then
    rm -rf ./AppDir
fi

if [[ -d ./buildset ]]; then
    rm -rf ./buildset
fi

rm -rf ./build