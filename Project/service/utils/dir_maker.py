import pathlib
from datetime import datetime
import os,shutil

"""
This module contains basic functions for creating a dealing with folder creation in the App
"""


# Creates a folder with the current date, to store the screenshots it takes
def create_dir(user,account):
    today = datetime.today().strftime("%d_%m")
    main_folder = "Ad_library_screens"
    subfolder_1 = user
    subfolder_2 = account
    final_folder = pathlib.Path.cwd().parent.joinpath(main_folder, subfolder_1, subfolder_2)
    if os.path.exists(final_folder):
        shutil.rmtree(final_folder,ignore_errors=True )
    final_folder.mkdir(parents=True,exist_ok=True)
    return final_folder


# This functions checks if the folder is created
# def check_dir():
#     today = datetime.today().strftime("%d_%m")
#     folder = "Ad_library_screens"
#     subfolder = f"screenshots_{today}"
#     final_folder = pathlib.Path.cwd().parent.joinpath(folder, subfolder)
#     return final_folder


if __name__ == "__main__":
    directory = create_dir("Toshko")
    print(directory)
