from Project.scraper.web_driver import BuildWebDriver
from Project.scraper.capture_bot import AdCapture
from Project.model.pages_model import pages_Model
from Project.model.account_model import account_Model
from Project.model.user_model import user_Model
from Project.utils.to_pdf import PdfBuilder
from dotenv import load_dotenv

load_dotenv("../.env")

driver = BuildWebDriver(headless=False)

ready_driver = driver.build_driver()

class capture_Controller():

    def __init__(self,user,driver):
        self.user = {"username":user[2],"id":user[0]}
        self.driver = driver

    def capture_and_send_all(self):
        accounts = self._get_user_accounts()
        for acc in accounts:
            self._capture(acc)

    def capture_and_send_one(self,acc_id):
        account=self._get_account_by_id(acc_id)
        self._capture(account)

    def _capture(self,account):
        bot = AdCapture(self.driver, user_folder=self.user["username"], acc_folder=account[2])
        pages = pages_Model.get_page(acc_id=account[0])
        bot.capture_db_pages(pages_list=pages)
        PdfBuilder.convert_to_pdf(folder=bot.file_dir, quality=80)

    def _get_user_accounts(self):
        data= account_Model.get_account(user_id=self.user["id"])
        return data

    def _get_account_by_id(self,id):
        data = account_Model.get_account(id=id)
        return data


users = user_Model.get_all_users()

for user in users:
    bot = capture_Controller(user, ready_driver)
    bot.capture_and_send_all()

ready_driver.close()


