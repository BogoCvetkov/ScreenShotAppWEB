from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import declarative_base
import os

user = os.environ["DB_USER"]
password = os.environ["DB_PASS"]
db_url = os.environ["DB_URL"].format( user, password )

Base = declarative_base()

engine = create_engine( db_url, echo=False, future=True )
Session = scoped_session( sessionmaker( bind=engine ) )