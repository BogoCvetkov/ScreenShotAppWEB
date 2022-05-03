from sqlalchemy import Column, String, Integer, ForeignKey
from Project.model.common.base_mixin import BaseMixin
from Project.model.DB import Base


class KeywordModel( Base, BaseMixin ):
	__tablename__ = "keywords"

	id = Column( Integer, primary_key=True )
	keyword = Column( String, nullable=False )
	account_id = Column( Integer, ForeignKey( "accounts.id", ondelete="CASCADE" ),
	                     nullable=False )