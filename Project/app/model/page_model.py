from sqlalchemy import Column, String, Integer, ForeignKey
from Project.app.model.common.base_mixin import BaseMixin
from Project.app.model import Base


class PageModel( Base, BaseMixin ):
	__tablename__ = "pages"

	id = Column( Integer, primary_key=True )

	name = Column( String, nullable=False )
	page_id = Column( String, nullable=False )
	account_id = Column( Integer, ForeignKey( "accounts.id", ondelete="CASCADE" ),
	                     nullable=False )