from Project.service.scraper.ad_capture import AdCapture
from Project.model.all_models import ScreenShotModel
from Project.service.utils.to_pdf import PdfBuilder
from Project.service.bots.base import BaseBot
from datetime import datetime, timedelta


class CaptureBot(BaseBot):
    bot_type = "capture"

    def __init__(self, driver, db_sess, user=None):
        super().__init__(db_sess, user)
        self.driver = driver

    def capture_all(self):
        accounts = self._get_all_ad_accounts()
        for account in accounts:
            if not self._was_scraped_soon(account):
                self._run_for_many(account, self._capture)
            self.db_sess.commit()
        self._retry_on_failed(self._capture)
        return self.status

    # Runs for multiple accounts - exception on single account must not affect the others
    def capture_from_list(self, id_list):
        for id in id_list:
            account = self._get_ad_account_by_id(id)
            if account and not self._was_scraped_soon(account):
                self._run_for_many(account, self._capture)
            self.db_sess.commit()
        self._retry_on_failed(self._capture)
        return self.status

    # Runs for single account - Exceptions are not being handled
    def capture_single(self, id):
        account = self._get_ad_account_by_id(id)
        if account and not self._was_scraped_soon(account):
            self._run_for_one(account, self._capture)

    def _capture(self, account):
        bot = AdCapture(self.driver, acc_folder=account.name)
        pages = [p for p in account.pages if p.active]
        keywords = [k for k in account.keywords if k.active]
        info = bot.capture_many(pages_list=pages, country=account.country)
        info2 = bot.capture_by_keywords(keywords_list=keywords, country=account.country)
        self._create_pdf(folder=bot.file_dir, account=account)
        return f"{info} ; {info2}"

    def _create_pdf(self, folder, account):
        pdf_loc = PdfBuilder.convert_to_pdf(folder=folder, quality=80)

        # If there is no record for the pdf file location, create one in the ScreenShot table
        if not account.screenshot:
            account.screenshot = ScreenShotModel(account_id=account.id)

        account.screenshot.file_dir = pdf_loc
        account.screenshot.last_captured = datetime.now()

    # Check if account was scraped recently - prevent repeated operations
    def _was_scraped_soon(self, account):
        if not account.last_scraped:
            return False
        if account.last_scraped and (datetime.now() - account.last_scraped) > timedelta(minutes=3):
            return False
        time_passed = datetime.now() - account.last_scraped
        details = f"Latest screenshot for {account.name} was {int(time_passed.seconds / 60)} minutes ago. " \
                  f"New screenshots are made only if 15 minutes have passed from the latest one."
        # self.status["skipped"].append({ "account": account.name, "info": details })
        self._log_operation_result(account, "Screenshot was skipped - latest was less than 15 min ago.", details)
        return True

    def close_driver(self):
        self.driver.quit()


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