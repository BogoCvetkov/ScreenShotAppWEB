from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv("../.env")

user=os.environ["DB_USER"]
password=os.environ["DB_PASS"]
db_url = os.environ["DB_URL"].format(user, password)

engine = create_engine(db_url, echo=False, future=True)
Session = sessionmaker(engine)