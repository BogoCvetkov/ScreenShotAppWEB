from selenium import webdriver
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

'''
This module contains the classes for navigating chrome browser in headless mode and creating screenshots of the desired
pages. It is based on the selenium framework. It supports different types of capturing:  by page id / by keyword
'''

driver_loc = Path.cwd().parent.joinpath( "Drivers", "chromedriver.exe" )


class BuildWebDriver:
	"""
	This time we're using the class with standard instance methods. Because the class can be instantiated
	with different browser options. And It needs to be instantiated anew every time we're creating a new batch
	of pages to be captured in the current session of the browser - e.g in the current instance of the driver class.
	"""

	default_loc = driver_loc

	def __init__( self, headless=True ):
		self._options = webdriver.ChromeOptions()
		if headless:
			self._options.add_argument( "headless" )
			self._options.add_argument( "disable-gpu" )

	# adding additional options to the instance if needed
	def add_options( self, *args ):
		if args:
			for arg in args:
				self._options.add_argument( arg )

	# Creating the driver (chrome session) to be used for screenshots
	def build_driver( self, webdriver_dir=default_loc ):
		cur_driver = webdriver.Chrome( executable_path=webdriver_dir,
		                               options=self._options )
		cur_driver.implicitly_wait( 15 )

		return cur_driver