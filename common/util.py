import os
import sys
from pathlib import Path


# def absolute_path(file_name):
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#
#     return os.path.join(base_path, file_name)


class Util:

    @staticmethod
    def absolute_path(file_name):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, file_name)

    @staticmethod
    def find_file(file_name):
        for directory_path, directory_names, files in os.walk('.'):
            for file_name_in_directory in files:
                if file_name_in_directory == file_name:
                    return os.path.join(directory_path, file_name_in_directory)

        # with os.scandir('.') as entries:
        #     for entry in entries:
        #         if entry.is_file() and entry.name == file_name:
        #             print("1" + entry.name)
        #             return Util.absolute_path(entry.name)
        #         elif entry.is_dir():
        #             print("2" + entry.name)
        #             return Util.find_file(entry.name)

        # print('888888888888888888')
        # for item in Path(file_name).iterdir():
        #     print(item.name)
