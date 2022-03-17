from Project.app.service.scraper.web_driver import BuildWebDriver
from Project.app.service.scraper.ad_capture import AdCapture
from Project.app.model.all_models import PageModel, ScreenShotModel
from Project.app.service.utils.to_pdf import PdfBuilder
from Project.app.service.bots.base import BaseBot
from datetime import datetime


class CaptureBot( BaseBot ):

	def __init__( self, driver, db_sess, user=None ):
		super().__init__( db_sess, user )
		self.driver = driver

	def capture_all( self ):
		accounts = self._get_all_ad_accounts()
		for account in accounts:
			self._run_with_status( account, self._capture )
		self._retry_on_failed( self._capture )
		return self.status

	def capture_from_list( self, id_list ):
		for id in id_list:
			account = self._get_ad_account_by_id( id )
			if account:
				self._run_with_status( account, self._capture )
		self._retry_on_failed( self._capture )
		return self.status

	def _capture( self, account ):
		bot = AdCapture( self.driver, acc_folder=account.name )
		pages = account.pages
		info = bot.capture_many( pages_list=pages )
		self._create_pdf( folder=bot.file_dir, account=account )
		return info

	def _create_pdf( self, folder, account ):
		pdf_loc = PdfBuilder.convert_to_pdf( folder=folder, quality=80 )

		# If there is no record for the pdf file location, create one in the ScreenShot table
		if not account.screenshot:
			account.screenshot = ScreenShotModel( account_id=account.id )

		account.screenshot.file_dir = pdf_loc
		account.screenshot.last_captured = datetime.now()

	def close_driver( self ):
		self.driver.close()


if __name__ == "__main__":
	'''
		driver = BuildWebDriver( headless=False )
		session = Session()
		user = UserModel.get_by_id( session, 8 )
	
		ready_driver = driver.build_driver()
	
		# bot = CaptureBot( user, ready_driver, session )
		bot.capture_all()
	
		bot.close_session()
	
		ready_driver.close()
	'''