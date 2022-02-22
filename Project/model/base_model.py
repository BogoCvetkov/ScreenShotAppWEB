import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()


class Model:

    connection = psycopg2.connect(
        host="localhost",
        database="ScreenshotAppWEB",
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"]
    )

    def __init__ (self):
        self._create_table()

    def _create_table(self):
        pass