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
	pages = relationship( "PageModel",
	                      cascade="all,delete-orphan",
	                      backref="accounts",
	                      passive_deletes=True )
	screenshot = relationship( "ScreenShotModel", uselist=False, backref="screenshots",
	                           cascade="all,delete-orphan", passive_deletes=True )