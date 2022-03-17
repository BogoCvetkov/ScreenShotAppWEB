import time, datetime
import random, re, urllib, os
from dotenv import load_dotenv
from Project.app.errors import AppServiceError
from Project.app.service.utils.dir_maker import create_dir
from Project.app.service.scraper.web_driver import BuildWebDriver
from selenium.webdriver.common.keys import Keys

load_dotenv()


class AdCapture:
	today = datetime.datetime.today().strftime( "%d_%m" )
	condition = os.environ.get( "SEARCH_CONDITION" )

	def __init__( self, driver, acc_folder ):
		self._driver = driver
		self.keyword_url = os.environ.get( "KEYWORD_URL" )
		self.fb_url = os.environ.get( "FB_URL" )
		self.file_dir = create_dir(  acc_folder )

	# Private method that prepares the browser window before making the screenshot
	def _prepare_window( self, scrolls, entity ):
		# Clicking the privacy policy button to allow page scrolling
		try:
			button = self._driver.find_element_by_xpath(
				"//button[text()[contains(.,'cookie')]]" )
			button.click()
		except:
			pass

		# Randomizing time between actions to mimic human behaviour
		time.sleep( random.randint( 4, 6 ) )
		get_body = self._driver.find_element_by_tag_name( 'body' )
		text_in_body = get_body.text

		# Regular Expression pattern for defining if a page has any ads running at the moment
		if re.search( self.condition, text_in_body ):
			print( f"No Ads Found For /{entity}/" )
			return f"No Ads Found For /{entity}/ \n"

		for n in range( scrolls ):
			get_body.send_keys( Keys.END )
			time.sleep( random.randint( 1, 3 ) )

		self._driver.set_window_size( 1920, 1080 )
		size = get_body.size
		self._driver.set_window_size( size["width"], size["height"] )

	# This method takes care of starting the chrome session(headless/normal) using the driver from the
	# previous class, navigate to the facebook pages and take screenshots of their ads
	# It uses randomized time intervals between each interaction with the web page to mimic human behaviour and
	# avoid blocking from FB servers
	# Private method used internally by the other methods in this class
	def _construct_capture_flow( self, page_name=None, page_id=None, scrolls=3, country="ALL",
	                             keyword="marketing" ):
		try:
			if page_id:
				entity = page_name
				final_url = self.fb_url.format( country, page_id )
				filename = f"{self.file_dir}\{self.today}_apage_{entity}.png"
			else:
				entity = keyword
				final_url = self.keyword_url.format( country, keyword )
				entity = urllib.parse.unquote( entity )
				filename = f"{self.file_dir}\{self.today}_key_{entity}.png"

			self._driver.get( final_url )

			self._prepare_window( scrolls, entity )

			self._driver.get_screenshot_as_file( filename )

			return f"Screenshot for/ {entity} / captured \n"

		except Exception as e:
			message = f"Failed to scrape for: {entity}."
			raise AppServiceError( message=message )

	def capture_page( self, page_id, page_name, scrolls=3, country="ALL" ):
		self._construct_capture_flow( page_id=page_id,
		                              page_name=page_name,
		                              scrolls=scrolls,
		                              country=country )

	def capture_many( self, pages_list, scrolls=3, country="ALL" ):
		status = ""

		for page in pages_list:
			res = self._construct_capture_flow( page_id=page.page_id,
			                                    page_name=page.name,
			                                    scrolls=scrolls,
			                                    country=country )
			status += res

		return status

	def capture_by_keyword( self, keyword, country="BG", scrolls=3 ):
		keyword = urllib.parse.quote( keyword )
		res = self._construct_capture_flow( keyword=keyword,
		                                    country=country,
		                                    scrolls=scrolls )

		return res


if __name__ == "__main__":
	# Used fot testing in Development

	# driver=BuildWebDriver().build_driver()
	# page_bot=AdLibCapture(driver)
	#
	# ## Bulk Capture
	# pages=[(0,3859501477945,"Kaufland"),(1,312617136169551,"SanaMedic"),(2,24078343402632998,"GoSport"),(3,11839230704429977,'Dev.bg'),(4,475170749544771,"Body_Aesthetics"),(5,513523225491395,"Viessman")]
	# page_bot.capture_bulk_pages(pages)

	## Capture By Keyword
	driver = BuildWebDriver( headless=False )
	ready_driver = driver.build_driver()
	bot = AdCapture( ready_driver, "Bogo", "Skoda" )
	pages = [(0, 3859501477945, "Kaufland"), (4, 475170749544771, "Body_Aesthetics"),
	         (5, 513523225491395, "Viessman")]
	bot.capture_many( pages )
	bot.capture_page( 312617136169551, "SanaMedic" )
	bot.capture_page( 240783402632998, "GoSport" )
	bot.capture_by_keyword( keyword="Чанта", scrolls=6 )
	bot.close()