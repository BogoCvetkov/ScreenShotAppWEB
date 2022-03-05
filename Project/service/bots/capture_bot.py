from Project.service.scraper.web_driver import BuildWebDriver
from Project.service.scraper.ad_capture import AdCapture
from Project.model.pages_model import PageModel
from Project.model.account_model import AccountModel
from Project.model.user_model import UserModel
from Project.service.utils.to_pdf import PdfBuilder
from Project.model.base import Session
from dotenv import load_dotenv

load_dotenv("../../.env")

driver = BuildWebDriver(headless=False)


class CaptureBot():

    def __init__(self, user, driver, session):
        self.user = user
        self.driver = driver
        self.session = session

    def capture_and_send_all(self):
        accounts = self._get_all_ad_accounts()
        for account in accounts:
            self._capture(account)

    def capture_and_send_one(self,acc_id):
        account=self._get_ad_account_by_id(acc_id)
        self._capture(account)

    def _capture(self, account):
        bot = AdCapture(self.driver, user_folder=self.user.username, acc_folder=account.name)
        pages = PageModel.search(self.session,account_id=account.id)
        bot.capture_db_pages(pages_list=pages)
        PdfBuilder.convert_to_pdf(folder=bot.file_dir, quality=80)

    def _get_all_ad_accounts(self):
        data = AccountModel.get_all(self.session)
        return data

    def _get_ad_account_by_id(self,id):
        data = AccountModel.get_by_id(self.session,id)
        return data

    def close_session(self):
        self.session.close()



if __name__ == "__main__":
    session = Session()
    user = UserModel.get_by_id(session,8)

    ready_driver = driver.build_driver()

    bot = CaptureBot(user, ready_driver, session)
    bot.capture_and_send_all()

    bot.close_session()

# ready_driver.close()


