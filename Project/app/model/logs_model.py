from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from Project.app.model.common.base_mixin import BaseMixin
from Project.app.model import Base
from datetime import datetime


class LogModel( Base, BaseMixin ):
	__tablename__ = "logs"

	id = Column( Integer, primary_key=True )
	started_by = Column( String, nullable=False, default="bot" )
	account_name = Column( String, nullable=False )
	log_msg = Column( String )
	log_details = Column( String )
	date = Column( DateTime )
	fail = Column( Boolean, default=False )
	user_id = Column( Integer )
	account_id = Column( Integer, ForeignKey( "accounts.id", ondelete="CASCADE" ),
	                     nullable=False )