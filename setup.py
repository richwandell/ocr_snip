import opcode
import os
import sys
import shutil

from cx_Freeze import setup, Executable

main_dlls, venv_dlls, main_lib, venv_lib = "", "", "", ""
for item in sys.path:
    if "\\DLLs" in item and "\\.venv\\DLLs" not in item:
        main_dlls = item
    elif "\\.venv\\DLLs" in item:
        venv_dlls = item
    elif "\\Lib" in item and "\\.venv\\Lib" not in item:
        main_lib = item

venv_lib = venv_dlls.replace("\\DLLs", "\\Lib")

# copy DLL's folder from main interpreter to venv
try:
    shutil.rmtree(venv_dlls)
    shutil.copytree(main_dlls, venv_dlls)
except:
    pass

# copy system distutils into venv
try:
    shutil.rmtree(venv_lib + "\\distutils")
    shutil.copytree(main_lib + "\\distutils", venv_lib + "\\distutils")
except:
    pass

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('main.py', base=base, targetName='ocrsnip')
]

tesseract_path = os.path.join(os.path.dirname(__file__), 'tesseract')
base_folder = os.path.join(os.path.dirname(__file__))

setup(name='OCR Snip',
      version='1.0',
      description='',
      options={
          'build_exe': {
              'include_files': [
                  (tesseract_path, 'tesseract'),
                  (base_folder + "\\lasso.ico", "lasso.ico")
              ]
          },
          'bdist_msi': {
                'upgrade_code': "{f21d72b8-7311-4b51-8741-f72bbd9ae757}",
                'install_icon': base_folder + "\\lasso.ico"
          }
      },
      executables=executables)
