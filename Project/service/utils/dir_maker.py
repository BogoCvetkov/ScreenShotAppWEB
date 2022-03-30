import pathlib
from datetime import datetime
import os, shutil

"""
This module contains basic functions for creating a dealing with folder creation in the App
"""


# Creates a folder with the current date, to store the screenshots it takes
def create_dir( account ):
	main_folder = "Ad_library_screens"
	subfolder_2 = account
	final_folder = pathlib.Path.cwd().parent.joinpath( main_folder, subfolder_2 )

	if os.path.exists( final_folder ):
		shutil.rmtree( final_folder, ignore_errors=True )
	final_folder.mkdir( parents=True, exist_ok=True )

	return final_folder