from selenium import webdriver
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests

load_dotenv()

'''
This module contains the classes for navigating chrome browser in headless mode and creating screenshots of the desired
pages. It is based on the selenium framework. It supports different types of capturing:  by page id / by keyword
'''


class BuildWebDriver:
    """
    This time we're using the class with standard instance methods. Because the class can be instantiated
    with different browser options. And It needs to be instantiated anew every time we're creating a new batch
    of pages to be captured in the current session of the browser - e.g in the current instance of the driver class.
    """

    default_loc = ChromeDriverManager().install()
    executor_url = "http://192.168.176.1:4444"

    def __init__(self, headless=True):
        self._options = webdriver.ChromeOptions()
        if headless:
            self._options.add_argument("headless")
            self._options.add_argument("disable-gpu")

    # adding additional options to the instance if needed
    def add_options(self, *args):
        if args:
            for arg in args:
                self._options.add_argument(arg)

    # Creating the driver (chrome session) to be used for screenshots
    def build_driver(self, webdriver_dir=default_loc):
        cur_driver = webdriver.Chrome(executable_path=webdriver_dir,
                                      options=self._options)
        cur_driver.implicitly_wait(15)

        return cur_driver

    # Creating a driver that uses Selenium Grid - (server-client) based approach
    # used in the scheduling script
    def build_remote_driver(self):
        cur_driver = webdriver.Remote(command_executor=self.executor_url,
                                      options=self._options)
        cur_driver.implicitly_wait(15)

        return cur_driver

    @classmethod
    def reuse_session(cls, session_id):
        # Check if session is valid
        check = cls._check_session_is_valid(session_id)

        # If the existing session is valid, reuse it
        if check["valid_sess"]:
            new_driver = cls._reuse_session(cls.executor_url, session_id)
        # If not try to connect to another existing one
        else:
            new_driver = cls._reuse_session(cls.executor_url, check["sess_list"][0])
        return new_driver

    @classmethod
    def close_all_sessions(cls):
        res = requests.get("http://localhost:4444/status")
        sess_list = [n["session"]["sessionId"] for n in res.json()["value"]["nodes"][0]["slots"] if n["session"]]
        for sess in sess_list:
            cls.reuse_session(sess).quit()

    '''A solution for reusing a selenium session I found on the internet - 
    https://tarunlalwani.com/post/reusing-existing-browser-session-selenium-grid-python/
    It's a monkey patch of the selenium library. I want to reuse the same session for 2 reasons:
    - opening a new browser session everytime is expensive and wasteful in this particular case
    - navigating in the same session mimics better human behavior, thus reducing the probability of block from facebook.'''

    @classmethod
    def _reuse_session(cls, executor_url, session_id):
        from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

        original_command = RemoteWebDriver.execute

        def custom_command_execute(self, command, params):
            if command == "newSession":
                return { "success": 0, "value": None, "sessionId": session_id }
            else:
                return original_command(self, command, params)

        RemoteWebDriver.execute = custom_command_execute

        new_driver = webdriver.Remote(command_executor=executor_url,
                                      options=webdriver.ChromeOptions())
        new_driver.session_id = session_id

        RemoteWebDriver.execute = original_command

        return new_driver

    # Check if session still exists
    @classmethod
    def _check_session_is_valid(cls, session_id):
        res = requests.get("http://localhost:4444/status")
        sess_list = [n["session"]["sessionId"] for n in res.json()["value"]["nodes"][0]["slots"] if n["session"]]
        return { "sess_list": sess_list, "valid_sess": session_id in sess_list }