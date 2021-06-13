#!/bin/bash
set -m
mkdir -p tesseract/tessdata

function build_app() {
    pipenv install \
    && pipenv run python setup.py build \
    && pipenv run python setup.py bdist_msi
}

function download_tessdata() {
    FILE=tesseract/tessdata/eng.traineddata
    if [ -f "$FILE" ]; then
        echo "Tessdata exists, skipping download"
    else
        cd tesseract/tessdata \
        && curl https://raw.githubusercontent.com/tesseract-ocr/tessdata/master/eng.traineddata --output eng.traineddata \
        && cd ../..
    fi
}

function make_tesseract() {
    FILE=tesseract/tesseract.exe
    if [ -f "$FILE" ]; then
        echo "tesseract.exe exists, skipping tesseract build step"
    else
        cd tesseract \
          && git clone https://github.com/microsoft/vcpkg --depth 1 \
          && cd vcpkg \
          && ./bootstrap-vcpkg.bat \
          && ./vcpkg.exe install tesseract:x64-windows-static \
          && cd .. \
          && cp vcpkg/packages/tesseract_x64-windows-static/tools/tesseract/tesseract.exe . \
          && chmod -R 777 vcpkg \
          && rm -R vcpkg \
          && cd ..
    fi
}

if [[ "$1" == "all" ]]; then
    if hash cygpath 2>/dev/null; then
        # building for windows using cygwin
        download_tessdata \
        && make_tesseract \
        && build_app
    fi
fi
