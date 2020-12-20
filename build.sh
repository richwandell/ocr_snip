#!/bin/bash
set -m
mkdir -p tesseract/tessdata

if [[ "$1" == "all" ]]; then
  if hash cygpath 2>/dev/null; then
    # building for windows using cygwin
    cd tesseract \
      && git clone https://github.com/microsoft/vcpkg --depth 1 \
      && cd tessdata \
      && wget --no-check-certificate https://raw.githubusercontent.com/tesseract-ocr/tessdata/master/eng.traineddata \
      && cd .. \
      && cd vcpkg \
      && ./bootstrap-vcpkg.bat \
      && ./vcpkg.exe install tesseract:x64-windows-static \
      && cd .. \
      && cp vcpkg/packages/tesseract_x64-windows-static/tools/tesseract/tesseract.exe . \
      && chmod -R 777 vcpkg \
      && rm -R vcpkg \
      && cd .. \
      && pipenv install \
      && pipenv run python setup.py build \
      && pipenv run python setup.py build_msi
  fi
fi



