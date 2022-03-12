from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime, event
from sqlalchemy.orm import relationship
from Project.app.model.common.base_mixin import BaseMixin
from Project.app.model import Base


class ScreenShotModel( Base, BaseMixin ):
	__tablename__ = "screenshots"

	id = Column( Integer, primary_key=True )
	file_dir = Column( String )
	last_captured = Column( DateTime )
	account_id = Column( Integer, ForeignKey( "accounts.id", ondelete="CASCADE" ),
	                     nullable=False )