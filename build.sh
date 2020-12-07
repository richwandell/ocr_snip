mkdir -p tesseract

if [[ "$1" == "all" ]]; then
  if hash cygpath 2>/dev/null; then
    # building for windows using cygwin
    cd tesseract \
      && git clone https://github.com/microsoft/vcpkg --depth 1 \
      && git clone https://github.com/tesseract-ocr/tessdata.git --depth 1 \
      && cd vcpkg \
      && ./bootstrap-vcpkg.bat \
      && ./vcpkg.exe install tesseract:x64-windows-static \
      && cd .. \
      && cp vcpkg/packages/tesseract_x64-windows-static/tools/tesseract/tesseract.exe . \
      && chmod -R 777 vcpkg \
      && rm -R vcpkg \
      && chmod -R 777 tessdata/.git \
      && rm -R tessdata/.git \
      && cd ..
  fi
fi



python setup.py build



