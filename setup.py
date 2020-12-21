import opcode
import os
import sys
import shutil

from cx_Freeze import setup, Executable


def build_windows():
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
        if os.path.exists(venv_dlls):
            shutil.rmtree(venv_dlls)
        shutil.copytree(main_dlls, venv_dlls)
    except:
        pass

    # copy system distutils into venv
    try:
        if os.path.exists(venv_lib + "\\distutils"):
            shutil.rmtree(venv_lib + "\\distutils")
        shutil.copytree(main_lib + "\\distutils", venv_lib + "\\distutils")
    except:
        pass

    base = 'Win32GUI' if sys.platform == 'win32' else None

    tesseract_path = os.path.join(os.path.dirname(__file__), 'tesseract')
    images_path = os.path.join(os.path.dirname(__file__), "images")
    lasso_path = os.path.join(os.path.dirname(__file__), "image", "lasso.ico")

    setup(
        name='OCR Snip',
        version='1.0',
        description='',
        options={
            'build_exe': {
                'include_files': [
                    (tesseract_path, 'tesseract'),
                    (images_path, "images")
                ]
            },
            'bdist_msi': {
                'upgrade_code': "{f21d72b8-7311-4b51-8741-f72bbd9ae757}",
                'install_icon': lasso_path
            }
        },
        executables=[
            Executable(
                'main.py',
                base=base,
                targetName='ocrsnip',
                shortcutName="OCR Snip",
                shortcutDir="DesktopFolder",
            )
        ]
    )


if sys.platform == 'win32':
    build_windows()


