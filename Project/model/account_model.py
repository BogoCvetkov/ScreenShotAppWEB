from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship
from Project.model.common.base_mixin import BaseMixin
from Project.model.base_model import Base


class AccountModel( Base, BaseMixin ):
	__tablename__ = "accounts"

	id = Column( Integer, primary_key=True )
	name = Column( String, nullable=False )
	email = Column( String, unique=True, nullable=False )
	email_body = Column( String )
	active = Column( Boolean, default=True )
	pages = relationship( "PageModel",
	                      cascade="all,delete-orphan",
	                      backref="accounts",
	                      passive_deletes=True )
