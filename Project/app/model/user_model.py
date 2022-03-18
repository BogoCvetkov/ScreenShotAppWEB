from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import validates
from Project.app.model.common.base_mixin import BaseMixin
from sqlalchemy import select
from Project.app.model import Base
from Project.app.auth import security

class UserModel( Base, BaseMixin ):
	__tablename__ = "users"

	id = Column( Integer, primary_key=True )
	email = Column( String, unique=True, nullable=False )
	username = Column( String, unique=True, nullable=False )
	password = Column( String, nullable=False )
	admin = Column( Boolean, default=False )

	# Hash password upon instantiation
	@validates( "password" )
	def hash_password( self, key, value ):
		return security.bhash_value( value )

	def verify_password( self, submit_password ):
		return security.bcheck_hash( submit_password, self.password )

	@classmethod
	def find_by_email( cls, session, email ):
		user = session.scalars( select( cls ).where( cls.email == email ) ).first()
		return user