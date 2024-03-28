from irspy.qt.ui_to_py import convert_ui, create_translate, convert_resources
import os
from distutils.sysconfig import get_python_lib

convert_ui(f'{os.getcwd()}/src/ui', f'./src/ui/py', resources_path="src.ui.resources")
convert_resources(f'{get_python_lib()}/irspy/qt/resources', './src/ui/resources')
