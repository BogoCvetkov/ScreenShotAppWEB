from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship
from Project.app.model.common.base_mixin import BaseMixin
from Project.app.model import Base


class AccountModel( Base, BaseMixin ):
	__tablename__ = "accounts"

	id = Column( Integer, primary_key=True )
	name = Column( String, unique=True, nullable=False )
	email = Column( String, unique=True, nullable=False )
	email_body = Column( String )
	active = Column( Boolean, default=True )
	last_scrape_fail = Column( Boolean, default=False )
	last_email_fail = Column( Boolean, default=False )
	pages = relationship( "PageModel",
	                      cascade="all,delete-orphan",
	                      backref="account",
	                      passive_deletes=True )
	screenshot = relationship( "ScreenShotModel", uselist=False, backref="account",
	                           cascade="all,delete-orphan", passive_deletes=True )
	logs = relationship( "LogModel", backref="account",
	                     cascade="all,delete-orphan", passive_deletes=True )